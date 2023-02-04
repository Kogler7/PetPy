import time
from abc import ABC, abstractmethod

from petpy.renderer.renderer import Renderer
from petpy.base.task import TaskInfo, TaskStatus
from rich.text import Text
from rich.box import HORIZONTALS
from rich.table import Table
from rich.progress import RenderableType
from rich.progress_bar import ProgressBar


class TaskInfoColumn(ABC):
    def __init__(self, name: str, justify: str = "left", style: str = ""):
        self.name = name
        self.justify = justify
        self.style = style

    @abstractmethod
    def render(self, task: TaskInfo) -> RenderableType:
        pass


class TaskIDColumn(TaskInfoColumn):
    def __init__(self, name: str = "ID", justify: str = "right", style: str = ""):
        super().__init__(name, justify, style)

    def render(self, task: TaskInfo) -> RenderableType:
        return Text(str(task.tid))


class TaskStatusColumn(TaskInfoColumn):
    def __init__(self, name: str = "Status", justify: str = "right", style: str = ""):
        super().__init__(name, justify, style)

    def render(self, task: TaskInfo) -> RenderableType:
        text = f"[{task.status.value}]"
        style = ""
        if task.status == TaskStatus.WAITING:
            style = "grey"
        elif task.status == TaskStatus.RUNNING:
            style = "cyan"
        elif task.status == TaskStatus.FINISHED:
            style = "green"
        elif task.status == TaskStatus.SYNCHING:
            style = "blue"
        elif task.status == TaskStatus.SUSPENDED:
            style = "yellow"
        elif task.status == TaskStatus.INTERRUPTED:
            style = "red"
        return Text(text, style=style)


class TaskPercentageColumn(TaskInfoColumn):
    def __init__(self, name: str = "   Percentage", justify: str = "left", style: str = ""):
        super().__init__(name, justify, style)

    def render(self, task: TaskInfo) -> RenderableType:
        per = f"{task.percentage:.1f}".rjust(5)
        return Text(f"{per}% [{task.steps}/{task.total}]")


class TaskProgressColumn(TaskInfoColumn):
    def __init__(self, name: str = "Progress", justify: str = "center", style: str = ""):
        super().__init__(name, justify, style)

    def render(self, task: TaskInfo) -> RenderableType:
        return ProgressBar(
            completed=task.steps,
            total=task.total,
            pulse=task.waiting,
        )


class TaskTimingColumn(TaskInfoColumn):
    def __init__(self, name: str = "Timing", justify: str = "center", style: str = ""):
        super().__init__(name, justify, style)

    def render(self, task: TaskInfo) -> RenderableType:
        elapsed = time.gmtime(task.time_elapsed)
        remaining = task.time_remaining
        if elapsed.tm_hour > 0:
            elapsed = time.strftime("%H:%M:%S", elapsed)
        else:
            elapsed = time.strftime("%M:%S", elapsed)
        if remaining is None:
            remaining = "∞:∞"
        else:
            remaining = time.gmtime(remaining)
            if remaining.tm_hour > 0:
                remaining = time.strftime("%H:%M:%S", remaining)
            else:
                remaining = time.strftime("%M:%S", remaining)
        return Text(f"<{elapsed}/{remaining}> ({task.cycle:.2f}s/it)")


class ProgressRenderer(Renderer):
    def __init__(self, tasks: dict[int, TaskInfo]):
        self.header = "Task Status"
        self.tasks: dict[int, TaskInfo] = tasks
        self.columns = (
            TaskIDColumn(),
            TaskStatusColumn(),
            TaskPercentageColumn(),
            TaskProgressColumn(),
            TaskTimingColumn(),
        )

    def update(self, *args, **kwargs):
        pass

    def render(self):
        table = Table(
            title="Tasks Status",
            expand=True,
            box=HORIZONTALS,
        )
        for column in self.columns:
            table.add_column(column.name, justify=column.justify, style=column.style)
        for task in self.tasks.values():
            table.add_row(*[column.render(task) for column in self.columns])
        return table
