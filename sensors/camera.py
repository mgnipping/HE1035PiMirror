import picamera
import time

camera = picamera.PiCamera()

def takePhoto():
    print("Taking photo...")
    camera.capture ('sensors/photos/example.jpg')
