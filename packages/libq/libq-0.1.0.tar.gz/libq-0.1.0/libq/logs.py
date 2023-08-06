import logging
from rich.logging import RichHandler

# FORMAT = "%(message)s"
# logging.basicConfig(
#     level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)]
# )


worker_log = logging.getLogger("streamq.worker")
queue_log = logging.getLogger("streamq.queue")
