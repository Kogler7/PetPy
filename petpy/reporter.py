from petpy.connect import Connection


class Reporter:

    def __init__(self, conn: Connection) -> None:
        pass

    @classmethod
    def report(cls, message: str) -> None:
        pass

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
