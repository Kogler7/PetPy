from abc import ABC, abstractmethod
from rich.progress import RenderableType


class Renderer(ABC):
    @abstractmethod
    def update(self, args, kwargs):
        pass

    @abstractmethod
    def render(self) -> RenderableType:
        pass
