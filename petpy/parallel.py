
class Parallel:
    def __init__(self,nr_processes:int=None) -> None:
        self.processes = nr_processes
        
    def task_wrapper(self, func):
        return func
    