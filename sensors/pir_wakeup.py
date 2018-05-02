import RPi.GPIO as GPIO
import time
import os, subprocess

PIR_PIN = 27
MAX_IDLE_SEC = 60

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIR_PIN,GPIO.IN)
os.environ['DISPLAY'] = ":0"

dorun = False
display_is_on = True
lastsignaled =0

def run():
    global dorun
    global display_is_on
    dorun = True  
    print("Staring wakeup on PIR...")

    while dorun:
        now=time.time()
        if GPIO.input(PIR_PIN):
            lastsigneled = now
            if not display_is_on:
                subprocess.call('xset dpms force on', shell=True)
                display_is_on = True
        else:
            if now-lastsignaled > MAX_IDLE_SEC and display_is_on:     
                subprocess.call('xset dpms force off', shell=True)
                display_is_on = False
        time.sleep(1)

    GPIO.cleanup()

def stop():
    dorun = False
