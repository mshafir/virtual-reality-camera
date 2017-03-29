import RPi.GPIO as GPIO
import time
import picamera
import flask
from flask import Flask
from PIL import Image
from io import BytesIO
from StringIO import StringIO

app = Flask(__name__)
camera = None
POS = 10

def setup_camera():
   global camera
   camera = picamera.PiCamera()
   camera.vflip = True
   print 'Camera set Up!'

def setup_mount():
  global POS
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(18, GPIO.OUT)
  move_mount()

def move_mount():
  mount = GPIO.PWM(18, 50)
  mount.start(POS)
  time.sleep(0.5)
  mount.stop()

@app.route('/')
def home():
  return 'Hello World'

@app.route('/image')
def image():
  global camera
  stream = StringIO()
  camera.capture(stream, format='jpeg')
  stream.seek(0)
  return flask.send_file(stream, mimetype='image/jpeg')

@app.route('/left')
def left():
  global POS
  POS -= 1
  if POS < 3:
    POS = 3
  move_mount()
  return 'position: '+str(POS)

@app.route('/right')
def right():
  global POS
  POS += 1
  if POS > 12:
    POS = 12
  move_mount()
  return 'position: '+str(POS)

if __name__ == '__main__':
  setup_camera()
  setup_mount()
  # move_mount(mount)
  app.run(host='0.0.0.0')
  # GPIO.cleanup()

