import time
from .api import *

config = configparser.ConfigParser()

class SL_APIrequester(APIrequester):
    apikey = ""
    stationid = None
    max_items = 5
    model = None
  
    def __init__(self, modelobj):
        print("init SL_APIrequester")
        super().__init__()
        self.model = modelobj
        self.model.setDataSize(rows=self.max_items, columns=3)
        
        #get api key from file
        config.read('./apis/apikeys.ini')
        self.apikey = str(config['APIkeys']['trafiklab1'])
        #get max_journeys, station id

    def request(self):
        t = time.localtime()
        #right justify with '0' to ensure hour and min args have 2 digits
        h = str(t.tm_hour).rjust(2, '0')
        m = str(t.tm_min).rjust(2, '0')
        timearg = h+":"+m
        
        rstring = "https://api.resrobot.se/v2/departureBoard?key="+ self.apikey +"&id=740001178&time="+timearg+"&maxJourneys="+ str(self.max_items) +"&passlist=0&format=json"
        r = None
        r = requests.get(rstring)
        print("Requesting data from Trafiklab API... timearg="+ timearg)
        if r != None:
            print("API data was fetched")

        #parse api data
        data = parse(r)

        if data is not None:
            #update model with api data
            self.model.setData(data)
        else:
            print("Failed to parse API data")

    def run(self):
        self.dorun = 1
        while self.dorun == 1:
            #request new API data every minute
            self.request()
            time.sleep(60)
            
    def stop(self):
        self.dorun = 0



def parse(data):

    d = data.json().get("Departure")
   

    if d is None:
        return None

    table = [None] * len(d)

    for i in range(0, len(d)):
        table[i] = []
        table[i].append(d[i].get("transportNumber"))
        s = d[i].get("direction")
        if '(' in s:
            s = s[0:s.index('(')]
        table[i].append(s)
        table[i].append(d[i].get("time")[0:5])
           
    return table
