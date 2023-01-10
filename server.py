import os
import time
import pickle
from flask import Flask, request
# from PIL import ImageGrab
from gevent import pywsgi

app = Flask(__name__)

@app.route('/upload_screenshot', methods=['POST'])
def upload_screenshot():
    image_bytes = request.data
    timeStr = time.strftime("%H%M%S")
    with open(f"./shots/{image_bytes}.pkl","wb") as f:
        f.write(image_bytes)
    # img = pickle.loads(image_bytes)
    # img.save(f"./results/{timeStr}.png")
    print("success", timeStr)
    return 'Success'

if __name__ == '__main__':
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    # server.server_forever()
    app.run(host='0.0.0.0',port=5000)
