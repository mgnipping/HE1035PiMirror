import picamera
import time

camera = picamera.PiCamera()

def takePhoto():
    print("Taking photo...")
    camera.capture ('photos\example.jpg')
