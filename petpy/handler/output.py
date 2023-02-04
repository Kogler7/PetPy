import os
import sys

from petpy.ansi_code import ANSIWrapper, ANSIController
import rich


class OutputHandler:
    pass


class OutputUnit:
    def __init__(self, tag: str, max_line: int = 1, scroll: bool = True):
        self.tag: str = tag
        self.max_line: int = max_line
        self.scroll: bool = scroll
        self.title: str = ''
        self.head_line: str = ''
        self.body_lines: list[str] = []

    def text(self):
        title = self.title if self.title else self.head_line
        res = f"{ANSIWrapper.bold(f'[{self.tag}] {title}')}\n\r"
        if self.title and self.head_line:
            res += f"{self.head_line}\n\r"
        res += "\n\r".join(self.body_lines)
        return res

    def append(self, line: str):
        if len(self.body_lines) >= self.max_line:
            if self.scroll:
                self.body_lines.pop(0)
            else:
                self.body_lines[-1] = line
                return
        self.body_lines.append(line)

    def set_title(self, title: str):
        self.title = title

    def set_head(self, line: str):
        self.head_line = line

    def set_body(self, line: str, line_no: int = -1):
        if line_no == -1:
            self.body_lines[-1] = line
            return
        if line_no >= len(self.body_lines):
            if line_no > self.max_line:
                raise IndexError(f"line_no {line_no} out of range")
            self.body_lines.append(line)
        else:
            self.body_lines[line_no] = line

    def clear(self):
        self.head_line = ''
        self.body_lines = []


class OutputBoard:
    def __init__(self):
        self.isatty: bool = False
        self.width: int = 0
        self.height: int = 0
        self.check_env()
        self.units: dict[str, OutputUnit] = {}

    def check_env(self):
        self.isatty = sys.stdout.isatty()
        if self.isatty:
            self.width, self.height = os.get_terminal_size()
        else:
            self.width, self.height = 80, 24

    def _render_tty(self):
        print(f"{'-' * self.width}\r")
        rich.print([1, 2, 3, True])
        # ANSIController.reset_screen()
        # ANSIController.cursor_home()
        # for unit in self.units.values():
        #     print(unit.text())

    def _render_file(self):
        ANSIController.reset_screen()
        ANSIController.cursor_home()
        print(f"{'-' * self.width}\r")
        for unit in self.units.values():
            print(unit.text())

    def render(self):
        self.check_env()
        if self.isatty:
            self._render_tty()
        else:
            self._render_file()

    def add_unit(self, tag: str, max_line: int = 1, scroll: bool = False):
        self.units[tag] = OutputUnit(tag, max_line, scroll)

    def remove_unit(self, tag: str):
        self.units.pop(tag, None)

    def append(self, tag: str, line: str):
        if tag not in self.units:
            raise KeyError(f"tag {tag} not found")
        self.units[tag].append(line)
        self.render()

    def set_title(self, tag: str, title: str):
        if tag not in self.units:
            raise KeyError(f"tag {tag} not found")
        self.units[tag].set_title(title)
        self.render()

    def set_head(self, tag: str, line: str):
        if tag not in self.units:
            raise KeyError(f"tag {tag} not found")
        self.units[tag].set_head(line)
        self.render()

    def set_body(self, tag: str, line: str, line_no: int = -1):
        if tag not in self.units:
            raise KeyError(f"tag {tag} not found")
        self.units[tag].set_body(line, line_no)
        self.render()
