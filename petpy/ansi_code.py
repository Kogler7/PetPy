class ANSIWrapper:
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


class ANSIController:
    @staticmethod
    def clear_screen():
        print('\033[2J', end='')

    @staticmethod
    def reset_screen():
        print('\033[H\033[J', end='')

    @staticmethod
    def cursor_home():
        print('\033[H', end='')

    @staticmethod
    def move_cursor(x: int, y: int):
        print(f'\033[{y};{x}H', end='')

    @staticmethod
    def cursor_up(n: int):
        print(f'\033[{n}A', end='')

    @staticmethod
    def cursor_down(n: int):
        print(f'\033[{n}B', end='')
