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

done = 1  # Check if robot is done moving.
first_key = None  # Initial key pressed.
current_key = None  # Used to check if current key is same as initial.

'''
    check() will check if the user is holding down a key. Currently, we are
    only testing keys 'w' and 's'.
    '''

def key_input(event):
    global done
    global first_key
    key_press = event.keysym.lower()

    print(key_press)

    if key_press == 'w':
        first_key = key_press
        if done == 1:
            done = 0
            print("Robot is moving forward.")
            #fwd()

    elif key_press == 's':
        first_key = key_press
        if done == 1:
            done = 0
            print("Robot is moving backwards.")
            # bwd()


def end(event):
    print("Stop")
    # stop()


command = tk.Tk()
command.bind_all("<KeyPress>", key_input)
command.bind_all("<KeyRelease>", end)
command.mainloop()

os.system("xset r on")
