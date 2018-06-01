#! /usr/bin/python

# Libraries importation
#######################

import configparser
import servo


# Configuration importation
###########################

config = configparser.ConfigParser()
config.read("config.ini")
SERVO_NAME_LIST = config["SERVO"]["SERVO_LIST"].split(", ")


# Main code
###########

# Gui declaration
gui = servo.Gui()

# Servo declaration
servo_list = []
for x in SERVO_NAME_LIST:
    servo_list.append(servo.Servo(x, gui.root, SERVO_NAME_LIST.index(x)))

# GUI servo objects declaration
gui.buildServoObjects(servo_list)

# GUI Grid
gui.guiGrid()

# GUI startup
gui.start()















        