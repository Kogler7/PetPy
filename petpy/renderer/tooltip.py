from petpy.renderer.renderer import Renderer
from rich.text import Text
from rich.progress import RenderableType


class TooltipRenderer(Renderer):
    def __init__(self, placeholder: str = " : help"):
        self.placeholder = Text(placeholder, style="yellow blink")

    def update(self, args, kwargs):
        pass

    def render(self) -> RenderableType:
        return self.placeholder
