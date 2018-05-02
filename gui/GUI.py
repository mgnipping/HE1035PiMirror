import tkinter as tk
#import Tkinter as tk
import gui


#GUI functions
class MainGUI(tk.Tk):
    root = tk.Tk()
    main_frame = None
    module_list = []
    model_list = []
    
    def __init__(self, model):
        self.model_list = model
        #print("init GUI")

    def hideModule(self,index):
        self.module_list[index].grid_remove()

    def showModule(self,index):
        self.module_list[index].grid()

    def start(self):
        print("Number of data modules:" + str(len(self.model_list)))

        self.root.configure(background="black")
        self.main_frame = tk.Frame(self.root, bg="black").grid(row=0, column=0)

        #tk.Label(self.main_frame, text="GUI", fg="white",bg="black", font="Helvetica 40 bold").grid(row=0, column=0, sticky=tk.W)
        clock = gui.GUI_clock.ModuleGUIClock(self.main_frame)
        clock.grid(row=0, column=0, sticky=tk.W, padx=20, pady=20)
      
        
        for i in range(0, len(self.model_list)):
            mod = gui.GUI_module.ModuleGUI(self.main_frame, self.model_list[i])
            self.module_list.append(mod)
            r = self.model_list[i].pos_row
            c = self.model_list[i].pos_col
            if r is None:
                r=i+1
            if c is None:
                c=0 
            mod.grid(row=r, column=c, sticky=tk.W, padx=20, pady=20)

        self.root.mainloop()

            
