from gui import *
from apis import *
from sensors import *
from model import *
import time
import configparser as cfparser
import threading

config = cfparser.ConfigParser()

sensors = []
apilist = []
data_model = []
threads = []
#init BT

def getModules(filename):
    print("initialize modules...")
    #open file for reading
    #append to list

#def storeModules(filename):
    #open file for writing
    #write all modules in list

def run():

    mgui = GUI.MainGUI(data_model)

    getModules("example.ini")

    data_model.append(dataobject.DataObject(0,2))
    
    apilist.append(api_sl.SL_APIrequester(data_model[0]))

    data_model.append(dataobject.DataObject(2,0))
    
    apilist.append(api_kth.KTH_APIrequester(data_model[1]))

    data_model.append(dataobject.DataObject(1,0))
    
    apilist.append(api_smhi.SMHI_APIrequester(data_model[2]))

    data_model.append(dataobject.DataObject(0,1))
    
    apilist.append(temp_sensor.tempSensorReader(data_model[3]))

    #request data from each active API module
    for i in range(0, len(apilist)):
        apilist[i].request()
        threads.append(threading.Thread(target=apilist[i].run))
        threads[i].setDaemon(True)
        threads[i].start()

    mgui.start()

def stopthreads():
    for i in range(0, len(apilist)):
        apilist[i].stop()

run()
print("returned from main run()")
stopthreads()

