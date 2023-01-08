from petpy.reporter import Reporter

def progress(start, end, step):
    total = end - start
    for i in range(start, end, step):
        Reporter.report(f'{i} / {total}')
        yield i
        
class Progress:
    def __init__(self, start, end, step):
        self.start = start
        self.end = end
        self.step = step
        self.total = end - start
        self.i = start
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.i >= self.end:
            raise StopIteration
        else:
            Reporter.report(f'{self.i} / {self.total}')
            self.i += self.step
            return self.i
        
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            for i in range(self.start, self.end, self.step):
                Reporter.report(f'{i} / {self.total}')
                func(*args, **kwargs)
        return wrapper
    
    def gene_text(self):
        for i in range(self.start, self.end, self.step):
            Reporter.report(f'{i} / {self.total}')
            yield i