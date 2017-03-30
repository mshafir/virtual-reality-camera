from VirtualCamera import VirtualCamera
import time
import flask
from flask import Flask
from flask import render_template


camera = VirtualCamera()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/left/<pos>')
def left(pos):
    global camera
    camera.move_to(pos)
    return flask.send_file(camera.get_image(), mimetype='image/jpeg')

@app.route('/right/<pos>')
def right(pos):
    camera.move_to(pos + camera.occular_offset)
    return flask.send_file(camera.get_image(), mimetype='image/jpeg')


app.run(host='0.0.0.0')

camera.cleanup()
