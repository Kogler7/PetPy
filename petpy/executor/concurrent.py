from concurrent.futures import ThreadPoolExecutor


class ConcurrentExecutor:
    def __init__(self, max_workers=10):
        self._max_workers = max_workers
        self._pool = ThreadPoolExecutor(max_workers=max_workers)

