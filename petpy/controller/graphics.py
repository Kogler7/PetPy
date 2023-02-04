from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.live import Live

from petpy.renderer import Renderer, CommandRenderer, TooltipRenderer


class GraphicsController:
    def __init__(self):
        self.layout = Layout()
        self.console = Console()
        self.live = Live(
            self.layout,
            screen=True,
            redirect_stderr=False,
            console=self.console,
            auto_refresh=True,
            refresh_per_second=10,
        )
        self.tooltip: TooltipRenderer = TooltipRenderer()
        self.command: CommandRenderer = CommandRenderer()
        self.setupLayout()
        self.live.start()

    def update(self, target: str, renderer: Renderer):
        self.layout[target].update(renderer.render())
        self.refresh()

    def refresh(self):
        self.live.refresh()

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
