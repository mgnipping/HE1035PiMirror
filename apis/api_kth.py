from .api import *
import time

config = cfparser.ConfigParser()

class KTH_APIrequester(APIrequester):

    url = ''
    model = None
    dorun = 0
    update_interval = 60*60

    def __init__(self, modelobj):
        super().__init__()
        config.read('./apis/apiconfig.ini')
        self.url = str(config['API_ICAL']['url'])
        self.model = modelobj
        print("init KTH_APIrequester")

    def request(self):
        #get and store icalendar file
        print("requesting ical schedule")
        res = requests.get(self.url, allow_redirects=True)
        open('./apis/kth_ical_schedule.ics', 'wb').write(res.content)

    def run(self):
        self.dorun = 1
        while self.dorun == 1:
            self.request()
            print("going to sleep for"+str(self.update_interval)+"seconds")
            time.sleep(60*60)

    def stop(self):
        self.dorun = 0        
