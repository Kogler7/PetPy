import sys

from petpy.base.task import TaskInfo
from petpy.controller.graphics import GraphicsController
from petpy.controller.progress import ProgressController

from petpy.handler.input import InputHandler
from petpy.handler.output import OutputHandler
from petpy.handler.command import CommandHandler


class PetPyConsole:
    isatty = None
    instance = None

    def __new__(cls):
        if cls.instance is None:
            start = cls.check_env()
            if start:
                cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.tasks: dict[int, TaskInfo] = {
            -1: TaskInfo(tid=-1, total=100),  # 防止空字典被进行拷贝传递，稍后会被清空
        }
        self.graphics = GraphicsController(
            tasks=self.tasks
        )
        self.progress = ProgressController(
            tasks=self.tasks,
            on_update=self.graphics.update_progress,
        )
        try:
            self.command = CommandHandler(
                console=self,
                update_command=self.graphics.update_command,
                update_tooltip=self.graphics.update_tooltip,
                on_refresh=self.graphics.refresh,
            )
            self.input = InputHandler(
                on_update=self.command.help,
                on_enter=self.command.handle,
            )
            self.output = OutputHandler()
        except Exception:
            self.graphics.print_exception()

    @classmethod
    def check_env(cls):
        cls.isatty = sys.stdout.isatty()
        if not cls.isatty:
            print(
                "The current environment does not support rich text output.\n\r"
                "All output will be printed in plain text.\n\r"
                "Please use a terminal instead.\n\r"
            )
        return cls.isatty
