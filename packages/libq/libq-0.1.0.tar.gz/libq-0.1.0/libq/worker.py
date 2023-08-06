import asyncio
import concurrent.futures
import random
import signal
from copy import deepcopy
from datetime import datetime
from functools import partial
from signal import Signals
from typing import Any, Callable, Dict, List, Optional

# from redis.asyncio import ConnectionPool, Redis
from redis.exceptions import ResponseError, WatchError

from libq import defaults, errors, types
from libq.connections import StreamRedis, create_pool
from libq.jobs import Job
from libq.logs import worker_log
from libq.utils import generate_random, get_function, parse_timeout, poll


def _now_secs() -> float:
    return datetime.utcnow().timestamp()


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def _elapsed_from_iso(dt: str, *, now=_now_secs()) -> float:
    _dt = datetime.fromisoformat(dt)
    return _dt.timestamp() - now


class AsyncWorker:

    def __init__(self, queues=None,
                 *,
                 conn=None,
                 id=None,
                 ctx=Optional[Dict[str, Any]],
                 max_jobs=defaults.WORKER_MAX_JOBS,
                 heartbeat_secs=defaults.WORKER_HEARTBEAT_REFRESH,
                 poll_delay=None,
                 handle_signals: bool = True,
                 poll_strategy="block",
                 ):

        self.conn: StreamRedis = conn
        self.id = id or generate_random()
        self.loop = asyncio.get_event_loop()
        self.ctx = ctx or {}
        self.tasks: Dict[str, asyncio.Task[Any]] = {}
        self.main_task: Optional[asyncio.Task[None]] = None
        self._queues = queues or [defaults.QUEUE_NAME]
        self.queues = [
            f"{types.Prefixes.queue_jobs.value}{q}" for q in self._queues]
        self.sem = asyncio.BoundedSemaphore(max_jobs)
        self._max_jobs = max_jobs
        self.poll_delay_s = parse_timeout(
            poll_delay) or defaults.WORKER_POLL_DELAY
        self._poll_strategy = poll_strategy

        self.heartbeat_refresh = parse_timeout(heartbeat_secs)
        self._handle_signals = handle_signals
        if self._handle_signals:
            self._add_signal_handler(signal.SIGINT, self.handle_sig)
            self._add_signal_handler(signal.SIGTERM, self.handle_sig)

        self.birthday: str = _now_iso()
        self.last_job: str = _now_iso()
        self.idle_secs = .0

        self._completed = 0
        self._failed = 0

    async def self_register(self):
        info = types.WorkerInfo(
            id=self.id,
            birthday=self.birthday,
            queues=self._queues,
            running=self.sem._value,
            completed=self._completed,
            failed=self._failed,
        )
        async with self.conn.pipeline() as pipe:
            pipe.setex(f"{types.Prefixes.worker.value}{self.id}", self.heartbeat_refresh + 50,
                       info.json())
            pipe.sadd(f"{types.Prefixes.workers_list.value}", self.id)
            for q in self._queues:
                pipe.sadd(f"{types.Prefixes.queue_workers.value}{q}", self.id)
            await pipe.execute()

    async def unregister(self):
        async with self.conn.pipeline() as pipe:
            pipe.delete(f"{types.Prefixes.worker.value}{self.id}")
            for q in self._queues:
                pipe.srem(f"{types.Prefixes.queue_workers.value}{q}", self.id)
            pipe.srem(f"{types.Prefixes.workers_list.value}", self.id)
            await pipe.execute()

    async def heartbeat(self):
        async for _ in poll(self.heartbeat_refresh):
            worker_log.debug("Heartbeating...")
            await self.self_register()

        worker_log.debug("Heartbeat stopped")

    async def send_command(self, cmd) -> int:
        key = f"{types.Prefixes.worker_commands.value}{self.id}"
        r = await self.conn.rpush(key, cmd)
        return r

    async def commands(self):

        key = f"{types.Prefixes.worker_commands.value}{self.id}"
        async for _ in poll(self.heartbeat_refresh + 2):
            cmd = await self.conn.lpop(key, 1)
            if cmd:
                worker_log.debug(f"===> cmd: {cmd}")
                if cmd[0] == "shutdown":
                    self.handle_sig(Signals.SIGINT)
                    continue

    async def main(self):
        if not self.conn:
            self.conn = await create_pool()
        worker_log.info(f"Starting worker {self.id}")
        worker_log.debug(f"Queues to listen {self.queues}")
        t = self.loop.create_task(self.heartbeat())
        self.tasks["heartbeat"] = t
        t2 = self.loop.create_task(self.commands())
        self.tasks["commands"] = t2

        while True:
            await self._poll_iteration()
        worker_log.debug("Finished main %s", self.id)

    async def _poll_iteration(self):
        keys = deepcopy(self.queues)
        random.shuffle(keys)
        async with self.sem:
            worker_log.debug(f"Waiting new jobs for {self.poll_delay_s} secs")
            task = await self.conn.blpop(keys, self.poll_delay_s)
            if task:
                worker_log.debug(
                    f"Job: {task[1:]} from queue {task[0]}")

        if task:
            _queue = task[0]
            _job = task[1]
            self.last_job = _now_iso()
            await self.start_job(_job, _queue)
        else:
            worker_log.debug("Not jobs found")
            last = _elapsed_from_iso(self.last_job, now=_now_secs())
            self.idle_secs += last

        for job_id, t in list(self.tasks.items()):
            if t.done():
                del self.tasks[job_id]
                t.result()

    async def start_job(self, job_id: str, qname: str):
        in_progress_key = types.Prefixes.job_in_progress.value + job_id
        await self.sem.acquire()
        async with self.conn.pipeline(transaction=True) as pipe:
            await pipe.watch(in_progress_key)
            ongoing_exists = await pipe.exists(in_progress_key)
            if ongoing_exists:
                self.sem.release()
                worker_log.debug(
                    "job %s already running elsewhere", job_id)
            else:
                pipe.multi()
                # pipe.setex(in_progress_key, int(10)) # secs
                pipe.set(in_progress_key, self.id)
                try:
                    await pipe.execute()
                except (ResponseError, WatchError):
                    self.sem.release()
                else:
                    t = self.loop.create_task(self.run_job(job_id, qname))
                    t.add_done_callback(lambda _: self.sem.release())
                    self.tasks[job_id] = t

    async def start_jobs(self, job_ids: List[str], qname: str):

        for job_id in job_ids:
            await self.start_job(job_id, qname)
            # in_progress_key = types.Prefixes.job_in_progress.value + job_id
            # await self.sem.acquire()
            # async with self.conn.pipeline(transaction=True) as pipe:
            #     await pipe.watch(in_progress_key)
            #     ongoing_exists = await pipe.exists(in_progress_key)
            #     if ongoing_exists:
            #         self.sem.release()
            #         worker_log.debug(
            #             "job %s already running elsewhere", job_id)
            #         continue
            #     pipe.multi()
            #     # pipe.setex(in_progress_key, int(10)) # secs
            #     pipe.set(in_progress_key, self.id)
            #     try:
            #         await pipe.execute()
            #     except (ResponseError, WatchError):
            #         self.sem.release()
            #     else:
            #         t = self.loop.create_task(self.run_job(job_id, qname))
            #         t.add_done_callback(lambda _: self.sem.release())
            #         self.tasks[job_id] = t

    async def call_func(self, payload: types.JobPayload) -> Any:
        func = get_function(payload.func_name)
        try:
            result = await func(**payload.params)
        except Exception as e:
            raise errors.FunctionCallError(payload.func_name, str(e))

        return result

    async def in_background(self, payload):
        func = get_function(payload.func_name)
        with concurrent.futures.ProcessPoolExecutor() as pool:
            try:
                result = await self.loop.run_in_executor(
                    pool,
                    func, **payload.params,
                )
            except Exception as e:
                raise errors.FunctionCallError(payload.func_name, str(e))
        return result

    async def run_job(self, job_id: str, qname: str):
        start_ms = datetime.utcnow().timestamp()
        worker_log.debug("Getting jobid %s from q %s", job_id, qname)
        job = Job(job_id, conn=self.conn)
        payload = await job.fetch()
        try:
            await job.mark_running()
            payload.started_ts = start_ms
            worker_log.debug(f"Doing {job_id}/{payload.func_name}")
            if payload.background:
                result = await self.in_background(payload)
            else:
                result = await self.call_func(payload)
            await job.mark_complete(result)
            worker_log.debug(f"Completed {job_id}/{payload.func_name}")
            self._completed += 1
        except (KeyError, errors.FunctionCallError) as e:
            await job.mark_failed({"error": str(e)})
            await self.conn.sadd(f"{types.Prefixes.queue_failed}{qname}", job_id)

        in_progress_key = types.Prefixes.job_in_progress.value + job_id
        await self.conn.delete(in_progress_key)

    def run(self):
        """
        Sync function to run the worker, finally closes worker connections.
        """
        worker_log.debug("Starting from sync")
        self.main_task = self.loop.create_task(self.main())
        try:
            self.loop.run_until_complete(self.main_task)
        except asyncio.exceptions.CancelledError as e:  # pragma: no cover
            # happens on shutdown, fine
            worker_log.debug(e)
        finally:
            self.loop.run_until_complete(self.close())

    async def async_run(self):

        self.main_task = self.loop.create_task(self.main())
        await self.main_task

    async def close(self):
        worker_log.debug("Closing %s", self.id)
        try:
            self.tasks["heartbeat"].cancel()
            del(self.tasks["heartbeat"])
            await self.unregister()
            await asyncio.gather(*self.tasks.values())
        except asyncio.CancelledError:
            pass
        await self.conn.close(close_connection_pool=True)
        worker_log.debug("Closed %s", self.id)

    def handle_sig(self, signum: Signals) -> None:
        sig = Signals(signum)
        # worker_log.info(
        #     'shutdown on %s ◆ %d jobs complete ◆ %d failed ◆ %d retries ◆ %d ongoing to cancel',
        #     sig.name,
        #     self.jobs_complete,
        #     self.jobs_failed,
        #     self.jobs_retried,
        #     len(self.tasks),
        # )
        worker_log.info("Shuting down worker %s", self.id)
        worker_log.debug(f"Pending jobs {self.tasks.values()}")
        for t in self.tasks.values():
            if not t.done():
                t.cancel()
        worker_log.debug("Cancelling main task")
        self.main_task and self.main_task.cancel()
        # self.on_stop and self.on_stop(sig)

    def _add_signal_handler(self, signum: Signals, handler: Callable[[Signals], None]) -> None:
        try:
            self.loop.add_signal_handler(signum, partial(handler, signum))
        except NotImplementedError:  # pragma: no cover
            worker_log.debug(
                'Windows does not support adding a signal handler to an eventloop')
