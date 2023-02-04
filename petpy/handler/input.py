from pynput.keyboard import Key, Listener

should_exit = False


class EditableText:
    def __init__(self):
        self.text = ""
        self.cursor = 0

    def insert(self, code: Key or str):
        char = code if isinstance(code, str) else code.char
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

    def __str__(self):
        return self.text[:self.cursor] + "|" + self.text[self.cursor:]


class InputHandler:
    def __init__(self):
        self.text = EditableText()
        self.listener = Listener(on_press=self.on_press, suppress=False)
        self.listener.start()

    def on_press(self, key):
        if key == Key.left:
            self.text.move_left()
        elif key == Key.right:
            self.text.move_right()
        elif key == Key.home:
            self.text.move_home()
        elif key == Key.end:
            self.text.move_end()
        elif key == Key.backspace:
            self.text.delete()
        elif key == Key.enter:
            self.listener.stop()
        elif key == Key.esc:
            self.listener.stop()
        elif key == Key.space:
            self.text.insert(' ')
        else:
            self.text.insert(key)
        print(self.text)


if __name__ == '__main__':
    handler = InputHandler()
    while True:
        pass
