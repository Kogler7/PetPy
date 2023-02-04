import atexit
import os
import threading
import queue
import weakref
from abc import abstractmethod
from typing import Union

from petpy.base.task import Future, Task

_current_executor: Union["Executor", None] = None

_global_shutdown = False
_global_shutdown_lock = threading.Lock()
_global_thread_dict = weakref.WeakKeyDictionary()


def _python_exit():
    global _global_shutdown
    with _global_shutdown_lock:
        _global_shutdown = True
    items = list(_global_thread_dict.items())
    for t, q in items:
        q.put(None)
    for t, q in items:
        t.join()


atexit.register(_python_exit)


class Executor:
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
            self._console = None
        else:
            self._console = None
        self._show_console = show_console

    def __enter__(self):
        global _current_executor
        self._old_executor = _current_executor
        _current_executor = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _current_executor
        _current_executor = self._old_executor
        self.shutdown()

    def __del__(self):
        self.shutdown()


class ConcurrentExecutor(Executor):
    instances: dict[str, "ConcurrentExecutor"] = {}

    @staticmethod
    def get_instance(uid=''):
        return ConcurrentExecutor.instances.get(uid, None)

    def __new__(cls, max_workers: int, uid='', show_console=True):
        if uid in cls.instances:
            return cls.instances[uid]
        instance = super().__new__(cls)
        cls.instances[uid] = instance
        return instance

    def __init__(self, max_workers: int, uid='', show_console=True):
        super().__init__(max_workers, uid, show_console)
        self._idle_semaphore = threading.Semaphore(0)
        self._threads = set()

    def _worker(self):
        while True:
            _task = self._task_queue.get(block=True)
            if _task is not None:
                _task.bind_to_cur_worker()
                _task.run()
                self._idle_semaphore.release()
                continue
            if _global_shutdown or self._shutdown:
                self._task_queue.put(None)
                return

    def _try_new_thread(self):
        if self._idle_semaphore.acquire(timeout=0):
            return
        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            t = threading.Thread(target=self._worker)
            t.start()
            self._threads.add(t)
            _global_thread_dict[t] = self._task_queue

    def submit(self, task: Task):
        with self._shutdown_lock, _global_shutdown_lock:
            if self._shutdown:
                raise RuntimeError("cannot schedule new futures after shutdown")
            if _global_shutdown:
                raise RuntimeError("cannot schedule new futures after interpreter shutdown")
            self._task_count += 1
            task.no = self._task_count
            task.worker_type = "Thread"
            task.executor = self
            self._task_queue.put(task)
            self._try_new_thread()

    def shutdown(self, wait=True):
        self._shutdown = True
        self._task_queue.put(None)


def runnable(fn: callable):
    def wrapper(*args, **kwargs):
        _future = Future()
        _task = Task(_future, fn, args, kwargs)
        if _current_executor is not None:
            _current_executor.submit(_task)
        else:
            _task.run()
        return _future

    return wrapper
