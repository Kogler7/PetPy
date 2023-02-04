import time
from executor import ConcurrentExecutor, runnable
from task import Task


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


class Console:
    show_console = True

    def __init__(self, show_console=True):
        self.show_console = show_console


def progress(start: int, end: int = None, step: int = 1):
    if end is None:
        end = start
        start = 0
    for i in range(start, end, step):
        if Console.show_console:
            report(f"{i}/{end}")
        yield i


def report(*args, sep=' ', end='\n'):
    task = Task.get_cur_task()
    if task is not None:
        print(f"[{task.no}]", *args, sep=sep, end=end)
    else:
        print(*args, sep=sep, end=end)


@runnable
def mytask():
    for i in progress(5):
        report(i)
        time.sleep(1)


@concurrent(max_workers=5)
def main():
    res_arr = []
    for i in range(10):
        res = mytask()
        res_arr.append(res)
    for res in res_arr:
        report(res.result())


if __name__ == '__main__':
    main()
    print("main thread")
