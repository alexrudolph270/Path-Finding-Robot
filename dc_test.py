'''
    Note:   Uncomment gopigo import and movement controls if you want to
    test this code on the robot.
    '''

import tkinter as tk
import time
from threading import Thread
#from gopigo import *

done = 1                # Check if robot is done moving.
first_key = None        # Initial key pressed.
current_key = None      # Used to check if current key is same as initial.

'''
    check() will check if the user is holding down a key. Currently, we are
    only testing keys 'w' and 's'.
    '''
def check():
    '''
        Change this delay variable for a different delay time.
        Note: The lower the delay, the more accurately it will stop; however,
        there is also a higher likeliness of "stuttering" in the beginning.
        Stuttering is when the robot moves forward, stops immediately, and then
        continues to move forward.
        The delay time may vary between computers depending on the OS.
        This is because of repeating input when a key is held down.
        '''
    delay = 0.1
    
    global current_key
    global done

    command.bind_all("<KeyPress>", setInput)
    
    time.sleep(delay)
    
    #print(current_key)
    if current_key == None:
        print("Stop the robot!")
        # stop()
        done = 1
        command.bind_all("<KeyPress>", key_input)
    
    elif current_key == first_key:
        print("Keep going in " + current_key + " direction.")
        current_key = None      # Resetting the key to None to wait for another input.
        check()
    
    else:
        print("Moving in a different direction.")
        done = 1
        command.bind_all("<KeyPress>", key_input)

'''
setInput(event) will set current_key to whatever the user last pressed.
'''
def setInput(event):
    global current_key
    key_press = event.keysym.lower()
    current_key = key_press

def key_input(event):
    global done
    global first_key
    key_press = event.keysym.lower()
    
    if key_press == 'w':
        first_key = key_press
        if done == 1:
            done = 0
            print("Robot is moving forward.")
            #fwd()
        
        Thread(target=check).start()
    
    elif key_press == 's':
        first_key = key_press
        if done == 1:
            done = 0
            print("Robot is moving backwards.")
            #bwd()
        
        Thread(target=check).start()


command = tk.Tk()
command.bind_all("<KeyPress>", key_input)
command.mainloop()
