import multiprocessing as mp
import threading as th

from petpy.reporter import Reporter
from petpy.listener import Listener
from petpy.connect import Connection


class Parallel:
    instances: dict[int] = {}
    listener: Listener = Listener()

    def __new__(cls, processes: int = None, priority: int = 0):
        unique_key = f"{priority}-{processes}"
        if cls.instances.get(unique_key) is None:
            instance = super().__new__(cls,  processes, priority)
            cls.instances[unique_key] = instance
        return cls.instances[unique_key]

    def __init__(self, processes: int = None, priority: int = 0):
        self.pool = mp.Pool(self.processes)
        self.in_service = False
        self.priority = priority
        self.processes = processes
        self.host_conn = Connection()
        self.reporter = Reporter(self.host_conn)
        
    def __del__(self):
        pass

    def start_service(self):
        self.in_service = True
        th.Thread(target=self.listener.start_listening).start()

    def parallel(self, task: callable):
        if not self.in_service:
            self.start_service()

        def task_wrapper(args, **kwargs):
            Reporter(self.listener.get_connection())
            self.pool.apply_async(task, args, kwargs)

        return task_wrapper
