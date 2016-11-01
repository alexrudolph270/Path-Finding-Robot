'''
    Note:   Uncomment gopigo import and movement controls if you want to
    test this code on the robot.
'''

import tkinter as tk
from threading import Thread
import time
import os

# from gopigo import *

os.system("xset r off")

done = 1

def end(event):
    global done
    done = 1
    print("Stop")
    #stop()

def key_input(event):
    global done
    key_press = event.keysym.lower()

    print(key_press)
    
    while done != 1:
        if key_press == 'w':
            done = 0
            print("Robot is moving forward.")
            #fwd()

        elif key_press == 's':
            done = 0
            print("Robot is moving backwards.")
            #bwd()
        
        command.bind_all("<KeyRelease>", end)

command = tk.Tk()
command.bind_all("<KeyPress>", key_input)
command.mainloop()

os.system("xset r on")
