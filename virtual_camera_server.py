import RPi.GPIO as GPIO
import time
import picamera
import flask
from flask import Flask
from flask import render_template
from PIL import Image
from io import BytesIO
from StringIO import StringIO


class VirtualCamera:
    def __init__(self, motor_pin, initial_position):
        self.motor_pin = motor_pin
        self.camera = picamera.PiCamera()
        self.camera.vflip = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MOTOR_PIN, GPIO.OUT)
        self.move_to(initial_position)

    def move(self):
        self.mount = GPIO.PWM(self.motor_pin, 50)
        self.mount.start(self.pos)
        time.sleep(0.2)
        self.mount.stop()
        
    def move_to(self, pos):
        self.pos = pos
        self.move()
        
    def move_left(self, amount=1):
        self.pos -= amount
        self.move()
        
    def move_right(self, amount=1):
        self.pos += amount
        self.move()
        
    def get_image(self):
        stream = StringIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        return stream
    
    def get_image_pair(self):
        image_left = self.get_image()
        self.move_right(0.3)
        image_right = self.get_image()
        return [image_left, image_right]
        
    def capture_sweep(self, start, end):
        image_pairs = []
        self.camera.start_preview()
        for i in range(start, end):
            self.move_to(i)
            image_pairs.append(self.get_image_pair())
        self.camera.stop_recording()
        return image_pairs
    
    def cleanup(self):
        GPIO.cleanup()
            
        

INIT_POS = 3
MOTOR_PIN = 18
START = 3
END = 12
camera = VirtualCamera(MOTOR_PIN, INIT_POS)
sweep = camera.capture_sweep(START, END)
      
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

@app.route('/left/<pos>', methods=['POST', 'GET'])
def left(pos):
  return flask.send_file(get_shot(pos)[0], mimetype='image/jpeg')
  #return flask.send_file('images/IMG_8173.JPG', mimetype='image/jpeg')

@app.route('/right/<pos>', methods=['POST', 'GET'])
def right(pos):
  return flask.send_file(get_shot(pos)[1], mimetype='image/jpeg')
  #return flask.send_file('images/IMG_8174.JPG', mimetype='image/jpeg')


app.run(host='0.0.0.0')
camera.cleanup()
