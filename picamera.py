from flask import redirect, url_for, session, request, \
             render_template, Response
from simplepam import authenticate
from app.camera_pi import Camera
from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index',  methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['submit']:
            Camera.StopPreview()
    elif request.method == 'GET':
        return render_template("index.html", title="Home")


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')