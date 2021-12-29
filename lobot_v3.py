from flask import Flask,render_template,Response,request, redirect,url_for
import cv2
import datetime
from gpiozero import Robot
from time import sleep
import logging

app = Flask(__name__)

camera = cv2.VideoCapture(cv2.CAP_V4L2)
robot = Robot(left=(9,10), right=(8,7))

def gen_frames():  
    while True:
        success, frame = camera.read()
        frame = cv2.flip(frame,0) #[0|1|-1]
        #frame = cv2.Canny(frame, 120, 120)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/move', methods=['POST'])
def move():
    movement = request.form['movement']
    #print "post request received with movement: ", movement
    if movement == 'forward':
        #app.logger.info('forward')
        robot.forward(0.5)
        sleep(1)
        robot.stop()
    if movement == 'left':
        #app.logger.info('left')
        robot.left(0.5)
        sleep(1)
        robot.stop()
    if movement == 'right':
        #app.logger.info('right')
        robot.right(0.5)
        sleep(1)
        robot.stop()
    if movement == 'backward':
        #app.logger.info('backward')
        robot.backward(0.5)
        sleep(1)
        robot.stop()
    return  redirect(url_for('index'))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
     app.run(debug=False, host="0.0.0.0",port=3223)