from .api import *


class SMHI_APIrequester(APIrequester):
    apikey = ""
    stationid = None
    model = None
  
    def __init__(self, modelobj):
        print("init SMHI_APIrequester")
        super().__init__()
        self.model = modelobj
