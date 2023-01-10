import time
import pickle
import requests
from PIL import ImageGrab

# 服务端URL
server_url = 'http://localhost:5000/upload_screenshot'

while True:
    try:
        img = ImageGrab.grab()
        image_bytes = pickle.dumps(img)
        headers = {'Content-Type': 'image/png'}
        requests.post(server_url, data=image_bytes, headers=headers)
        print("ok")
    except:
        print("retry")
    time.sleep(10)
