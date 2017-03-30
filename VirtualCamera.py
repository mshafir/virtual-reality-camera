import RPi.GPIO as GPIO
import picamera
from PIL import Image
from StringIO import StringIO
import time

class VirtualCamera:
    def __init__(self):
        # VIRTUAL CAMERA SETTINGS
        self.motor_pin = 18
        self.occular_offset = 0.3
        self.motor_start = 3
        self.motor_end = 12
        self.motor_inc = 1
        self.motor_delay = 0.2
        # initialization
        self.camera = picamera.PiCamera()
        self.camera.vflip = True
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        self.move_to(self.motor_start, 0.5)

    def move(self, delay=0.2):
        self.mount = GPIO.PWM(self.motor_pin, 50)
        self.mount.start(self.pos)
        time.sleep(delay)
        self.mount.stop()
        
    def move_to(self, pos, delay):
        self.pos = pos
        self.move(delay)
        
    def move_left(self, amount=1, delay=0.2):
        self.pos -= amount
        self.move(delay)
        
    def move_right(self, amount=1, delay=0.2):
        self.pos += amount
        self.move(delay)
        
    def get_image(self):
        # stream = StringIO()
	stream = 'images/img'+str(self.pos)+'.jpg'
        self.camera.capture(stream, format='jpeg')
        # stream.seek(0)
        return stream
    
    def get_image_pair(self):
        image_left = self.get_image()
        self.move_right(self.occular_offset, self.motor_delay)
        image_right = self.get_image()
        return [image_left, image_right]
        
    def capture_sweep(self):
        image_pairs = []
        self.camera.start_preview()
        i = self.motor_start
        while i <= self.motor_end:
            self.move_to(i, self.motor_delay)
            image_pairs.append(self.get_image_pair())
            i += self.motor_inc
        self.camera.stop_preview()
        return image_pairs
    
    def cleanup(self):
        GPIO.cleanup()
            