from tkinter import *
import numpy as np
import odl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import math
import time

class CTsimulator_running_mode(Toplevel):
    def __init__(self, attenuation_cof, mA, kV, total_rotation, fast_simulation):
        super().__init__()
        
        self.init_window()
        self.init_content_frames()
        
        #init variables
        self.attenuation_cof = attenuation_cof
        self.mA = mA
        self.kV = kV
        self.total_rot = total_rotation
        if fast_simulation:
            self.simulation_speed = 20
        else:
            self.simulation_speed = 150
        self.perform_CT()
        self.init_imageframe()
        self.start_animation()
        

    def init_window(self):
        self.title("CT Simulator")
        self.attributes('-topmost', True)
        self.state('zoomed')
        self.content_frame = Frame(self)
        self.content_frame.pack(fill="both", expand=True)
        self.geometry("720x480")
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.backButton = Button(master=self, text="Main", command=self.destroy)
        self.backButton.place(relx=0.01, rely=0.01,relheight=0.03, relwidth=0.07, anchor='nw')



    def init_content_frames(self):    
        self.imageFrame = Frame(master=self)
        self.imageFrame.place(relx=0.5, rely=0.01,relheight= 0.95,relwidth= 0.4, anchor = "nw")
        self.plotFrame = Frame(master=self)
        self.plotFrame.place(relx=0.1, rely=0.01,relheight= 0.95,relwidth= 0.4, anchor = "nw")

    def perform_CT(self):
        reco_space = odl.uniform_discr(min_pt=[-20, -20], max_pt=[20, 20], shape=[len(self.attenuation_cof), len(self.attenuation_cof[0])], dtype='float32')
        angle_partition = odl.uniform_partition(0, math.radians(self.total_rot), self.total_rot)    #Custom angle
        detector_partition = odl.uniform_partition(-30, 30, 512)
        geometry = odl.tomo.Parallel2dGeometry(angle_partition, detector_partition)
        ray_trafo = odl.tomo.RayTransform(reco_space, geometry, impl='astra_cpu')
        phantom_data = self.attenuation_cof
        self.phantom = reco_space.element(phantom_data)
        self.proj_data = ray_trafo(self.phantom)
        self.backproj = ray_trafo.adjoint(self.proj_data)

    def init_imageframe(self):  
        self.phantom_image = self.get_image(self.phantom.asarray(), TRUE)
        self.recon_image = self.get_image(self.backproj.asarray(), TRUE)
        self.sino_image = self.get_image(self.proj_data.asarray(), FALSE)
        self.phantomtext = Label(master=self.imageFrame, text="Phantom:")
        self.phantomtext.pack()
        self.phantomimage = Label(master=self.imageFrame, image=self.phantom_image, width=300, height=300)
        self.phantomimage.pack()
        self.sinotext = Label(master=self.imageFrame, text="Sinogram::")
        self.sinotext.pack()
        self.sinogramimage = Label(master=self.imageFrame, image=self.sino_image, width=300)
        self.sinogramimage.pack()
        self.recotext = Label(master=self.imageFrame, text="Reconstructed image::")
        self.recotext.pack()
        self.reconstructedimage = Label(master=self.imageFrame, width=300, height=300)
        self.reconstructedimage.pack()


    def get_image(self,array, resize):
        #create PIL image from array
        normalized_array = (array - np.min(array)) / (np.max(array) - np.min(array))
        pil_image = Image.fromarray((normalized_array * 255).astype(np.uint8))
    
        if resize:
            self.resized_image = pil_image.resize((300, 300), Image.ANTIALIAS)
        else:
            self.resized_image = pil_image    

        #convert to a Photo image
        photo_image = ImageTk.PhotoImage(self.resized_image)

        return photo_image
        

    def start_animation(self):
        # reset current row, scheduling the first update
        self.current_row = 0
        self.after(0, self.update_row)   


    def update_row(self):
        
        row_image = self.resized_image.crop((0, 0, self.resized_image.width, self.current_row + 1))
        row_photo = ImageTk.PhotoImage(row_image)

        self.sinogramimage.configure(image=row_photo)
        self.sinogramimage.image = row_photo

        self.create_plot()

        self.current_row += 1

        # Check if there are more rows to display
        if self.current_row < self.resized_image.height:
            # Schedule the next update [milliseconds]
            self.after(self.simulation_speed, self.update_row)
        else:
            self.reconstructedimage.configure(image=self.recon_image)

     

    def create_plot(self):

        sinogram_intensity = self.proj_data.asarray()
        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(1, 1, 1)

        if hasattr(self, 'plot_canvas'):
            self.plot_canvas.get_tk_widget().destroy()

        plot.plot(sinogram_intensity[(self.current_row), :])

        self.plot_canvas = FigureCanvasTkAgg(fig, master=self.plotFrame)
        self.plot_canvas.draw()
        self.plot_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1) 

 