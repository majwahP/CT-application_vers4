from tkinter import *
from wiki import Wiki
from ctSimulator import CTsimulator
from exercises import Exercises
#customtkinter.set.appearence("system")

#AppFrame
app = Tk()
app.attributes('-topmost', True)
app.state('zoomed') 

#Functions
def calculatePos(root_window,new_window):
    header_height = new_window.winfo_rooty() - new_window.winfo_y()
    x_ = root_window.winfo_rootx() + (root_window.winfo_width() - new_window.winfo_width()) // 2
    y_ = root_window.winfo_rooty() + (root_window.winfo_height() - new_window.winfo_height()) // 2 - header_height
    return x_, y_

def wiki_view():
    new_window = Wiki(app)
    new_window.transient(app)   
    #new_x, new_y = calculatePos(app,new_window)
    #new_window.geometry("+{}+{}".format(new_x, new_y))
    new_window.geometry("1080x720-100-40")
    new_window.wait_window()
    

def simulator_view():

    new_window = CTsimulator()
    app.withdraw()
    new_window.wait_window()
    app.deiconify()

def exercise_view():
    new_window = Exercises()
    app.withdraw()
    new_window.wait_window()
    app.deiconify()
      



#SystemSettings

#Buttons

button_color = '#6CA6CD' 
button_text_color = 'white' 
button_font = ('Helvetica',30,'bold')

btnInfo = Button(master = app, text = "Wiki", command=wiki_view,bg=button_color,fg=button_text_color,font=button_font)
btnSimulation = Button(master=app, text="Simulation", command=simulator_view,bg=button_color,fg=button_text_color,font=button_font) #Changed this to exercise view will fixing from CTK to TK
btnExercises = Button(master=app, text="Exercises",bg=button_color,fg=button_text_color,font=button_font)
btnExtra = Button(master=app, text="Extra",bg=button_color,fg=button_text_color,font=button_font)


btnInfo.place(relx=0.01, rely=0.01,relheight=0.48, relwidth=0.48, anchor='nw')
btnSimulation.place(relx=0.99, rely=0.01,relheight=0.48, relwidth=0.48, anchor='ne')
btnExercises.place(relx=0.01, rely=0.99,relheight=0.48, relwidth=0.48, anchor='sw')
btnExtra.place(relx=0.99, rely=0.99,relheight=0.48, relwidth=0.48, anchor='se')


#GUI
app.geometry("720x480")


#RunTime


app.mainloop()