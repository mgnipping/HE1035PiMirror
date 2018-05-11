import RPi.GPIO as GPIO
import time
import os, subprocess

PIR_PIN = 27
MAX_IDLE_SEC = 60

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIR_PIN,GPIO.IN)
#os.environ['DISPLAY'] = ":0"

dorun = False
display_is_on = True
lastsignaled =0

modules = None

def set(mod_list):
    global modules
    modules = mod_list

def run():
    global dorun
    global display_is_on
    dorun = True  
    print("Staring wakeup on PIR...")

    while dorun is True:
        now=time.time()
        if GPIO.input(PIR_PIN):
            lastsigneled = now
            if not display_is_on:
                subprocess.call('xset dpms force on', shell=True)
                display_is_on = True
                global modules
                for m in modules:
                    m.activate()
        else:
            if now-lastsignaled > MAX_IDLE_SEC and display_is_on:     
                subprocess.call('xset dpms force off', shell=True)
                display_is_on = False
                global modules
                for m in modules:
                    m.inactivate()
                    
        time.sleep(1)

    GPIO.cleanup()
    subprocess.call('xset dpms force on', shell=True)
    print("Stopped wakeup on PIR...")

def stop():
    global dorun
    dorun = False
