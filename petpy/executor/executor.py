import atexit
import os
import threading
import queue
import weakref
from abc import abstractmethod
from typing import Union

from petpy.base.task import Future, Task
from petpy.console import PetPyConsole
from petpy.controller.progress import ProgressController

global_shutdown = False
global_shutdown_lock = threading.Lock()
global_thread_dict = weakref.WeakKeyDictionary()


def _python_exit():
    global global_shutdown
    with global_shutdown_lock:
        global_shutdown = True
    items = list(global_thread_dict.items())
    for t, q in items:
        q.put(None)
    for t, q in items:
        t.join()


atexit.register(_python_exit)


class Executor:
    current_executor: Union["Executor", None] = None
    progress: ProgressController = None
    console: PetPyConsole = None

    @abstractmethod
    def submit(self, task: Task) -> Future:
        raise NotImplementedError

    @abstractmethod
    def shutdown(self, wait=True):
        raise NotImplementedError

    def __init__(self, max_workers=None, uid: str = '', show_console=True):
        if max_workers is None:
            max_workers = os.cpu_count() or 1
        self._uid = uid
        self._task_count = 0
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._max_workers = max_workers
        self._task_queue = queue.SimpleQueue()
        if show_console:
            Executor.console = PetPyConsole()
            if Executor.console:
                Executor.progress = Executor.console.progress
            else:
                raise RuntimeError("Create progress controller failed.")
        self._show_console = show_console

    def __enter__(self):
        self._old_executor = Executor.current_executor
        Executor.current_executor = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Executor.current_executor = self._old_executor
        self.shutdown()

    def __del__(self):
        self.shutdown()
