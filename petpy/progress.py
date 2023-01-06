from petpy.reporter import Reporter

def progress(start, end, step):
    total = end - start
    for i in range(start, end, step):
        Reporter.report(f'{i} / {total}')
        yield i