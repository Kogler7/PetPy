import time

from handler.output import OutputBoard


class ProgressRenderer:
    def __init__(self, start: int, end: int = None, step: int = 1):
        if end is None:
            end = start
            start = 0
        self.start = start
        self.end = end
        self.step = step


class Progress:
    def __init__(self, start: int, end: int = None, step: int = 1):
        if end is None:
            end = start
            start = 0
        self.start = start
        self.end = end
        self.step = step

    def bar(self, cur: int, width: int = 10):
        if cur < self.start:
            cur = self.start
        elif cur > self.end:
            cur = self.end
        bar = int((cur - self.start) / (self.end - self.start) * width)
        return f"[{'=' * bar}{' ' * (width - bar)}]"

    def __iter__(self):
        for i in range(self.start, self.end, self.step):
            yield i

    def __len__(self):
        return (self.end - self.start) // self.step

    def __next__(self):
        return next(self)


if __name__ == '__main__':
    board = OutputBoard()
    board.add_unit('test', 3, True)
    board.set_title('test', 'test title')
    board.set_head('test', 'test head')
    for i in range(1000):
        board.append('test', f"line {i}")
        time.sleep(0.01)
