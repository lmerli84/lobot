from flask import *
from picamera import PiCamera

app = Flask(__name__)

camera = PiCamera()

@app.route("/")
def index():
    return render_template("index.html")

def gen():
    """Video streaming generator function."""
    while True:
        camera.capture("./templates/image.jpg")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + send_file("./templates/image.jpg") + b'\r\n')

@app.route("/video_feed")
def video_feed():
    while True:
        #camera.capture("./templates/image.jpg")
        #return send_file("./templates/image.jpg")
        return Response(gen())

if __name__ == "__main__":
     app.run(debug=False, host="0.0.0.0",port=3223)