import sys
PI = len(sys.argv) == 1

if PI:
    from VirtualCamera import VirtualCamera
    
import time
import flask
from flask import Flask
from flask import render_template


if PI:
    camera = VirtualCamera()
    sweep = camera.capture_sweep()
      
app = Flask(__name__)

def get_shot(pos):
    global sweep, START, END
    pos = int(pos)
    if pos < START:
        pos = START
    if pos > END:
        pos = END
    return sweep[pos]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/left/<pos>', methods=['GET'])
def left(pos):
    global PI
    if PI:
        return flask.send_file(get_shot(pos)[0], mimetype='image/jpeg')
    else:
        return flask.send_file('images/left.jpg', mimetype='image/jpeg')

@app.route('/right/<pos>', methods=['GET'])
def right(pos):
    if PI:
        return flask.send_file(get_shot(pos)[1], mimetype='image/jpeg')
    else:
        return flask.send_file('images/right.jpg', mimetype='image/jpeg')


app.run(host='0.0.0.0')

if PI:
    camera.cleanup()
