from flask import Flask, render_template, request
import datetime
from gpiozero import Motor
from time import sleep

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
    return render_template('main.html', **templateData)

@app.route('/move', methods=['GET', 'POST'])
def move():
    movement = request.form['movement']
    print "post request received with movement: ", movement
    if movement == 'forward':
        print "triggering forward action"
        robot.forward()
        sleep(2)
        robot.stop()
    if movement == 'left':
        print 'triggering left action'
        robot.left()
        sleep(2)
        robot.stop()
    if movement == 'right':
        print 'triggering right action'
        robot.right()
        sleep(2)
        robot.stop()
    if movement == 'backward':
        print "triggering backward action"
        robot.backward()
        sleep(2)
        robot.stop()
    return "Moving " + movement

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3223, debug=True)