from tkinter import *
from topic import Topic
from Xray_Tube import Xray_Tube
from sinogram import Sinogram
from ct_scanning import CT_scanning
from reconstruction import Reconstruction
from PIL import Image, ImageTk
import tkinter as tk

button_color = '#6CA6CD' 
button_text_color = 'white'

class Wiki(Toplevel):
    
    def __init__(self,master=None):
        super().__init__(master=master)
        self.title = "Wiki page"
        self.content_frame = Frame(self)
        self.content_frame.pack(fill="both", expand=True)
        self.attributes('-topmost', True)

        self.createExitButton()       
        self.createScrollFrame()  
        #self.createRightSide()  
        self.initRightSide()    
        
        tube = Xray_Tube()  
        title_text = tube.get_title() 
        self.buttons[0].configure(text=title_text, command=lambda tube=tube: self.createRightSide(tube))

        sino = Sinogram()  
        title_text2 = sino.get_title() 
        self.buttons[1].configure(text=title_text2, command=lambda sino=sino: self.createRightSide(sino))

        ct = CT_scanning()  
        title_text3 = ct.get_title() 
        self.buttons[2].configure(text=title_text3, command=lambda ct = ct: self.createRightSide(ct))

        rec = Reconstruction()  
        title_text4 = rec.get_title() 
        self.buttons[3].configure(text=title_text4, command=lambda rec=rec: self.createRightSide(rec))
    
    
    def close_window(self):
        self.destroy()

    
    def createExitButton(self):
        self.exit_button = Button(self.content_frame,bg=button_color,fg=button_text_color, height=5,width=5, text="\u2190", font=("Arial", 12), command=self.close_window)
        self.exit_button.pack(side="left",anchor="nw", padx=5, pady=5) 
        
    def createScrollFrame(self):
        self.scroll_frame = Frame(self.content_frame)
        self.scroll_frame.pack(side="left",fill="both",expand=False)
        
        self.canvas_scroll = Canvas(self.scroll_frame,bg="white",width=200)
        self.canvas_scroll.pack(side="left",fill="both",expand=True)
        
        self.scrollbar_topics = Scrollbar(self.scroll_frame,command=self.canvas_scroll.yview)
        self.scrollbar_topics.pack(side="right",fill="y")
        self.scrollbar_topics.configure(command=self.canvas_scroll.yview)
        
        self.topic_button_frame = Frame(self.canvas_scroll)
        self.canvas_scroll.create_window((10, 0), window = self.topic_button_frame,anchor="nw")
        
        self.buttons = []
        for i in range (4):
            button = Button(master=self.topic_button_frame,width=25, text=f"Button {i+1}",command=lambda i=i+1: self.showInfo(i))
            button.pack(fill="x")
            self.buttons.append(button)
        
        self.canvas_scroll.update_idletasks()
        self.canvas_scroll.config(scrollregion=self.canvas_scroll.bbox("all"))
    
    def createRightSide(self,Topic):
        if hasattr(self, 'canvas'):
            self.update_wiki(Topic)
        else:
            self.canvas = Canvas(self.right_frame, bg="gray")
            self.canvas.place(relx=0, rely=0, anchor="nw", width=920, height=720)
            self.content_frame.bind('<Configure>', self.on_resize)
            #self.canvas.pack(fill="both", expand=True)
            self.update_wiki(Topic)
        
    def on_resize(self, event):
        new_width = self.content_frame.winfo_width() * 0.6
        new_height = self.content_frame.winfo_height() * 0.6

        self.canvas.place_configure(width=new_width, height=new_height)      

   
    def update_wiki(self,some_topic):
        self.canvas.delete("all")
        if some_topic.get_title() == "X-ray Tube":
            self.update_textbox(some_topic)
        elif some_topic.get_title() == "Sinogram":
            self.update_textbox(some_topic)
        else : 
            pass
    
    
    def initRightSide(self):
        self.right_frame = Frame(self.content_frame)
        self.right_frame.pack(side="right",fill="both",expand=True)    
    
    
    def update_textbox(self, some_topic):
        title = some_topic.get_title()
        images = some_topic.get_content()
        
        # Clear canvas before updating
        self.canvas.delete("all")

        # Display title
        self.canvas.create_text(10, 10, anchor="nw", text=title, font=("Arial", 16, "bold"))

        # Create a frame to hold the images
        self.image_frame = tk.Frame(self.canvas, bg = "red")
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")
        #self.image_frame.bind('<Configure>', self.on_resize_two)
       
        image_width = 730   
        image_height = 850  

        img_offset = 0 
        for image in images:
            resized_image = image.resize((image_width, image_height), Image.ANTIALIAS)
            self.tk_image = ImageTk.PhotoImage(resized_image)  
            label = tk.Label(self.image_frame, image=self.tk_image)
            label.image = self.tk_image  
            label.pack(fill='both',expand=True,pady=5)  
            self.canvas.bind('<Configure>', self.on_resize_two)



        if not hasattr(self, 'scrollbar'):
            self.scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
            self.scrollbar.pack(side="right", fill="y")
            self.canvas.config(yscrollcommand=self.scrollbar.set)

            # Update scroll region and bind mouse wheel events
            self.image_frame.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
            self.image_frame.bind_all("<MouseWheel>", self._on_mousewheel)  # macOS and Linux
            self.image_frame.bind_all("<Button-4>", self._on_mousewheel)    # Windows
            self.image_frame.bind_all("<Button-5>", self._on_mousewheel) 
    
    def on_resize_two(self, event):
        # Calculate the new size while maintaining the aspect ratio
        new_width = event.width
        new_height = int((new_width / self.tk_image.width) * self.tk_image.height)

   
    '''def on_resize_two(self, event):
        # Calculates new dimensions based on the event width and height
        new_width = self.right_frame.winfo_width() * 0.9
        new_height = self.right_frame.winfo_height() * 0.9

        self.image_frame(width=new_width, height=new_height) '''     
    
    
    def on_frame_configure(self, event=None):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        for label in self.image_frame.winfo_children():
            image = label.cget("image")
            img_width, img_height = image.width(), image.height()
            frame_width, frame_height = self.image_frame.winfo_width(), self.image_frame.winfo_height()
            if img_width > frame_width or img_height > frame_height:
                ratio = min(frame_width / img_width, frame_height / img_height)
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                image = image.zoom(new_width // img_width, new_height // img_height)
                label.config(image=image)
                label.image = image

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")
        