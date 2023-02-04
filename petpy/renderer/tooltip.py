from petpy.renderer.renderer import Renderer
from rich.text import Text
from rich.progress import RenderableType


class TooltipRenderer(Renderer):
    def __init__(self):
        self.base = Text(" > ", style="white")
        self.tooltip = Text("")

    def update(self, tip: str, match_strs: list[str]):
        if tip:
            self.tooltip = Text(tip, style="white")
        for match_str in match_strs:
            match_start = tip.find(match_str)
            match_end = match_start + len(match_str)
            self.tooltip.stylize("yellow", match_start, match_end)

    def render(self) -> RenderableType:
        return self.base + self.tooltip
