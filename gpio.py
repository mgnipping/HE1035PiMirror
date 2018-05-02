import time
import RPi.GPIO as GPIO

GPIO.setmode (GPIO.BCM ) 
GPIO.setwarnings (False)

GPIO.setup (17,GPIO.OUT )
GPIO.setup (20,GPIO.OUT )
GPIO.setup(21,GPIO.IN)

dorun = False

def ledon():
    print ("Turning LEDs on")
    GPIO.output (17,GPIO.HIGH )

def ledoff():
    print ("Turning LEDs off")
    GPIO.output (17,GPIO.LOW )

def runMagneticSensor():

    global dorun
    dorun = True

    while dorun:
        if ( GPIO.input(21)==0 ):
                GPIO.output (20,GPIO.HIGH )

        else:
                GPIO.output (20,GPIO.LOW )
        time.sleep(1)

def stopMagneticSensor():

    global dorun
    dorun = False
