from .api import *

config = cfparser.ConfigParser()

class KTH_APIrequester(APIrequester):

    url = ''
    model = None

    def __init__(self, modelobj):
        super().__init__()
        config.read('./apis/apiconfig.ini')
        self.url = str(config['URL']['kth'])
        self.model = modelobj
        print("init KTH_APIrequester")

    def request(self):
        #get and store icalendar file
        print("requesting ical schedule")
        res = requests.get(self.url, allow_redirects=True)
        open('./apis/kth_ical_schedule.ics', 'wb').write(res.content)
