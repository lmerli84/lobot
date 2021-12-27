from flask import Flask
import time
import picamera
import logging
import sys
import os
if sys.version_info[0] == 2:
    from cStringIO import StringIO as bio
else:
    from io import BytesIO as bio

app = Flask(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s '
                    + '[%(filename)s:%(lineno)s:%(funcName)s()] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

@app.route("/start", methods=['POST'])
def start_preview():
    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)
        camera.start_preview()
        time.sleep(300)

@app.route("/stop", methods=['POST'])
def stop_preview():
    with picamera.PiCamera() as camera:
        camera.stop_preview()

if __name__ == "__main__":
    app.run(host='192.168.0.198', port='8080')