import time

from petpy.base.task import TaskInfo
from petpy.controller.graphics import GraphicsController
from petpy.controller.progress import ProgressController

from petpy.handler.input import InputHandler
from petpy.handler.output import OutputHandler
from petpy.handler.command import CommandHandler


class PetPyConsole:
    def __init__(self):
        self.tasks: dict[int, TaskInfo] = {
            0: TaskInfo(tid=0, total=100),  # 防止空字典被进行拷贝传递，稍后会被清空
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
