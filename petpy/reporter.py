class Reporter:
    def __new__(cls: type[Self]) -> Self:
        pass
    
    def __init__(self) -> None:
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
    
    
def report(message: str) -> None:
    Reporter.report(message)