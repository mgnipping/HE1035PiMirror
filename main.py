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

    mgui = GUI.MainGUI(data_model)
    
    data_model.append(dataobject.DataObject())
    
    apilist.append(api_sl.SL_APIrequester(data_model[0]))

    data_model.append(dataobject.DataObject())
    
    apilist.append(api_kth.KTH_APIrequester(data_model[1]))

    #request data from each active API module
    for i in range(0, len(apilist)):
        apilist[i].request()

    mgui.start()

run()
