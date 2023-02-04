import time
from random import random

from petpy.base.runnable import runnable
from petpy.executor.concurrent import concurrent
from petpy.utils.reporter import report
from petpy.controller.progress import progress


@runnable
def mytask():
    for i in progress(100):
        report(i)
        time.sleep(random() * 0.9 + 0.1)


@concurrent(max_workers=3)
def main():
    res_arr = []
    for i in range(16):
        res = mytask()
        res_arr.append(res)
    for res in res_arr:
        report(res.result())


if __name__ == '__main__':
    main()
    print("main thread")
