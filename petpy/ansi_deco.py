class ANSIDecorator:
    @staticmethod
    def bold(text: str) -> str:
        return f"\033[1m{text}\033[0m"
    
    @staticmethod
    def underline(text: str) -> str:
        return f"\033[4m{text}\033[0m"
    
    @staticmethod
    def blink(text: str) -> str:
        return f"\033[5m{text}\033[0m"
    
    @staticmethod
    def reverse(text: str) -> str:
        return f"\033[7m{text}\033[0m"
    
    @staticmethod
    def concealed(text: str) -> str:
        return f"\033[8m{text}\033[0m"