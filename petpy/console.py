import time

from controller.graphics import GraphicsController
from controller.progress import ProgressController
from handler.command import CommandHandler
from handler.input import InputHandler
from handler.output import OutputHandler


class PetPyConsole:
    def __init__(self):
        self.graphics = GraphicsController()


if __name__ == '__main__':
    console = PetPyConsole()
    progress = console.graphics.progress
    progress.add_task(tid=1, total=500, start=True)
    progress.add_task(tid=2, total=1000, start=True)
    progress.add_task(tid=3, total=200, start=True)
    while not progress.finished:
        progress.step(1)
        progress.step(2, 10)
        progress.step(3)
        time.sleep(0.1)
