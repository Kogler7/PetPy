import os
import sys
import keyboard as kbd

# print(os.getcwd())
# print(os.path.abspath(__file__))
# print(os.path.dirname(os.path.abspath(__file__)))
# print(os.getpid())
# print(os.cpu_count())

# from PIL import ImageGrab

# img = ImageGrab.grab()
# img.save('test.png')


while True:
    # 打印所有输入字符，不换行
    print(kbd.read_key(), end='')


print(sys.stdout.isatty())
is_windows_terminal = (sys.platform == "win32" and os.environ.get("WT_SESSION"))
print(is_windows_terminal, os.get_terminal_size())
