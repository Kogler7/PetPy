import multiprocessing as mp
from queue import PriorityQueue

from petpy.console import Console
from petpy.base_task import TaskInfo, TaskEntity, TaskStatus
from petpy.rmi_proxy import RMIProxy, RMICallee, RMICaller
from petpy.reporter import Reporter


class Parallel:
    para_queue: PriorityQueue = PriorityQueue()
    instances: dict[int, "Parallel"] = {}

    def __new__(cls, processes: int = None, priority: int = 0):
        if cls.instances.get(priority) is None:
            instance = super().__new__(cls,  processes, priority)
            cls.instances[priority] = instance
            cls.para_queue.put((priority, instance))
        return cls.instances[priority]

    def __init__(self, processes: int = None, priority: int = 0):
        self.pool: mp.Pool = mp.Pool(self.processes)
        self.processes = processes
        self.priority = priority
        self.caller = Console.local_caller
        self.info_map = Console.task_info_map
        self.entities: dict[str, TaskEntity] = {}
        self.nr_running = 0

    def __del__(self):
        pass

    def start(self):
        for e in self.entities.values():
            info = self.info_map.get(e.tid)
            if info.status == TaskStatus.WAITING:
                info.status = TaskStatus.RUNNING
                self.nr_running += 1
                self.pool.apply_async(
                    Parallel.start_task,
                    (e, self.caller),
                    callback=Parallel.task_ended
                )
        self.pool.close()
        self.pool.join()

    @staticmethod
    def start_task(entity: TaskEntity, caller: RMICaller):
        Reporter(caller)
        entity.func(*entity.args, **entity.kwargs)

    @staticmethod
    def task_ended(task_id: str):
        pass

    def parallel(self, task: callable):

        def task_wrapper(args, **kwargs):
            info = TaskInfo(task.__name__, self.caller.pid, 0, 0, TaskStatus.WAITING, 0)
            entity = TaskEntity(task.__name__, task, args, kwargs)
            self.entities[entity.tid] = entity
            Reporter(self.listener.get_connection())
            self.pool.apply_async(task, args, kwargs)

        return task_wrapper
