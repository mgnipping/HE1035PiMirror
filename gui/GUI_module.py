import tkinter as tk
#import Tkinter as tk

class ModuleGUI(tk.Frame):

    model = None

    def __init__(self, prnt, model):
        self.model = model
        super().__init__(prnt, bg="black")

        if model is not None:
            tk.Label(self, text="Module, " +str(model.data_rows)  + "x" + str(model.data_cols), fg="white", bg="black", font="Helvetica 40 bold" ).grid(row=0, column=0, sticky=tk.W)

