from petpy.renderer.renderer import Renderer
from rich.text import Text
from rich.progress import RenderableType


class CommandRenderer(Renderer):
    def __init__(self, placeholder: str = "Type command here..."):
        self.placeholder = Text(placeholder, style="yellow italic")

    def update(self, args, kwargs):
        pass

    def render(self) -> RenderableType:
        return self.placeholder
