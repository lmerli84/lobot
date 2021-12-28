from flask import *
#from picamera import PiCamera
from camera import VideoCamera
import io
app = Flask(__name__)

camera = PiCamera()
camera.vflip = True

@app.route("/")
def index():
    return render_template("index.html")

def gen_frames(camera):  # generate frame by frame from camera
    while True:
        frame = camera.read() 
        try:
            buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            pass

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
    #while True:
        #camera.capture("./templates/image.jpg")
        #return send_file("./templates/image.jpg")
        #return Response(gen())

if __name__ == "__main__":
     app.run(debug=False, host="0.0.0.0",port=3223)