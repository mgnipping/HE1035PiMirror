import time
import configparser as cfparser
import requests
import time
import datetime
import dateutil.parser
from dateutil.tz import tzlocal

file = './sensors/weatherdata.ini'
config = cfparser.ConfigParser()

class WeatherStation():

    dorun = False
    device_file = None
    ssid = None
    serverip = None
    update = None

    def __init__(self, modelobj, active=True, ssid='', ip=''):
        self.model = modelobj
        self.model.setDataSize(rows=4, columns=3)
        self.update = active
        self.ssid = ssid
        self.serverip=ip

    def request(self):  
        data = []
        try:
            config.read(file)

        except Exception:
            print("Failed to read weather data file")
            return

        try:
            timestamp=dateutil.parser.parse(str(config['meta']['updated'])) #str(config['meta']['updated']) 
            
            print(timestamp)

            now = datetime.datetime.now(tzlocal())
            delta = datetime.timedelta(minutes = -2)
            if timestamp< (now+delta):
                print("weather not updated in >2 minutes")
                data.append(['', 'No weather data', ''])
                data.append(['', 'Connect weatherstation', ''])
                data.append(['', 'to network: '+self.ssid, ''])
                data.append(['', 'server ip: '+self.serverip, ''])

                self.model.setData(data)
                return
         
        except Exception:
            print("Failed to read weather update time")        

        try:
            #insert decimal points
            temp= str(config['values']['t'])
            temp= temp[0:-1]+'.'+temp[-1:]
            wspeed= str(config['values']['w']).rjust(2, '0')
            wspeed= wspeed[0:-1]+'.'+wspeed[-1:]
        
            data.append(['temp', temp, str(u'\xb0'+'C')])
            data.append(['vind', wspeed, 'm/s'])
            data.append(['fukt', str(config['values']['h']), '%'])

            light =  int(config['values']['l'])
            light_p =int(light/1024 * 100)

            data.append(['ljus', str(light_p), '%'])
        except Exception:
            print("Failed to read weather data from file")

      
        try:
            self.model.setData(data)
        except Exception:
            print("Failed to set weather data to model")

     
    def run(self):
        self.dorun = True
        while self.dorun==True:
            if self.update ==True:
                self.request()

            time.sleep(30)

    def activate(self):
        self.update = True
        self.request()
    def inactivate(self):
        self.update = False

    def stop(self):
        self.dorun = False
