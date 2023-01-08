from petpy.rmi_proxy import Connection


class Reporter:

    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    @classmethod
    def report(cls, *values: object, sep: str = None, end: str = None) -> None:
        
        print(*values, sep=sep, end=end)

    @classmethod
    def report_error(cls, message: str) -> None:
        pass

    @classmethod
    def report_warning(cls, message: str) -> None:
        pass

    @classmethod
    def report_info(cls, message: str) -> None:
        pass

    @classmethod
    def report_debug(cls, message: str) -> None:
        pass

    @classmethod
    def report_progress(cls, message: str) -> None:
        pass
