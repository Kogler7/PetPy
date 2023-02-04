from pynput.keyboard import Key


class EditableText:
    def __init__(self):
        self.text = ""
        self.cursor = 0

    def insert(self, code: Key or str):
        char = code if isinstance(code, str) else code.char
        if not char:
            return
        self.text = self.text[:self.cursor] + char + self.text[self.cursor:]
        self.cursor += 1

    def delete(self):
        if self.cursor > 0:
            self.text = self.text[:self.cursor - 1] + self.text[self.cursor:]
            self.cursor -= 1

    def move_left(self):
        if self.cursor > 0:
            self.cursor -= 1

    def move_right(self):
        if self.cursor < len(self.text):
            self.cursor += 1

    def move_home(self):
        self.cursor = 0

    def move_end(self):
        self.cursor = len(self.text)

    def clear(self):
        self.text = ""
        self.cursor = 0

    def get_text(self):
        return self.text

    def __str__(self):
        return self.text[:self.cursor] + "|" + self.text[self.cursor:]
