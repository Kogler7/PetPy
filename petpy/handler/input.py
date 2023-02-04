from pynput.keyboard import Key, Listener
from petpy.utils.text import EditableText


class InputHandler:
    def __init__(self, on_update: callable, on_enter: callable):
        self.on_update = on_update
        self.on_enter = on_enter
        self.text = EditableText()
        self.editing = False
        self.listener = Listener(on_press=self.on_press, suppress=True)
        self.listener.start()

    def on_press(self, key):
        if not self.editing:
            if key.char and key.char == '/':
                self.editing = True
                self.text.clear()
                self.text.insert('/')
        else:
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
                self.on_enter(self.text)
                self.text.clear()
                self.editing = False
            elif key == Key.esc:
                self.text.clear()
                self.editing = False
            elif key == Key.space:
                self.text.insert(' ')
            else:
                self.text.insert(key)
        self.on_update(self.text)
