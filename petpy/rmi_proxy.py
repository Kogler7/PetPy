# (Queue Based) Remote Method Invocation Proxy
from enum import Enum
from threading import Thread
from multiprocessing import Queue, Manager


class RMIMode(Enum):
    LOCAL = 0
    REMOTE = 1


class RMIProxy:
    def __init__(self, mode: RMIMode, addr: str = None, port: int = None, authkey = None):
        if mode == RMIMode.LOCAL:
            self.queue = Queue()
        elif mode == RMIMode.REMOTE:
            self.manager = Manager()
            self.queue = self.manager.Queue()
        else:
            raise ValueError("Invalid mode")
        self.caller = RMICaller(mode, self.queue)
        self.callee = RMICallee(mode, self.queue)
        return self.caller, self.callee

class RMICaller:
    def __init__(self, mode: RMIMode, queue) -> None:
        self.mode = mode
        if self.mode == RMIMode.LOCAL:
            self.local_queue = queue
        if self.mode == RMIMode.REMOTE:
            self.remote_queue = queue

    def invoke(self, func_name: str, *args, **kwargs) -> None:
        if self.mode == RMIMode.LOCAL:
            self.local_queue.put((func_name, args, kwargs))
        elif self.mode == RMIMode.REMOTE:
            self.remote_queue.put((func_name, args, kwargs))
        else:
            raise ValueError("Invalid mode")
        
    def __getattr__(self, name: str) -> callable:
        def func(*args, **kwargs):
            self.invoke(name, *args, **kwargs)
        return func

class RMICallee:
    def __init__(self, mode: RMIMode, queue) -> None:
        self.mode = mode
        self.func_dict = {}
        if self.mode == RMIMode.LOCAL:
            self.local_queue = queue
        if self.mode == RMIMode.REMOTE:
            self.remote_queue = queue

    def registry(self, func: callable) -> None:
        self.func_dict[func.__name__] = func
        
    def invoke(self, func_name: str, *args, **kwargs) -> bool:
        if func_name == "exit":
            return False
        if func_name not in self.func_dict:
            raise ValueError("Invalid function name")
        func = self.func_dict[func_name]
        func(*args, **kwargs)
        return True
    
    def start(self) -> None:
        target = None
        if self.mode == RMIMode.LOCAL:
            target = self.start_local
        elif self.mode == RMIMode.REMOTE:
            target = self.start_remote
        else:
            raise ValueError("Invalid mode")
        t = Thread(target=target)
        t.setDaemon(True)
        t.start()
    
    def start_local(self) -> None:
        while True:
            func_name, args, kwargs = self.local_queue.get(True)
            success = self.invoke(func_name, *args, **kwargs)
            if not success:
                break
    
    def start_remote(self) -> None:
        pass