from petpy.executor.executor import *


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
                if Executor.progress:
                    Executor.progress.start_task(_task.tid)
                _task.run()
                if Executor.progress:
                    Executor.progress.finish_task(_task.tid)
                self._idle_semaphore.release()
                continue
            if global_shutdown or self._shutdown:
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
            global_thread_dict[t] = self._task_queue

    def submit(self, task: Task):
        with self._shutdown_lock, global_shutdown_lock:
            if self._shutdown:
                raise RuntimeError("cannot schedule new futures after shutdown")
            if global_shutdown:
                raise RuntimeError("cannot schedule new futures after interpreter shutdown")
            self._task_count += 1
            task.no = self._task_count
            task.worker_type = "Thread"
            task.executor = self
            if Executor.progress:
                Executor.progress.add_task(task.tid, start=False)
            self._task_queue.put(task)
            self._try_new_thread()

    def shutdown(self, wait=True):
        self._shutdown = True
        self._task_queue.put(None)


def concurrent(fn: callable = None, max_workers: int = None, uid: str = '', show_console=True):
    if fn is not None:
        def wrapper():
            with ConcurrentExecutor(max_workers, uid, show_console):
                fn()

        return wrapper

    def wrapper(_fn: callable):
        def inner(*args, **kwargs):
            with ConcurrentExecutor(max_workers, uid, show_console):
                _fn(*args, **kwargs)

        return inner

    return wrapper
