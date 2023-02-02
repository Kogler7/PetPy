from petpy.utils.rmi_proxy import RMICaller


class Reporter:
    caller:RMICaller = None
    
    def __new__(cls, caller: RMICaller):
        cls.caller = caller

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
