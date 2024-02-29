from tkinter import *

class Exercises(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Exercises")
        self.content_frame = Frame(self)
        self.content_frame.pack(fill="both", expand=True)
        self.geometry("720x480")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        self.mainButton = Button(master=self, text="Main", command=self.destroy)
        self.mainButton.place(relx=0.01, rely=0.01,relheight=0.48, relwidth=0.48, anchor='nw')