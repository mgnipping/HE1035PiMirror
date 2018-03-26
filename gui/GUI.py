from tkinter import *


#GUI functions
class GUItk:

    model_list = []
    
    def __init__(self, model):
        self.model_list = model
        print("starting GUI")

    def update(self):
        print("Number of data modules:" + str(len(self.model_list)))
