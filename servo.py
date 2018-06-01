#! /usr/bin/python

# Libraries importation
#######################

import configparser
from tkinter import *
from tkinter.ttk import *
import time
# import Adafruit_PCA9685


# Configuration importation
###########################

config = configparser.ConfigParser()
config.read("config.ini")
SERVO_NAME_LIST = config["SERVO"]["SERVO_LIST"].split(", ")
SERVO_AMOUNT = len(SERVO_NAME_LIST)


# Class definition
##################
class Gui:
    """ Class for GUI management of servo. """

    def __init__(self):
        """ Constructor for GuiManagement, building:
        - Root;
        - Fixed objects (not depending on servo declaration). """

        # GUI main definitions
        ###################

        # Main window declaration
        self.root = Tk()
        self.root_height = 140 + SERVO_AMOUNT*40
        self.root_geometry = "+800+400"
        self.root.geometry(self.root_geometry)
        self.root.title("Servo supervision")

        # GUI objects definition
        self.lb_title = Label(self.root, text = "Servo list: ")
        self.lb_title.config(font = ("bold"))
        self.lb_stub = Label(self.root, text = "Stub")
        self.lb_stub.config(font = ("bold"))
        self.lb_request = Label(self.root, text = "Enter a position: ")
        self.en_request = Entry(self.root)
        self.bt_quit = Button(self.root, text = "Quit", command = self.root.quit)

        # Variables definition for GUI interactions
        self.servo_selected = StringVar()


    def buildServoObjects(self, ServoList):
        """ Building objects of GUI needing the servo declaration. """

        self.cmb_servo = Combobox(self.root, textvariable = self.servo_selected, values = SERVO_NAME_LIST, state = "readonly")
        self.cmb_servo.set(SERVO_NAME_LIST[0])
        self.bt_validate = Button(self.root, text = "Validate", command = lambda : ServoList[self.cmb_servo.current()].gotopos(int(self.en_request.get())))
        self.root.bind("<Return>", lambda ReturnEvent : ServoList[self.cmb_servo.current()].gotopos(int(self.en_request.get())))

    
    def guiGrid(self):
        """ Build grid for main GUI. """

        # GUI objects grid 
        ##################
        self.lb_title.grid(row = 0, column = 0)
        self.lb_stub.grid(row = 0, column = 2)
        self.cmb_servo.grid(row = SERVO_AMOUNT +1, columnspan = 3)
        self.lb_request.grid(row = SERVO_AMOUNT + 2, columnspan = 3)
        self.en_request.grid(row = SERVO_AMOUNT + 3, columnspan = 3)
        self.bt_validate.grid(row = SERVO_AMOUNT + 4, columnspan = 3)
        self.bt_quit.grid(row = SERVO_AMOUNT + 5, columnspan = 3)

    def start(self):
        """ Starting GUI main loop.
        Once done, the GUI cannot be modified anymore."""

        # GUI startup
        #############
        self.root.mainloop()


class Servo:
    """ Class defining a servo with the following attributes:
    - Text definition;
    - window to be diplayed in;
    - id. """

    def __init__(self, text_def, window, id):
        """ Constructor definition """
        # Main attributes definition
        self.text_def = text_def
        self.window = window
        self.id = id
        self.current_position = IntVar()
        self.current_position.set(0)
        self.stub = IntVar()

        # GUI object definition
        lb_current = Label(self.window, text = self.text_def + " servo current value: ")
        lb_currentVar = Label(self.window, textvariable = self.current_position)
        cb_stub = Checkbutton(self.window, variable= self.stub, command = lambda : print("stub for {0} is set to {1}.".format(self.text_def, self.stub.get())))

        # GUI objects packing
        lb_current.grid(row = self.id + 1, column=0, sticky = W)
        lb_currentVar.grid(row = self.id + 1, column = 1)
        cb_stub.grid(row = self.id + 1, column = 2)
       

    def gotopos(self,requested_position):
        """ Method to give a setpoint to the servo. """

        while requested_position != self.current_position.get(): 
            if not bool(self.stub.get()):
                    print("{0} servo going to {1}.".format(self.text_def, str(requested_position)))
                    self.current_position.set(requested_position) # Debug
            else:
                if requested_position > self.current_position.get():
                    self.current_position.set(self.current_position.get() + 1)
                else:
                    self.current_position.set(self.current_position.get() - 1)
                print(self.current_position.get()) # Debug
            time.sleep(0.02)


