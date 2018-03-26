from gui import *
from apis import *
from sensors import *
from model import *

sensors = []
apilist = []
data_model = []
#init BT

#def getModules(list[], filename):
    #open file for reading
    #append to list

def run():

    print("starting...")
    gui = GUI.GUItk(data_model)
    gui.update()
    data_model.append(dataobject.DataObject())
    gui.update()
    apilist.append(api_sl.SL_APIrequester(data_model[0]))
    #sensor.startSensors()
    
    #get lists of apis and sensors

    #request data from each active API module
    for i in range(0, len(apilist)):
        apilist[i].request()

run()
