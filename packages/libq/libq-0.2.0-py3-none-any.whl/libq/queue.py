import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Union

from libq import defaults, errors, serializers
from libq.connections import Driver, create_pool
from libq.jobs import Job
from libq.types import JobPayload, JobRef, JobStatus, Prefixes
from libq.utils import generate_random, parse_timeout
from libq.worker import AsyncWorker


class Queue:

    def __init__(self, name: str, *,
                 conn: Optional[Driver] = None,
                 default_timeout=None,
                 queue_wait_ttl=None,
                 is_async=True):
        self._name = name
        self._default_timeout = parse_timeout(
            default_timeout) or defaults.QUEUE_TIMEOUT
        self.conn = conn
        self._queue_wait_ttl = defaults.QUEUE_WAIT_TTL
        self._is_async = is_async

    @property
    def name(self) -> str:
        _prefix = Prefixes.queue_jobs.value
        return f"{_prefix}{self._name}"

    async def _send_job(self, id: str, payload: JobPayload):
        async with self.conn.pipeline() as pipe:
            pipe.sadd(Prefixes.queues_list.value, self.name)
            pipe.setex(f"{Prefixes.job.value}{id}",
                       self._queue_wait_ttl, payload.json())
            # pipe.hset(f"{self.q_info}", mapping={"last_job": enqueued})
            pipe.rpush(self.name, id)
            result = await pipe.execute()
        return result

    async def enqueue(self,
                      func_name, *,
                      params: Dict[str, Any] = {},
                      timeout=None,
                      result_ttl=60 * 5,
                      background=False,
                      queue_wait_ttl=None,
                      desc=None, execid=None) -> Job:

        id = execid or generate_random()
        ts = parse_timeout(timeout) or self._default_timeout

        _now = datetime.utcnow().timestamp()
        status = JobStatus.queued.value

        payload = JobPayload(
            func_name=func_name,
            timeout=ts,
            background=background,
            params=params,
            result_ttl=result_ttl,
            status=status,
            enqueued_ts=_now,
            queue=self._name
        )
        await self._send_job(id, payload)

        return Job(id, conn=self.conn, payload=payload)

    async def list_enqueued(self, start="0", end="-1") -> List[str]:
        return await self.conn.lrange(self.name, start, end)

    async def list_workers(self) -> Set[str]:
        # print(f"{Prefixes.queue_workers.value}{self.name}")
        workers = await self.conn.sinter(
            f"{Prefixes.queue_workers.value}{self._name}")
        return workers

    async def send_command(self, cmd: str, *, key=None, public: str = "all"):
        key = key or generate_random()
        channel = f"{Prefixes.queues_commands.value}{self._name}"
        msg = serializers.command_serializer(cmd, key=key, public=public)
        await self.conn.publish(channel, msg)
        return key

    def get_worker(self, worker_id) -> AsyncWorker:
        return AsyncWorker(self._name, conn=self.conn, id=worker_id)
