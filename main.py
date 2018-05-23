from gui import *
from apis import *
from sensors import *
from model import *
import time
import configparser as cfparser
import threading
import serialreader
import gpio
import wificonfig

config = cfparser.ConfigParser()

mgui = None
modules = []
data_model = []
threads = []
serial = False
    
def serialread():
    global serial
    global mgui
    
    serial = True

    while serial is True:
        msg = serialreader.readline()
        print(msg)

        cmd = msg.split("=")
        print(cmd)

        if cmd[0] == 'buss':
            if mgui != None:
                if cmd[1] == '0':
                    mgui.hideModule(0)
                    modules[0].inactivate()
                elif cmd[1] == '1':
                    mgui.showModule(0)
                    modules[0].activate()

        elif cmd[0] == 'schema':
            if mgui != None:
                if cmd[1] == '0':
                    mgui.hideModule(1)
                    modules[1].inactivate()
                elif cmd[1] == '1':
                    mgui.showModule(1)
                    modules[1].activate()

        elif cmd[0] == 'vader':
            if mgui != None:
                if cmd[1] == '0':
                    mgui.hideModule(2)
                    modules[2].inactivate()
                elif cmd[1] == '1':
                    mgui.showModule(2)
                    modules[0].activate()
        elif cmd[0] == 'temp':
            if mgui != None:
                if cmd[1] == '0':
                    mgui.hideModule(3)
                    modules[3].inactivate()
                elif cmd[1] == '1':
                    mgui.showModule(3)
                    modules[3].activate()
        elif cmd[0] == 'vaderut':
            if mgui != None:
                if cmd[1] == '0':
                    mgui.hideModule(4)
                    modules[4].inactivate()
                elif cmd[1] == '1':
                    mgui.showModule(4)
                    modules[4].inactivate()

        elif cmd[0] == 'lights on':
            gpio.ledon()
        elif cmd[0] == 'lights off':
            gpio.ledoff()
        elif cmd[0] == 'photo':
            camera.takePhoto()
        
        elif cmd[0]=='network':
            if str(cmd[1]).find(','):
                params = str(cmd[1]).split(",")
                ssid = params[0].strip()
                pwd = params[1].strip()
                global isConnected
                isConnected = wificonfig.configure(ssid, pwd)
                print(isConnected)

def run():
    global mgui
    mgui = GUI.MainGUI(data_model)

    data_model.append(dataobject.DataObject(1,1))
    
    modules.append(api_sl.SL_APIrequester(data_model[0]))

    data_model.append(dataobject.DataObject(2,0))
    
    modules.append(api_kth.KTH_APIrequester(data_model[1]))

    data_model.append(dataobject.DataObject(2,1))
    
    modules.append(api_smhi.SMHI_APIrequester(data_model[2]))

    data_model.append(dataobject.DataObject(0,1))
    
    modules.append(temp_sensor.tempSensorReader(data_model[3]))

    data_model.append(dataobject.DataObject(1,0))
    
    modules.append(weatherstation.WeatherStation(data_model[4], True, wificonfig.current_ssid, wificonfig.current_ip))

    #request data from each active API module
    for i in range(0, len(modules)):
        modules[i].request()
        threads.append(threading.Thread(target=modules[i].run))
        threads[i].setDaemon(True)
        threads[i].start()

    pir_wakeup.set(modules)
    PIRthread = threading.Thread(target=pir_wakeup.run)
    PIRthread.setDaemon(True)
    PIRthread.start()
    
    mgui.start()


def stopthreads():
    for i in range(0, len(modules)):
        modules[i].stop()

BTcomthread = threading.Thread(target=serialread)
BTcomthread.setDaemon(True)
BTcomthread.start()

MagSensorthread = threading.Thread(target=gpio.runMagneticSensor)
MagSensorthread.setDaemon(True)
MagSensorthread.start()

print(wificonfig.getSSID())
print(wificonfig.current_ip)

if wificonfig.isConnected() is False:
    print("waiting for wifi data...")
while wificonfig.isConnected() is False:
    time.sleep(1)

run()

print("returned from main run()")
serial = False
pir_wakeup.stop()
gpio.stopMagneticSensor()
stopthreads()

