from .api import *
import time
import icalendar
import datetime
from dateutil.tz import tzlocal

config = cfparser.ConfigParser()

class KTH_APIrequester(APIrequester):

    url = ''
    model = None
    dorun = 0
    update_interval = 60*60
    max_items = 6
    datafile = None

    def __init__(self, modelobj):
        super().__init__()
        config.read('./apis/apiconfig.ini')
        self.url = str(config['API_ICAL']['url'])
        self.model = modelobj
        self.model.setDataSize(rows=self.max_items, columns=4)
        
        self.datafile = './apis/kth_ical_schedule.ics'
        print("init KTH_APIrequester")

    def request(self):
        #get and store icalendar file
        print("requesting ical schedule")
        res = requests.get(self.url, allow_redirects=True)
        open(self.datafile, 'wb').write(res.content)
        data = parse(self.datafile)
        self.model.setData(data)
        #----(just debug print)---
        #print("upcoming calendar events: " + str(len(data)))
        #for i in range(0, len(data)):
        #    for j in range(0, len(data[i])):
        #        print(data[i][j])
        #-----------------------

    def run(self):
        self.dorun = 1
        while self.dorun == 1:
            self.request()
            print("going to sleep for"+str(self.update_interval)+"seconds")
            time.sleep(60*60)

    def stop(self):
        self.dorun = 0

def formatEvent(veventobj):

    dateformat = '%Y-%m-%d'
    timeformat = '%H:%M'
    lastrow = []

    startdatetime = veventobj['DTSTART'].dt
    enddatetime = veventobj['DTEND'].dt

    datestr = startdatetime.strftime(dateformat)
    timestr = startdatetime.strftime(timeformat) + " - " + enddatetime.strftime(timeformat) 

    lastrow.append(datestr)
    lastrow.append(timestr)

    lastrow.append(str(veventobj['SUMMARY']))
    lastrow.append(str(veventobj['LOCATION']))
    return lastrow
      
def parse(filename, max_items= 6, num_days=7):
    
    #print("Attempting to parse ical file " + str(filename))

    cal = None
    cal = icalendar.Calendar.from_ical(open(filename, 'rb').read())

    if cal is None:
        print("Error: unable to parse icalendar data file")
        return
    
    #get all event objects
    events = cal.walk('vevent')
    table = []
    print("Number of fetched events: " + str(len(events)))

    #get current time (timezone aware) and set delta for timespan to search from now
    curtime = datetime.datetime.now(tzlocal())
    delta = datetime.timedelta(days = num_days)

    #search through the list for events in chosen interval 
    for i in range (0, len(events)):

        starttime = events[i]['DTSTART'].dt
    
        #return if all events in the time interval is already parsed
        if(starttime>curtime+delta) or len(table)==max_items:
            return table

        #skip all past events
        if curtime.year>starttime.year:
            continue
        if curtime.year==starttime.year and curtime.month>starttime.month:
            continue
        if curtime.month == starttime.month and curtime.day>starttime.day:
            continue
        else:
            #construct a new data table row
            table.append(formatEvent(events[i]))
