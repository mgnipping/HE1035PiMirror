import time
from .api import *

config = configparser.ConfigParser()

#trafiklab API


#extends api_requester base class

class SL_APIrequester(APIrequester):
    apikey = ""
    stationid = None
    max_items = 5
    model = None
  
    def __init__(self, modelobj):
        print("init SL_APIrequester")
        super().__init__()
        self.model = modelobj
        
        #get api key from file
        config.read('./apis/apikeys.ini')
        print("config file sections: ")
        print(len(config.sections()))
        global apikey
        apikey = str(config['APIkeys']['trafiklab1'] )
        #apikey = config.get('APIkeys','trafiklab1')

    def request(self):
        
        t = time.localtime()
        timearg = str(t.tm_hour)+":"+str(t.tm_min)
        print("timearg="+ timearg)
        
        rstring = "https://api.resrobot.se/v2/departureBoard?key="+ self.apikey +"&id=740001178&time="+timearg+"&maxJourneys="+ str(self.max_items) +"&passlist=0&format=json"
        r = None
        r = requests.get(rstring)
        print("requesting as SL_APIrequester")
        if r != None:
            print("api data was fetched")

        #parse api data
        self.model.setData(r.json().get("Departure"))    
        
        #update model with api data
