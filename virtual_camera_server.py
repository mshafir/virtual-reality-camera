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

if PI:
    START = camera.motor_start
    END = camera.motor_end
else:
    START = 1
    END = 18

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
    global START, END
    return render_template('index.html', start=START, end=END)

@app.route('/left/<pos>')
def left(pos):
    global PI
    pos = int(pos)
    if PI:
        return flask.send_file(get_shot(pos)[0], mimetype='image/jpeg')
    else:
        return flask.send_file('images/img'+str(19-pos)+'.jpg', mimetype='image/jpeg')

@app.route('/right/<pos>')
def right(pos):
    global PI
    pos = int(pos)
    if PI:
        return flask.send_file(get_shot(pos)[1], mimetype='image/jpeg')
    else:
        return flask.send_file('images/img'+str(20-pos)+'.jpg', mimetype='image/jpeg')


app.run(host='0.0.0.0')

if PI:
    camera.cleanup()
