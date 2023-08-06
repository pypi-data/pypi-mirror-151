import asyncio
import concurrent.futures
import random
import signal
from copy import deepcopy
from dataclasses import asdict
from functools import partial
from signal import Signals
from typing import Any, Callable, Coroutine, Dict, List, Optional

# from redis.asyncio import ConnectionPool, Redis
from redis.exceptions import ResponseError, WatchError

from libq import defaults, errors, serializers, types
from libq.connections import Driver, create_pool
from libq.jobs import Job
from libq.logs import logger
from libq.utils import (
    elapsed_from,
    generate_random,
    get_function,
    now_iso,
    now_secs,
    parse_timeout,
    poll,
)


class AsyncWorker:

    def __init__(self, queues: str,
                 *,
                 conn=None,
                 id=None,
                 ctx=Optional[Dict[str, Any]],
                 max_jobs=defaults.WORKER_MAX_JOBS,
                 heartbeat_secs=defaults.WORKER_HEARTBEAT_REFRESH,
                 poll_delay_secs=None,
                 poll_strategy="blocking",
                 handle_signals: bool = True,
                 ):
        """
        Async worker

        :param conn: A Redis connection
        :param queues: A List of queues names to listen to
        :param id: an identifier for this worker
        :param ctx: Not implemented yet but it allows to gives optionals objs
        :param max_jobs: how many jobs running concurrently
        :param heartbeat_secs: how often notify to redis that we are alive
        :param poll_delay_secs: how much will be waiting for messages from redis
        :param poll_strategy: there are two options; blocking a iteration. 

        """

        self.conn: Driver = conn
        self.id = id or generate_random()
        self.loop = asyncio.get_event_loop()
        self.ctx = ctx or {}
        self.tasks: Dict[str, asyncio.Task[Any]] = {}
        self.main_task: Optional[asyncio.Task[None]] = None
        self._queues = queues.split(",")
        self.queues = [
            f"{types.Prefixes.queue_jobs.value}{q}" for q in self._queues]
        self.sem = asyncio.BoundedSemaphore(max_jobs)
        self._max_jobs = max_jobs
        self.poll_delay_s = parse_timeout(
            poll_delay_secs) or defaults.WORKER_POLL_DELAY
        self.poll_strategy = poll_strategy

        self.heartbeat_refresh = parse_timeout(heartbeat_secs)
        self._handle_signals = handle_signals
        if self._handle_signals:
            self._add_signal_handler(signal.SIGINT, self.handle_sig)
            self._add_signal_handler(signal.SIGTERM, self.handle_sig)

        self.sub = None

        self.birthday: str = now_iso()
        self.last_job: str = now_iso()
        self.idle_secs = .0

        self._completed = 0
        self._failed = 0

    def create_task(self, key: str, func: Coroutine):
        """ creates an async task into the loop """
        t = self.loop.create_task(func)
        self.tasks[key] = t

    def cancel_task(self, key):
        self.tasks[key].cancel()
        del self.tasks[key]

    async def register(self):
        """ Self Register, used in the heartbeat cycle """
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
            logger.debug("Heartbeating...")
            await self.register()

        logger.debug("Heartbeat stopped")

    # async def send_command(self, cmd) -> int:
    #     key = f"{types.Prefixes.worker_commands.value}{self.id}"
    #     r = await self.conn.rpush(key, cmd)
    #     return r

    async def run_cmd(self, cmd: types.Command):
        if cmd.public == "all" or cmd.public == self.id:
            if cmd.action == "shutdown":
                self.handle_sig(Signals.SIGINT)
            else:
                logger.warning("Command not supported")

    async def commands(self):
        logger.info("Listening for commands")
        for q in self._queues:
            await self.sub.subscribe(f"{types.Prefixes.queues_commands.value}{q}")

        async for _msg in self.sub.listen():
            msg = types.PubSubMsg(**_msg)
            if msg.type == "message":
                cmd = serializers.command_deserializer(msg.data)
                if cmd.public == "all" or cmd.public == self.id:
                    logger.debug(
                        f"Command {cmd.action} for {cmd.public} with {cmd.key}")
                    if cmd.action == "shutdown":
                        self.handle_sig(Signals.SIGINT)
                        continue
                    else:
                        logger.warning("Command not supported")

                    # self.create_task(cmd.key, self.run_cmd(cmd))
        # key = f"{types.Prefixes.worker_commands.value}{self.id}"
        # async for _ in poll(self.heartbeat_refresh + 2):
        #     cmd = await self.conn.lpop(key, 1)
        #     if cmd:
        #         logger.debug(f"===> cmd: {cmd}")
        #         if cmd[0] == "shutdown":
        #             self.handle_sig(Signals.SIGINT)
        #             continue

    async def main(self):
        if not self.conn:
            self.conn = await create_pool()

        self.sub = self.conn.pubsub()
        logger.info(f"Starting worker {self.id}")
        logger.debug(f"Queues to listen {self.queues}")
        self.create_task("heartbeat", self.heartbeat())
        self.create_task("commands", self.commands())

        if self.poll_strategy == "blocking":
            while True:
                await self._poll_blocking()
        else:
            async for _ in poll(self.poll_delay_s):  # noqa F841
                await self._poll_iteration()

        logger.debug("Finished main %s", self.id)

    async def _poll_blocking(self):
        """ Difference than poll_iteration, it will listen to all queues
        but it only recieves one message. """
        keys = deepcopy(self.queues)
        random.shuffle(keys)
        async with self.sem:
            logger.debug(f"Waiting new jobs for {self.poll_delay_s} secs")
            task = await self.conn.blpop(keys, self.poll_delay_s)
            if task:
                logger.debug(
                    f"Job: {task[1:]} from queue {task[0]}")

        if task:
            _queue = task[0]
            _job = task[1]
            self.last_job = now_iso()
            await self.start_job(_job, _queue)
        else:
            logger.debug("No jobs found")
            last = elapsed_from(self.last_job)
            self.idle_secs += last

        for job_id, t in list(self.tasks.items()):
            if t.done():
                del self.tasks[job_id]
                t.result()

    async def _poll_iteration(self):
        q = random.choice(self.queues)
        async with self.sem:
            count = self._max_jobs - self.sem._value
            tasks = await self.conn.lpop(q, count)
        if tasks:
            self.last_job = now_iso()
            await self.start_jobs(tasks, q)
        else:
            logger.debug("[yellow]No jobs found[/]", extra={"markdown": True})
            last = elapsed_from(self.last_job)
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
                logger.debug(
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
        await asyncio.gather(
            [self.start_job(jid, qname)
             for jid in job_ids],
            return_exceptions=True
        )

    async def call_func(self, payload: types.JobPayload) -> types.FunctionResult:

        result = types.FunctionResult(error=False)
        try:
            func = get_function(payload.func_name)
        except KeyError:
            result.error = True
            result.error_msg = f"func {payload.func_name} not found"
            return result
        try:
            _result = await asyncio.wait_for(func(**payload.params), payload.timeout)
            result.func_result = _result
        except (Exception, asyncio.CancelledError) as e:
            result.error = True
            result.error_msg = f"func {payload.func_name} failed or timeouted with {e}"

        return result

    async def call_func_bg(self, payload) -> types.FunctionResult:

        result = types.FunctionResult(error=False)
        try:
            func = get_function(payload.func_name)
        except KeyError:
            result.error = True
            result.error_msg = f"func {payload.func_name} not found"
            return result
        with concurrent.futures.ProcessPoolExecutor() as pool:
            try:
                _result = await asyncio.wait_for(self.loop.run_in_executor(
                    pool, partial(func, **payload.params)), payload.timeout)
                result.func_result = _result
            except (Exception, asyncio.CancelledError) as e:
                result.error = True
                result.error_msg = f"func {payload.func_name} failed or timeouted with {e}"

        return result

    async def run_job(self, job_id: str, qname: str):
        start_ms = now_secs()
        logger.debug("Getting jobid %s from q %s", job_id, qname)
        job = Job(job_id, conn=self.conn)
        payload = await job.fetch()
        try:
            await job.mark_running()
            payload.started_ts = start_ms
            logger.debug(f"Doing {job_id}/{payload.func_name}")
            if payload.background:
                result = await self.call_func_bg(payload)
            else:
                result = await self.call_func(payload)
            if not result.error:
                await job.mark_complete(result.func_result)
                logger.debug(f"Completed {job_id}/{payload.func_name}")
                self._completed += 1
            else:
                await job.mark_failed(asdict(result))
                self._failed += 1
                await self.conn.sadd(f"{types.Prefixes.queue_failed.value}{qname}", job_id)
        except Exception as e:
            # last catch if something faild
            await job.mark_failed({"error": str(e)})
            self._failed += 1
            await self.conn.sadd(f"{types.Prefixes.queue_failed.value}{qname}", job_id)

        in_progress_key = types.Prefixes.job_in_progress.value + job_id
        await self.conn.delete(in_progress_key)

    def run(self):
        """
        Sync function to run the worker, finally closes worker connections.
        """
        logger.debug("Starting from sync")
        self.main_task = self.loop.create_task(self.main())
        try:
            self.loop.run_until_complete(self.main_task)
        except asyncio.exceptions.CancelledError as e:  # pragma: no cover
            # happens on shutdown, fine
            logger.debug(e)
        finally:
            self.loop.run_until_complete(self.close())

    async def async_run(self):

        self.main_task = self.loop.create_task(self.main())
        await self.main_task

    async def close(self):
        logger.debug("Closing %s", self.id)
        try:
            self.cancel_task("heartbeat")
            self.cancel_task("commands")
            for q in self._queues:
                await self.sub.unsubscribe()
            await self.unregister()
            await asyncio.gather(*self.tasks.values())
        except asyncio.CancelledError:
            pass
        await self.conn.close(close_connection_pool=True)
        logger.debug("Closed %s", self.id)

    def handle_sig(self, signum: Signals) -> None:
        sig = Signals(signum)
        # logger.info(
        #     'shutdown on %s ◆ %d jobs complete ◆ %d failed ◆ %d retries ◆ %d ongoing to cancel',
        #     sig.name,
        #     self.jobs_complete,
        #     self.jobs_failed,
        #     self.jobs_retried,
        #     len(self.tasks),
        # )
        logger.info("Shuting down worker %s", self.id)
        logger.debug(f"Pending jobs {self.tasks.values()}")
        for t in self.tasks.values():
            if not t.done():
                t.cancel()
        logger.debug("Cancelling main task")
        self.main_task and self.main_task.cancel()
        # self.on_stop and self.on_stop(sig)

    def _add_signal_handler(self, signum: Signals, handler: Callable[[Signals], None]) -> None:
        try:
            self.loop.add_signal_handler(signum, partial(handler, signum))
        except NotImplementedError:  # pragma: no cover
            logger.debug(
                'Windows does not support adding a signal handler to an eventloop')
