from VirtualCamera import VirtualCamera
import time
import flask
from flask import Flask
from flask import render_template


camera = VirtualCamera()
app = Flask(__name__)

@app.route('/')
def home():
    global camera
    return render_template('index.html', start=camera.motor_start, end=int(camera.motor_end / camera.motor_inc), caching = 'false')

@app.route('/left/<pos>')
def left(pos):
    global camera
    pos = int(pos)
    camera.move_to(pos, 0.2)
    return flask.send_file(camera.get_image(), mimetype='image/jpeg')

@app.route('/right/<pos>')
def right(pos):
    pos = int(pos)
    camera.move_to(pos + camera.occular_offset, 0.2)
    return flask.send_file(camera.get_image(), mimetype='image/jpeg')


app.run(host='0.0.0.0')

camera.cleanup()
