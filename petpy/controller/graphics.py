from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.live import Live

from petpy.base.task import TaskInfo
from petpy.renderer.command import CommandRenderer
from petpy.renderer.tooltip import TooltipRenderer
from petpy.renderer.progress import ProgressRenderer


class GraphicsController:
    def __init__(self, tasks: dict[int, TaskInfo]):
        self.tasks = tasks
        self.layout = Layout()
        self.console = Console()
        self.live = Live(
            self.layout,
            screen=True,
            redirect_stderr=False,
            console=self.console,
            auto_refresh=True,
            refresh_per_second=4,
        )
        self.tooltip: TooltipRenderer = TooltipRenderer()
        self.command: CommandRenderer = CommandRenderer()
        self.progress: ProgressRenderer = ProgressRenderer(self.tasks)
        self.setupLayout()
        self.live.start()

    def update_progress(self):
        self.layout["main"].update(self.progress.render())
        self.refresh()

    def update_command(self, cmd: str, cursor_pos: int):
        self.command.update(cmd, cursor_pos)
        self.layout["command"].update(
            Panel(self.command.render(), border_style="white")
        )

    def update_tooltip(self, tip: str, match_strs: list[str]):
        self.tooltip.update(tip, match_strs)
        self.layout["tooltip"].update(self.tooltip.render())

    def refresh(self):
        self.live.refresh()

    def print_exception(self):
        self.live.stop()
        self.console.print_exception()

    def setupLayout(self):
        self.layout.split(
            Layout(name="header", size=2),
            Layout(name="main", ratio=1),
            Layout(name="tooltip", size=1),
            Layout(name="command", size=3),
        )

        self.layout["header"].split_row(
            Layout(name="title", ratio=3),
            Layout(name="version", ratio=1),
        )

        self.layout["title"].update(Align.left(Text("PetPy Console", style="bold yellow")))
        self.layout["version"].update(Align.right(Text("v0.0.1", style="bold yellow")))

        self.layout["tooltip"].update(self.tooltip.render())

        self.layout["command"].update(
            Panel(self.command.render(), border_style="white")
        )
