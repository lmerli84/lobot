from flask import Flask, render_template, request,Response
import datetime
from gpiozero import Robot
from time import sleep

import picamera

#from app.camera_pi import Camera

#from app import app


app = Flask(__name__)

robot = Robot(left=(10, 9), right=(8,7))

@app.route("/")
def controller():
    now = datetime.datetime.now()
    timestring = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': "HELLO",
        'time': timestring
        }
    return render_template('index.html', **templateData)

@app.route('/move', methods=['GET', 'POST'])
def move():
    movement = request.form['movement']
    #print "post request received with movement: ", movement
    if movement == 'forward':
        #print "triggering forward action"
        robot.forward()
        sleep(2)
        robot.stop()
    if movement == 'left':
        #print 'triggering left action'
        robot.left()
        sleep(2)
        robot.stop()
    if movement == 'right':
        #print 'triggering right action'
        robot.right()
        sleep(2)
        robot.stop()
    if movement == 'backward':
        #print "triggering backward action"
        robot.backward()
        sleep(2)
        robot.stop()
    return "Moving " + movement

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(picamera.PiCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3223, debug=True)
