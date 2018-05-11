import os
#import glob
import time
     
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#device_file = '/sys/bus/w1/devices/28-03168b14e3ff/w1_slave'


class tempSensorReader():

    dorun = False
    device_file = None
    update = None

    def __init__(self, modelobj, active=True):
        self.model = modelobj
        self.model.setDataSize(rows=1, columns=1)
        self.update = active
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
            
            data = [[str(temp_string[0:2]+' '+u'\xb0'+'C')]]

            try:
                self.model.setData(data)
            except Exception:
                print("failed to set temp data")


    def run(self):
        self.dorun = True
        while self.dorun==True:
            if self.update==True:
                self.request()
            time.sleep(60)
    def activate(self):
        self.update = True
        self.request()
    def inactivate(self):
        self.update = False    

    def stop(self):
        self.dorun = 0






