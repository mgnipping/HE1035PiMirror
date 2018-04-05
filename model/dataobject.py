
class DataObject:
    data_rows = 0
    data_cols = 0

    data = []

    def __init__(self):
        print("init base DataObject")

    def setData(self, newdata, **kwargs):
        print("setData() for DataObject")
        self.data = newdata

        for key, val in kwargs.items():
            print('[%s] => [%s]' % (str(key), str(val)))
            if key is 'columns':
                self.data_cols = val

            elif key is 'rows':
                self.data_rows = val

        
