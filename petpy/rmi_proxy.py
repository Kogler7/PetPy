# (Queue Based) Remote Method Invocation Proxy
import os
import time
from threading import Thread
from multiprocessing import Queue, Process, freeze_support
from multiprocessing.managers import BaseManager


class RMIProxy:
    manager = None
    is_server = False
    remote_caller_queue = None
    remote_callee_queue = None

    @staticmethod
    def get_solo_pair():
        import queue
        q = queue.Queue()
        return RMICaller(q), RMICallee(q)

    @staticmethod
    def get_local_pair():
        queue = Queue()
        return RMICaller(queue), RMICallee(queue)

    @classmethod
    def set_remote_manager(
        cls,
        manager=None,
        is_server=False,
        socket: tuple[str, int] = ('localhost', 8080),
        authkey=b'abc'
    ):
        if manager is not None:
            cls.manager = manager
            cls.is_server = is_server
        else:
            cls.manager = BaseManager(address=socket, authkey=authkey)
            if "localhost" == socket[0]:
                cls.is_server = True
                cls.manager.start()
            else:
                cls.is_server = False
                cls.manager.connect()

    @classmethod
    def get_remote_caller(cls):
        cls.manager.register(
            "get_caller_queue",
            callable=lambda: cls.remote_callee_queue if cls.is_server else None
        )
        queue = cls.manager.get_caller_queue()
        return RMICaller(queue)

    @classmethod
    def get_remote_callee(cls):
        cls.manager.register(
            "get_callee_queue",
            lambda: cls.remote_callee_queue if cls.is_server else None
        )
        queue = cls.manager.get_callee_queue()
        return RMICallee(queue)


class RMICaller:
    def __init__(self, queue: Queue) -> None:
        self.queue = queue

    def invoke(self, func_name: str, *args, **kwargs):
        return self.queue.put((func_name, args, kwargs))


class RMICallee:
    def __init__(self, queue: Queue) -> None:
        self.queue = queue
        self.func_dict = {}

    def register(self, func: callable):
        self.func_dict[func.__name__] = func
        return self

    def invoke(self, func_name: str, *args, **kwargs) -> bool:
        if func_name == "exit":
            return False
        if func_name not in self.func_dict:
            raise ValueError("Invalid function name")
        func = self.func_dict[func_name]
        func(*args, **kwargs)
        return True

    def start(self) -> None:
        t = Thread(target=self.start_service)
        t.setDaemon(True)
        t.start()
        return self

    def start_service(self) -> None:
        while True:
            func_name, args, kwargs = self.queue.get(True)
            success = self.invoke(func_name, *args, **kwargs)
            if not success:
                break


def worker(caller):
    for i in range(10):
        time.sleep(1)
        pid = os.getpid()
        caller.invoke("fprint", f"[{pid}]:{i}")


def fprint(msg: str):
    print(msg)


if __name__ == '__main__':
    freeze_support()
    print(os.getpid())
    RMIProxy.set_remote_manager()
    # callee = RMIProxy.get_remote_callee()
    # caller = RMIProxy.get_remote_caller()
    caller, callee = RMIProxy.get_solo_pair()
    callee.register(fprint)
    callee.start()
    caller.invoke("fprint", "Hello, World!")
    # p = Process(target=worker, args=(caller,))
    # p.start()
    # p.join()
    time.sleep(1)
