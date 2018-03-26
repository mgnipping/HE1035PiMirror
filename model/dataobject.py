
class DataObject:
    data = []
    def __init__(self):
        print("init base DataObject")

    def setData(self, newdata):
        self.data = newdata
