import os
import time
import threading

from rich.progress import *
from enum import Enum


class Future:
    def __init__(self):
        self._result = None
        self._exception = None
        self._done = False
        self._condition = threading.Condition()

    def set_result(self, result):
        with self._condition:
            self._result = result
            self._done = True
            self._condition.notify_all()

    def set_exception(self, exception):
        with self._condition:
            self._exception = exception
            self._done = True
            self._condition.notify_all()

    def result(self, timeout=None):
        with self._condition:
            if not self._done:
                self._condition.wait(timeout)
            if self._exception:
                raise self._exception
            return self._result

    def done(self):
        with self._condition:
            return self._done


class TaskStatus(Enum):
    WAITING = "WAI"  # Waiting to start, Grey
    RUNNING = "RUN"  # Running, Blue
    FINISHED = "FIN"  # Finished, Green
    SYNCHING = "SYN"  # Synching, Cyan
    SUSPENDED = "SUS"  # Suspended, Yellow
    INTERRUPTED = "INT"  # Interrupted, Red


class Task:
    worker_task_map: dict[str, "Task"] = {}

    @staticmethod
    def gene_worker_id():
        prc_id = os.getpid()
        thd_id = threading.currentThread().ident
        wrk_id = "%05d-%05d" % (prc_id, thd_id)
        return wrk_id

    @classmethod
    def get_cur_task(cls):
        wrk_id = cls.gene_worker_id()
        return cls.worker_task_map.get(wrk_id, None)

    def __init__(self, future: Future, fn: callable, args, kwargs):
        from executor import Executor
        self.future: Future = future
        self.fn: callable = fn
        self.no: int = 0
        self.id: str = ''
        self.executor: Executor
        self.worker_id: str = '0-0'
        self.worker_type: Union[str, None] = None
        self.args = args
        self.kwargs = kwargs

    def bind_to_cur_worker(self):
        self.worker_id = self.gene_worker_id()
        self.worker_task_map[self.worker_id] = self
        return self

    def run(self):
        if self.future is None:
            self.fn(*self.args, **self.kwargs)
            return

        try:
            result = self.fn(*self.args, **self.kwargs)
        except BaseException as exc:
            self.future.set_exception(exc)
        else:
            self.future.set_result(result)


@dataclass
class TaskInfo:
    tid: int
    steps: int = 0
    total: int = 0
    speed: float = 0
    status: TaskStatus = TaskStatus.WAITING
    time_last_start: float = 0
    time_accumulated: float = 0
    lock: RLock = field(repr=False, default_factory=RLock)

    @property
    def cycle(self) -> float:
        """Time spent in each step."""
        if not self.speed:
            return 0.0
        return 1.0 / self.speed

    @property
    def waiting(self) -> bool:
        """True if task is waiting."""
        return self.status == TaskStatus.WAITING

    @property
    def running(self) -> bool:
        """True if task is running."""
        return self.status == TaskStatus.RUNNING or self.status == TaskStatus.SYNCHING

    @property
    def suspended(self) -> bool:
        """True if task is suspended."""
        return self.status == TaskStatus.SUSPENDED

    @property
    def stopped(self) -> bool:
        """True if task is stopped."""
        return self.status == TaskStatus.FINISHED or self.status == TaskStatus.INTERRUPTED

    @property
    def percentage(self) -> float:
        """Percentage completed, between 0.0 and 100.0."""
        if not self.total:
            return 0.0
        completed = (self.steps / self.total) * 100.0
        completed = min(100.0, max(0.0, completed))
        return completed

    @property
    def time_elapsed(self) -> float:
        """Time elapsed in seconds."""
        if self.status == TaskStatus.WAITING:
            return 0
        if self.running:
            return time.time() - self.time_last_start + self.time_accumulated
        return self.time_accumulated

    @property
    def time_remaining(self) -> Optional[float]:
        """Time remaining in seconds."""
        if self.speed == 0:
            return None
        return (self.total - self.steps) / self.speed

    def start(self):
        with self.lock:
            if self.status == TaskStatus.WAITING:
                self.status = TaskStatus.RUNNING
                self.time_last_start = time.time()

    def step(self, advance: int = 1):
        with self.lock:
            if self.status == TaskStatus.RUNNING:
                elapsed = max(0.001, time.time() - self.time_last_start)
                self.steps += advance
                self.speed = advance / elapsed
                self.time_last_start = time.time()
                self.time_accumulated += elapsed
                if self.steps >= self.total:
                    self.status = TaskStatus.FINISHED

    def update(self, total: int = None, steps: int = None, advance: int = None):
        with self.lock:
            if total is not None:
                self.total = total
            if steps is not None:
                self.steps = steps
            if advance is not None:
                self.step(advance)

    def suspend(self):
        with self.lock:
            if self.running:
                self.status = TaskStatus.SUSPENDED
                self.time_accumulated += time.time() - self.time_last_start

    def resume(self):
        with self.lock:
            if self.suspended:
                self.status = TaskStatus.RUNNING
                self.time_last_start = time.time()

    def interrupt(self):
        with self.lock:
            if self.running:
                self.status = TaskStatus.INTERRUPTED
                self.time_accumulated += time.time() - self.time_last_start

    def sync(self, advance: int = 1):
        """Not well implemented yet."""
        with self.lock:
            if self.status == TaskStatus.RUNNING:
                self.status = TaskStatus.SYNCHING
            self.steps += advance

    def finish(self):
        with self.lock:
            if self.running:
                self.status = TaskStatus.FINISHED
                self.time_accumulated += time.time() - self.time_last_start
                self.steps = self.total
