from rich.progress import *
from petpy.base.task import TaskInfo


class ProgressController:
    def __init__(self, on_update: callable = None, tasks: dict[int, TaskInfo] = None):
        self.onUpdate = on_update
        self.lock = RLock()
        self.tasks: dict[int, TaskInfo] = tasks or {}
        self.tasks.clear()  # 防止空字典被进行拷贝传递，因而需要清空
        self.onUpdate()

    @property
    def finished(self) -> bool:
        return all(task.stopped for task in self.tasks.values())

    def add_task(self, tid: int, total: int = 0, start: bool = False):
        task = TaskInfo(
            tid=tid,
            total=total,
        )
        if start:
            task.start()
        with self.lock:
            self.tasks[tid] = task
        if self.onUpdate is not None:
            self.onUpdate()

    def pop_task(self, tid: int):
        with self.lock:
            task = self.tasks[tid]
            task.interrupt()
            del self.tasks[tid]
        if self.onUpdate is not None:
            self.onUpdate()

    def start_task(self, tid: int):
        with self.lock:
            task = self.tasks[tid]
            task.start()
        if self.onUpdate is not None:
            self.onUpdate()

    def stop_task(self, tid: int):
        with self.lock:
            task = self.tasks[tid]
            task.interrupt()
        if self.onUpdate is not None:
            self.onUpdate()

    def finish_task(self, tid: int):
        with self.lock:
            task = self.tasks[tid]
            task.finish()
        if self.onUpdate is not None:
            self.onUpdate()

    def step(self, tid: int, advance: int = 1):
        with self.lock:
            task = self.tasks[tid]
            task.step(advance)
        if self.onUpdate is not None:
            self.onUpdate()

    def update(
            self,
            tid: int,
            total: int = None,
            steps: int = None,
            advance: int = None,
    ):
        with self.lock:
            task = self.tasks[tid]
            task.update(total, steps, advance)
        if self.onUpdate is not None:
            self.onUpdate()


def progress(start: int, end: int = None, step: int = 1):
    from petpy.console import PetPyConsole
    from petpy.utils.reporter import Reporter
    if end is None:
        end = start
        start = 0
    if PetPyConsole.instance:
        Reporter.setupProgress(end - start)
    for i in range(start, end, step):
        if PetPyConsole.instance:
            Reporter.step()
        yield i
