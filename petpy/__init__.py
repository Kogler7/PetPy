from petpy.parallel import Parallel
from petpy.listener import Listener
from petpy.reporter import Reporter
from petpy.progress import progress
from petpy.ansi_deco import ANSIDecorator


def parallel(processes: int = None, priority: int = 0):
    par = Parallel(processes, priority)
    return par.parallel


def report(message: str) -> None:
    Reporter.report(message)


def info(message: str) -> None:
    Reporter.report_info(message)


def warn(message: str) -> None:
    Reporter.report_warning(message)


def debug(message: str) -> None:
    Reporter.report_debug(message)


def error(message: str) -> None:
    Reporter.report_error(message)


__all__ = [
    "parallel", "progress",
    "Listener", "Reporter",
    "ANSIDecorator",
    "report", "info", "warn", "debug", "error"
]
