from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    WAITING = "WAI"
    RUNNING = "RUN"
    FINISHED = "FIN"
    SYNCHING = "SYN"
    SUSPENDED = "SUS"
    INTERRUPTED = "INT"


@dataclass
class TaskInfo:
    tid: str
    pid: str
    step: int
    total: int
    status: TaskStatus
    elapsed: float


@dataclass
class TaskEntity:
    tid: str
    func: callable
    args: tuple
    kwargs: dict
