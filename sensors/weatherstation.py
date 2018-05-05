import time
import configparser as cfparser

file = './sensors/weatherdata.ini'
config = cfparser.ConfigParser()

class WeatherStation():

    dorun = 0
    device_file = None

    def __init__(self, modelobj):
        self.model = modelobj
        self.model.setDataSize(rows=4, columns=3)

    def request(self):  
        data = []
        try:
            config.read(file)

            #insert decimal points
            temp= str(config['values']['t'])
            temp= temp[0:-1]+'.'+temp[-1:]
            wspeed= str(config['values']['w']).rjust(2, '0')
            wspeed= wspeed[0:-1]+'.'+wspeed[-1:]
        
            data.append(['temp', temp, str(u'\xb0'+'C')])
            data.append(['wind', wspeed, 'm/s'])
            data.append(['hum.', str(config['values']['h']), '%'])
            data.append(['light', str(config['values']['l']), ' '])
        except Exception:
            print("Failed to read weather data from file")

        #print(data)
        try:
            self.model.setData(data)
        except Exception:
            print("Failed to set weather data to model")

    def run(self):
        self.dorun = 1
        while self.dorun==1:
            self.request()
            time.sleep(30)

    def stop(self):
        self.dorun = 0
