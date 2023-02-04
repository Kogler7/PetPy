from petpy.base.task import Task


class Reporter:
    @staticmethod
    def print(*args, sep=' ', end='\n'):
        task = Task.get_cur_task()
        if task is not None:
            print(f"[{task.no}]", *args, sep=sep, end=end)
        else:
            print(*args, sep=sep, end=end)

    @staticmethod
    def setupProgress(total: int):
        from petpy.console import PetPyConsole
        from petpy.controller.progress import ProgressController
        progress: ProgressController = PetPyConsole.instance.progress
        task = Task.get_cur_task()
        if task is not None:
            progress.update(task.tid, total=total)

    @staticmethod
    def step(advance: int = 1):
        from petpy.console import PetPyConsole
        from petpy.controller.progress import ProgressController
        progress: ProgressController = PetPyConsole.instance.progress
        task = Task.get_cur_task()
        if task is not None:
            progress.step(task.tid, advance)

    @staticmethod
    def table(data: list, header: list = None):
        raise NotImplementedError


def report(*args, sep=' ', end='\n'):
    task = Task.get_cur_task()
    # if task is not None:
    #     print(f"[{task.no}]", *args, sep=sep, end=end)
    # else:
    #     print(*args, sep=sep, end=end)
