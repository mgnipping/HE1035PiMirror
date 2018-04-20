import os
#import glob
import time
     
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#device_file = '/sys/bus/w1/devices/28-03168b14e3ff/w1_slave'


class tempSensorReader():

    dorun = 0
    device_file = None

    def __init__(self, modelobj):
        self.model = modelobj
        self.model.setDataSize(rows=1, columns=1)
        self.device_file = '/sys/bus/w1/devices/28-03168b14e3ff/w1_slave'

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def request(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            #temp_c = float(temp_string) / 1000.0

            
            data = [[str(temp_string[0:2]+' '+u'\xb0'+'C')]]
            print(data)
            self.model.setData(data)

    def run(self):
        self.dorun = 1
        while self.dorun==1:
            self.request()
            time.sleep(60)

    def stop(self):
        self.dorun = 0






