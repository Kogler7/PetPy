from petpy.renderer.renderer import Renderer
from rich.text import Text
from rich.progress import RenderableType


class CommandRenderer(Renderer):
    def __init__(self, placeholder: str = 'Press "/" to type command.'):
        self.placeholder = Text(placeholder, style="yellow italic")
        self.command = self.placeholder

    def update(self, cmd: str, cursor_pos: int):
        if not cmd:
            self.command = self.placeholder
            return
        self.command = Text(cmd, style="white")
        if cursor_pos == len(cmd):
            self.command.append(" ", style="black on white")
        else:
            self.command.stylize("black on white", cursor_pos, cursor_pos + 1)

    def render(self) -> RenderableType:
        return self.command
