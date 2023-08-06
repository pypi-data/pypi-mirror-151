from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class Prefixes(Enum):
    ns = "sq"
    job = "sq:job::"
    job_in_progress = "sq:job:running::"
    # queue = "sq:q::"
    # queue_info = "sq:q:info::"
    queue_jobs = "sq:q:jobs::"
    queue_running = "sq:q:running::"
    queue_cancelled = "sq:q:cancelled::"
    queue_failed = "sq:q:failed::"
    queue_complete = "sq:q:complete::"
    queue_workers = "sq:q:workers::"
    queues_list = "sq:q:queues"
    worker = "sq:w::"
    workers_list = "sq:workers"
    worker_commands = "sq:w:cmd::"


class JobStatus(Enum):
    not_found = -1
    created = 0
    queued = 1
    running = 2
    canceled = 3
    failed = 4
    complete = 5


class JobResult(BaseModel):
    execid: str
    func_name: str
    success: bool
    status: str
    qname: str
    elapsed: float
    started_ts: Optional[float] = None
    func_result: Optional[Dict[str, Any]] = None


class JobPayload(BaseModel):
    func_name: str
    timeout: int
    background: bool = False
    params: Dict[str, Any] = {}
    result_ttl: int = 60 * 5
    status: int
    queue: str
    enqueued_ts: float
    max_retry: int = 3
    retries: int = 0
    started_ts: Optional[float] = None
    job_result: Optional[JobResult] = None


class JobRef(BaseModel):
    execid: str
    qname: str


class WorkerInfo(BaseModel):
    id: str
    birthday: str
    queues: List[str]
    completed: int
    failed: int
    running: int
