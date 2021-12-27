from flask import *
from picamera import PiCamera

app = Flask(__name__)

camera = PiCamera()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/image.jpg")
def getImage():
     camera.capture("./templates/image.jpg")
     return send_file("./templates/image.jpg")

if __name__ == "__main__":
     app.run(debug=True, host="0.0.0.0",debug=False)