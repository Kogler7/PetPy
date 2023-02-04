import time
from petpy.console import PetPyConsole

if __name__ == '__main__':
    console = PetPyConsole()
    progress = console.progress
    progress.add_task(tid=1, total=500, start=True)
    progress.add_task(tid=2, total=1000, start=True)
    progress.add_task(tid=3, total=200, start=True)
    # print(console.graphics.tasks)
    while not progress.finished:
        progress.step(1)
        progress.step(2, 10)
        progress.step(3)
        time.sleep(0.1)
