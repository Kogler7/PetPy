from petpy.base.task import Future, Task
from petpy.executor.executor import Executor


def runnable(fn: callable):
    def wrapper(*args, **kwargs):
        _future = Future()
        _task = Task(_future, fn, args, kwargs)
        current_executor = Executor.current_executor
        if current_executor is not None:
            current_executor.submit(_task)
        else:
            _task.run()
        return _future

    return wrapper
