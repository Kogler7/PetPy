import os
import keyboard as kbd

print(os.getcwd())
print(os.path.abspath(__file__))
print(os.path.dirname(os.path.abspath(__file__)))
print(os.getpid())
print(os.cpu_count())