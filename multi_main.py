from petpy import parallel, progress, report
import time


@parallel
def worker():
    for i in progress(10):
        time.sleep(1)
        report(i)
        
if __name__ == '__main__':
    for i in range(10):
        worker()