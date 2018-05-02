from gui import *
from apis import *
from sensors import *
from model import *
import time
import configparser as cfparser
import threading
import serialreader
import gpio

config = cfparser.ConfigParser()

mgui = None
modules = []
data_model = []
threads = []
serial = False

def getModules(filename):
    print("initialize modules...")
    #open file for reading
    #append to list

#def storeModules(filename):
    #open file for writing
    #write all modules in list
    
def serialread():
    global serial
    serial = True

    while serial is True:
        msg = serialreader.readline()
        print(msg)

        cmd = msg.split("=")
        print(cmd)

        if cmd[0] == 'buss':
            print("sl-tabell: "+ cmd[1])
            
        elif cmd[0] == 'vader':
            print("väder: "+ cmd[1])
        elif cmd[0] == 'schema':
            print("schema: "+ cmd[1])
        elif cmd[0] == 'lights on':
            gpio.ledon()

        elif cmd[0] == 'lights off':
            gpio.ledoff()

        elif cmd[0] == 'photo':
            camera.takePhoto()
        
        elif cmd[0]=='network':
            if str(cmd[1]).find(','):
                params = str(cmd[1]).split(",")

def run():
    global mgui
    mgui = GUI.MainGUI(data_model)

    getModules("example.ini")

    data_model.append(dataobject.DataObject(0,2))
    
    modules.append(api_sl.SL_APIrequester(data_model[0]))

    data_model.append(dataobject.DataObject(2,0))
    
    modules.append(api_kth.KTH_APIrequester(data_model[1]))

    data_model.append(dataobject.DataObject(1,0))
    
    modules.append(api_smhi.SMHI_APIrequester(data_model[2]))

    data_model.append(dataobject.DataObject(0,1))
    
    modules.append(temp_sensor.tempSensorReader(data_model[3]))

    #request data from each active API module
    for i in range(0, len(modules)):
        modules[i].request()
        threads.append(threading.Thread(target=modules[i].run))
        threads[i].setDaemon(True)
        threads[i].start()

    BTcomthread = threading.Thread(target=serialread)
    BTcomthread.start()
    PIRthread = threading.Thread(target=pir_wakeup.run)
    PIRthread.start()
    MagSensorthread = threading.Thread(target=gpio.runMagneticSensor)
    MagSensorthread.start()
    
    mgui.start()


def stopthreads():
    for i in range(0, len(modules)):
        modules[i].stop()

run()
print("returned from main run()")
serial = False
pir_wakeup.stop()
gpio.stopMagneticSensor()
stopthreads()

