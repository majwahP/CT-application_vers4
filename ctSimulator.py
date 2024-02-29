from tkinter import *
from ctSimulator_running_mode import CTsimulator_running_mode
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import spekpy as sp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math


class CTsimulator(Toplevel):
    def __init__(self):
        super().__init__()
        
        #init variable
        self.phantom_objects = []

        self.init_window()
        self.init_window_content()
        self.init_tube_settings_box()
        self.update_spectra() 
        self.init_phantom_creation_functions()
        
        #button to start simulation with chosen values
        self.goButon = Button(master=self.content_frame, text="Simulate!", command=self.go_to_simulator)
        self.goButon.place(relx=0.7, rely=0.85, relwidth=0.25, relheight=0.12, anchor="nw")


    #Functions

    def init_window(self):
        self.title("CT Simulator")
        self.attributes('-topmost', True)
        self.state('zoomed') 
        self.content_frame = Frame(self)
        self.content_frame.pack(fill="both", expand=True)
        self.geometry("720x480")
        self.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.start_width = self.winfo_width()
        self.start_height = self.winfo_height()
        

    def init_window_content(self):
        self.header = Label(master=self.content_frame, text="Setup your CT scan", font=("Arial",25))
        self.header.pack( pady=1,anchor="n")
        #button to go back to main
        self.mainButton = Button(master=self, text="Main", command=self.closeWindow)
        self.mainButton.place(relx=0.01, rely=0.01,relheight=0.03, relwidth=0.07, anchor='nw')
        #frame to bpace dropdowns with object characteristics above object canvas
        self.dropDown_frame = Frame(master=self.content_frame)
        self.dropDown_frame.place(relx=0.4, rely=0.1, relwidth=0.45, relheight=0.1, anchor="nw") 
        #add options of how simulation should be peformed
        self.noSimulationChecked= BooleanVar()
        self.noSimulation = Checkbutton(master=self.content_frame, variable=self.noSimulationChecked, text="No simulation", command=self.on_checkbox_clicked)
        self.noSimulation.place(relx=0.7, rely=0.8, relwidth=0.05, relheight=0.05, anchor="nw")  
        self.simulation_speed_fast_btn = Button(master=self.content_frame, text="Fast simulation", command=self.toggle_color, bg='gray')
        self.simulation_speed_fast_btn.place(relx=0.77, rely=0.8, relwidth=0.1, relheight=0.05, anchor="nw")
        self.simulation_speed_slow_btn = Button(master=self.content_frame, text="Slow simulation", command=self.toggle_color, bg='green')
        self.simulation_speed_slow_btn.place(relx=0.87, rely=0.8, relwidth=0.1, relheight=0.05, anchor="nw")

        

    #Settings frame
    def init_tube_settings_box(self):

        #Frame to but content related to the tube settings
        self.tubeSettingsFrame = Frame(master=self.content_frame)
        self.tubeSettingsFrame.pack()
        self.tubeSettingsFrame.place(relx=0.03, rely=0.1,relheight= 0.85,relwidth= 0.3, anchor = "nw")

        #settings related to x-ray tube (in the order they appear in the frame)
        #title
        self.tubeTitle = Label(master=self.tubeSettingsFrame,text="Tube Settings", font=("Helvetica", 16))
        self.tubeTitle.pack(padx= 60, side=TOP, anchor="nw")

        #choose anode material
        self.anodeFrame = Frame(master=self.tubeSettingsFrame, height=50)
        self.anodeFrame.pack(padx=10, side=TOP, anchor="nw")
        self.labelanode = Label(master=self.anodeFrame,text="Anode material")
        self.labelanode.pack(side=LEFT)

        anode_material_options = [ 
            "Tungsten",
            "Rhodium",
            "Molybdenum"
        ]
        self.selected_option_anode_material = StringVar()
        self.selected_option_anode_material.set("Tungsten")
        option_drop_menu_anode_material = OptionMenu(self.anodeFrame, self.selected_option_anode_material, *anode_material_options, command=lambda event: self.update_voltage_message())
        option_drop_menu_anode_material.pack(side=LEFT)
        
        #choose tube current
        self.currentFrame = Frame(master=self.tubeSettingsFrame, height=50)
        self.currentFrame.pack(padx= 10, side=TOP, anchor="nw")
        self.labelmA = Label(master=self.currentFrame,text="Current [mA]")
        self.labelmA.pack(side=LEFT)
        self.mAinput = Entry(master=self.currentFrame)
        self.mAinput.insert(0, "100")
        self.mAinput.config(fg='gray')
        self.mAinput.pack(side=LEFT,pady=10)

        #Choose tube voltage
        self.voltageFrame = Frame(master=self.tubeSettingsFrame, height=50)
        self.voltageFrame.pack(padx=10, side=TOP, anchor="nw")
        self.labelkV = Label(master=self.voltageFrame,text="Enter a voltage between 20 and 300 kV.")
        self.labelkV.pack(side=LEFT)
        self.kVinput = Entry(master=self.voltageFrame)
        self.kVinput.insert(0, "120")
        self.kVinput.config(fg='gray')
        self.kVinput.pack(side=LEFT, pady=5)

        #filter material
        self.filterFrame = Frame(master=self.tubeSettingsFrame, height=50)
        self.filterFrame.pack(padx=10, side=TOP, anchor="nw")
        self.labelfilter_mat = Label(master=self.filterFrame,text="Material of tube filter:")
        self.labelfilter_mat.pack(side=LEFT)

        filter_material_options = [ 
            "Aleminium",
            "Copper",
            "Tin",
            "Gadolinium"
        ]
        self.selected_option_filter_material = StringVar()
        self.selected_option_filter_material.set("Aleminium")
        option_drop_menu_filter_material = OptionMenu(self.filterFrame, self.selected_option_filter_material, *filter_material_options)
        option_drop_menu_filter_material.pack(side=LEFT)

        #thickness of filter
        self.thicknessFrame = Frame(master=self.tubeSettingsFrame, height=50)
        self.thicknessFrame.pack(padx=10, side=TOP, anchor="nw")
        self.labelthickness = Label(master=self.thicknessFrame,text="Thickness filter [mm]")
        self.labelthickness.pack(side=LEFT)
        self.thicknessinput = Entry(master=self.thicknessFrame)
        self.thicknessinput.insert(0, "1")
        self.thicknessinput.config(fg='gray')
        self.thicknessinput.pack(side=LEFT, pady=5)

        #Choose angle of anode
        self.anode_angle_Frame = Frame(master=self.tubeSettingsFrame, height=50)
        self.anode_angle_Frame.pack(padx=10, side=TOP, anchor="nw")
        self.label_anode_angle = Label(master=self.anode_angle_Frame,text="Anode angle [Deg]")
        self.label_anode_angle.pack(side=LEFT)
        self.angle_input = Entry(master=self.anode_angle_Frame)
        self.angle_input.insert(0, "15")
        self.angle_input.config(fg='gray')
        self.angle_input.pack(side=LEFT, pady=5)

        #button that generates a new spectra when pressed
        self.add_plot_button = Button(self.tubeSettingsFrame, text="Update Spectra", command=self.update_spectra)
        self.add_plot_button.pack(pady=1)

        #Frame to place image of the spectra
        self.spectra_frame = Frame(self.tubeSettingsFrame, width=500, height=400)
        self.spectra_frame.pack(pady=5)

        


        #simulation settings
        self.simulatorTitle = Label(master=self.tubeSettingsFrame,text="Simulator Settings:", font=("Helvetica", 16))
        self.simulatorTitle.pack(padx= 60, side=TOP, anchor="nw")

        #Choose the total rotation of scan
        self.total_rot_Frame = Frame(master=self.tubeSettingsFrame, height=50)
        self.total_rot_Frame.pack(padx=10, side=TOP, anchor="nw")
        self.label_tot_rot = Label(master=self.total_rot_Frame,text="Total rotation angle [Deg]")
        self.label_tot_rot.pack(side=LEFT)
        self.tot_rot_input = Entry(master=self.total_rot_Frame)
        self.tot_rot_input.insert(0, "180")
        self.tot_rot_input.config(fg='gray')
        self.tot_rot_input.pack(side=LEFT, pady=5)

          
    def update_voltage_message(self):
        if self.selected_option_anode_material.get() == "Rhodium" or self.selected_option_anode_material.get() == "Molybdenum":
            self.labelkV.config(text="Enter a voltage between 20 and 50 kV")
            self.kVinput.delete(0, END)  
            self.kVinput.insert(0, "30") 
        elif self.selected_option_anode_material.get() == "Molybdenum":
            self.labelkV.config(text="Enter a voltage between 20 and 50 kV")
            self.kVinput.insert(0, "30")
        else:
            self.labelkV.config(text="Enter a voltage in the interval 20 to 300 kV")


    #Spectra functions
    def generate_spectra(self):
    
        #get user input
        kV = int(self.kVinput.get())
        anode_material = self.selected_option_anode_material.get()
        thickness = int(self.thicknessinput.get())
        angle = int(self.angle_input.get())
        if self.selected_option_filter_material.get() == "Aleminium":
            filter_material = 'Al'
        elif self.selected_option_filter_material.get() == "Copper":
           filter_material = 'Cu' 
        elif self.selected_option_filter_material.get() == "Tin":
           filter_material = 'Sn'  
        elif self.selected_option_filter_material.get() == "Gadolinium":
            filter_material = 'Gd' 
        if self.selected_option_anode_material.get() == "Tungsten":
            anode_material = 'W'
        elif self.selected_option_anode_material.get() == "Rhodium":
            anode_material = 'Rh'
        elif self.selected_option_anode_material.get() == "Molybdenum":
            anode_material = 'Mo'

        #generate the spectra
        self.spectra = sp.Spek(kvp=kV,th=angle,mu_data_source='nist', targ=anode_material)
        self.spectra.filter(filter_material,thickness)
        
        
    def update_spectra(self):
        self.generate_spectra()

        #Create plot of spectra and put in frame
        fig = Figure(figsize=(5,4), dpi=100)
        spec_plot = fig.add_subplot(111)
        spec_plot.set_xlabel('Energy (eV)')
        spec_plot.set_ylabel('Intensity')
        energy, intensity = self.spectra.get_spectrum(edges=True)
        x = energy
        y = intensity

        #remove erlier plot
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()


        spec_plot.plot(x, y)
    
        self.canvas = FigureCanvasTkAgg(fig, master=self.spectra_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP,fill=BOTH, expand=False)       
       
    def init_phantom_creation_functions(self):
        #canvas for objects
        self.dragNdropCanvas = Canvas(master=self.content_frame, width=600, height=600)
        self.dragNdropCanvas.pack()
        self.dragNdropCanvas.place(relx=0.4, rely=0.2, anchor = "nw")
        self.draw_square()
        self.create_dropdown_opt()

    #Drag and drop Functions
    def start_drag(self, event, id):
        self.widget = id
        self.dragNdropCanvas.itemconfig(self.widget, start=(event.x, event.y))
       
    def motion_drag(self, event, id):
        self.widget = id
        current_coords = self.dragNdropCanvas.coords(self.widget)
        width = current_coords[2] - current_coords[0]
        height = current_coords[3] - current_coords[1]
        self.dragNdropCanvas.coords(self.widget, event.x, event.y, event.x + width, event.y + height)          

    def delete_object(self, event, id):
        self.widget = id
        self.dragNdropCanvas.delete(self.widget)   
       
   
    def draw_square(self):
        #draw square to mark canvas
        self.square_x1 = 10
        self.square_y1 = 10
        self.square_x2 = 599
        self.square_y2 = 599

        # Draw the square
        self.dragNdropCanvas.create_rectangle(self.square_x1, self.square_y1, self.square_x2, self.square_y2, outline="black")


    def create_dropdown_opt(self):

        #options
        shape_options = [ 
            "rectangle", 
            "45 deg line", 
            "vertical line",
            "horizontal line",
            "oval"
        ]

        material_options = [
            "al",
            "water",
            "tissue",
            "Air",
            "Bone",
            "Blood",
            "Kidney",
            "Lead"
        ]

        scale_options = [
            1,
            2,
            3,
            4,
            5
        ]

        #add size options, how?

        #shape drop down
        self.selected_option_shape = StringVar()
        self.selected_option_shape.set("Shape")
        option_drop_menu_shape = OptionMenu(self.dropDown_frame, self.selected_option_shape, *shape_options)
        option_drop_menu_shape.pack(side=LEFT)
        option_drop_menu_shape.config(height=17)

        #material drop down
        self.selected_option_material = StringVar()
        self.selected_option_material.set("Material")
        option_drop_menu_material = OptionMenu(self.dropDown_frame, self.selected_option_material, *material_options)
        option_drop_menu_material.pack(side=LEFT)
        option_drop_menu_material.config(height=17)

        #scaling options dropdown
        self.selected_option_scale = StringVar()
        self.selected_option_scale.set("Scale")
        option_drop_menu_scale = OptionMenu(self.dropDown_frame, self.selected_option_scale, *scale_options)
        option_drop_menu_scale.pack(side=LEFT)
        option_drop_menu_scale.config(height=17)
        
        #button to att the object with chosen characteristics
        self.addObject_button = Button(master=self.dropDown_frame, text="Add Object", bg = "green", command=self.addObject)
        self.addObject_button.pack(side=LEFT)

        #add info about deleting objects after dropdowns
        self.info_delete_object = Label(master=self.dropDown_frame, text="Delete an object by right-clicking on it")
        self.info_delete_object.pack(side=LEFT, anchor=S)
       

      
    
    def addObject(self):
        #find chosen characteristics
        if self.selected_option_shape.get() == "Shape":
            shape = "rectangle"   
        else:
            shape = self.selected_option_shape.get()
        if self.selected_option_material.get() == "Material":
            material = "tissue"
        else:
            material = self.selected_option_material.get()
        if self.selected_option_scale.get() != "Scale":
            scale = int(self.selected_option_scale.get())
        else:
            scale=1

        #Create the object   
        if shape == "rectangle":
            object_id = self.dragNdropCanvas.create_rectangle(100, 100, 100+(scale/2)*150, 100+(scale/2)*150, fill=self.get_material_color(material))
        if shape == "45 deg line":
            object_id =self.dragNdropCanvas.create_line(100, 100, 100+(scale/2)*150, 100+(scale/2)*150, width=5, fill=self.get_material_color(material))
        if shape == "vertical line":
            object_id =self.dragNdropCanvas.create_line(100, 100, 100, 100+(scale/2)*150, width=5, fill=self.get_material_color(material))    
        if shape == "horizontal line":
            object_id =self.dragNdropCanvas.create_line(100, 100, 100+(scale/2)*150, 100, width=5, fill=self.get_material_color(material))        
        if shape == "oval":
            object_id =self.dragNdropCanvas.create_oval(100, 100, 100+(scale/2)*150, 100+(scale/2)*150, fill=self.get_material_color(material))

        #bind action functions to the object
        self.dragNdropCanvas.tag_bind(object_id, "<ButtonPress-1>", lambda event, id=object_id: self.start_drag(event, id))
        self.dragNdropCanvas.tag_bind(object_id, "<B1-Motion>", lambda event, id=object_id: self.motion_drag(event, id))
        self.dragNdropCanvas.tag_bind(object_id,"<ButtonPress-3>", lambda event, id=object_id: self.delete_object(event, id))
        #add object to objectarray
        self.phantom_objects.append(self.dragNdropCanvas.find_withtag(object_id)[0])

    def get_material_color(self, material):
        # Define a color to each material
        color_codes = {
            "al": "gray",
            "water": "blue",
            "tissue": "pink",
            "Air": "white",
            "Bone": "light gray",
            "Blood": "red",
            "Kidney":"purple",
            "Lead":"black"
            
        }
        return color_codes.get(material, 0)


    #start simulation Functions
    def go_to_simulator(self):
        #get input values
        matrix = self.get_phantom_matrix()
        attenuation = matrix
        mA = self.mAinput.get()
        kV = self.kVinput.get()
        rot_deg = self.tot_rot_input.get()
        if self.simulation_speed_fast_btn.cget("bg") == 'green':
            fast_simulation = TRUE
        elif self.simulation_speed_fast_btn.cget("bg") == 'gray':   
            fast_simulation = False
        if self.noSimulationChecked.get():
            no_simulation = TRUE
            fast_simulation = None
        else:
            no_simulation=False    
            if self.simulation_speed_fast_btn.cget("bg") == 'green':
                fast_simulation = TRUE
            elif self.simulation_speed_fast_btn.cget("bg") == 'gray':   
                fast_simulation = False    
        if not rot_deg:
            rot_deg=180
        self.new_window = CTsimulator_running_mode(attenuation, mA, kV, int(rot_deg), fast_simulation, no_simulation)
        self.new_window.wait_window()
        
       
   
    def get_phantom_matrix(self):
        # create a matrix with mu values present in each pixel in the phantom canvas
        matrix = [[0 for _ in range(600)] for _ in range(600)]

        # Iterate through each canvas object, different way to add depending on shape
        for obj in self.phantom_objects:
            if self.dragNdropCanvas.type(obj) == "rectangle":
                x1, y1, x2, y2 = self.dragNdropCanvas.coords(obj)
                color = self.dragNdropCanvas.itemcget(obj, "fill")
                color_code = self.get_mu(color)
                for y in range(int(y1), int(y2)):
                    for x in range(int(x1), int(x2)):
                        matrix[y][x] = color_code

            elif self.dragNdropCanvas.type(obj) == "oval":
                x1, y1, x2, y2 = self.dragNdropCanvas.coords(obj)
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                radius_x = (x2 - x1) / 2
                radius_y = (y2 - y1) / 2

                color = self.dragNdropCanvas.itemcget(obj, "fill")
                color_code = self.get_mu(color)

                for y in range(int(y1), int(y2)):
                    for x in range(int(x1), int(x2)):
                        if ((x - center_x) / radius_x)**2 + ((y - center_y) / radius_y)**2 <= 1:
                            matrix[y][x] = color_code

            elif self.dragNdropCanvas.type(obj) == "line":
                coordinates = self.dragNdropCanvas.coords(obj)
                color = self.dragNdropCanvas.itemcget(obj, "fill")
                color_code = self.get_mu(color)

                width = 5
                for i in range(0, len(coordinates) - 2, 2):
                    x1, y1, x2, y2 = coordinates[i], coordinates[i + 1], coordinates[i + 2], coordinates[i + 3]
                    line_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    unit_vector = ((x2 - x1) / line_length, (y2 - y1) / line_length)

                    for j in range(int(line_length)):
                        x = int(x1 + j * unit_vector[0])
                        y = int(y1 + j * unit_vector[1])

                        for k in range(-width // 2, (width + 1) // 2):
                            for l in range(-width // 2, (width + 1) // 2):
                                if 0 <= y + k < 600 and 0 <= x + l < 600:
                                    matrix[y + k][x + l] = color_code

        return matrix
    


    def get_mu(self, color):
        # define mu for each color that depeds on the material chosen
        color_codes = {
            "blue": (math.log(2)/self.spectra.get_hvl('Water, Liquid')),  
            "red": (math.log(2)/self.spectra.get_hvl('Blood (ICRP)')),
            "pink": (math.log(2)/self.spectra.get_hvl('Tissue, Soft (ICRP)')),
            "light gray": (math.log(2)/self.spectra.get_hvl('Bone Substitute (SB3)')),
            "white": (math.log(2)/self.spectra.get_hvl('Air Dry (Near Sea Level)')),  
            "purple": (math.log(2)/self.spectra.get_hvl('Kidney (ICRU)')),
            "black": (math.log(2)/self.spectra.get_hvl('Pb')),
            "gray": (math.log(2)/self.spectra.get_hvl('Al')),
        }
        return color_codes.get(color, 0)
    
    def toggle_color(self):
        current_color = self.simulation_speed_fast_btn.cget("bg")
        new_color = "green" if current_color == "gray" else "gray"
        self.simulation_speed_fast_btn.config(bg=new_color)
        self.simulation_speed_slow_btn.config(bg=current_color)
    
    def on_checkbox_clicked(self):
        if self.noSimulationChecked.get():
            self.simulation_speed_fast_btn.place_forget()
            self.simulation_speed_slow_btn.place_forget()
        else:
            self.simulation_speed_fast_btn.place(relx=0.77, rely=0.8, relwidth=0.1, relheight=0.05, anchor="nw")
            self.simulation_speed_slow_btn.place(relx=0.87, rely=0.8, relwidth=0.1, relheight=0.05, anchor="nw")

    def closeWindow(self):
        self.master.state('zoomed')
        self.destroy()
        
  
    
        
        
    