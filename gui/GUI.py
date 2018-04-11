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
        print("init GUI")

    def start(self):
        print("Number of data modules:" + str(len(self.model_list)))

        self.root.configure(background="black")
        self.main_frame = tk.Frame(self.root, bg="black").grid(row=0, column=0)

        #tk.Label(self.main_frame, text="GUI", fg="white",bg="black", font="Helvetica 40 bold").grid(row=0, column=0, sticky=tk.W)
        clock = gui.GUI_clock.ModuleGUIClock(self.main_frame)
        clock.grid(row=0, column=0, sticky=tk.W)
      
        
        for i in range(0, len(self.model_list)):
            mod = gui.GUI_module.ModuleGUI(self.main_frame, self.model_list[i])
            self.module_list.append(mod)
            mod.grid(row=i+1, column=0, sticky=tk.W)

        self.root.mainloop()

            
