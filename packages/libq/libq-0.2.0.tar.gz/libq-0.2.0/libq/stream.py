import asyncio
import random
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional

from redis.asyncio import ConnectionPool, Redis
from redis.exceptions import RedisError, ResponseError, WatchError

from libq import defaults, types
from libq.connections import RedisSettings, StreamRedis
from libq.jobs import Job
from libq.logs import worker_log
from libq.utils import generate_random, parse_timeout, poll


class StreamWorker:

    def __init__(self, *,
                 streams=[defaults.STREAM_NAME],
                 group_name=defaults.GROUP_NAME,
                 redis_settings: RedisSettings,
                 redis_pool: StreamRedis = None,
                 identity=None,
                 ):
        if streams is None:
            if redis_pool is not None:
                streams = [redis_pool.default_queue_name]
            else:
                raise ValueError(
                    'If queue_name is absent, redis_pool must be present.')

        self.identity = identity or generate_random()
        self._pool = redis_pool
        self.streams = streams
        self.group_name = group_name

    async def create_stream_group(self, create_stream=True, from_id="$"):
        for s in self.streams:
            res = await self._pool.xgroup_create(
                s, self.group_name, id=from_id, mkstream=create_stream)
        return res

    async def read(self, block_timeout=0, count=1, lastid="$"):
        streams = {s: lastid for s in self.streams}
        res = await self._pool.xread(streams, count=count, block=block_timeout)
        return res

    async def readgroup(self, count=1, lastid=">"):
        streams = {s: lastid for s in self.streams}
        res = await self._pool.xreadgroup(self.group_name, self.identity, streams, count)
