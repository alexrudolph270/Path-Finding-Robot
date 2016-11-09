###############################################################################
## Gui interface classes
## Made with reference to http://www.blog.pythonlibrary.org/2012/07/26/
##  tkinter-how-to-show-hide-a-window/
## Currently, only the Path Mode interface has been implemented. It is
##  suggested that class Path be used as a template for implemantation of
##  other GUI class dealies
## A lot of the comments from the previous version are missing cause laziness
##  might put them in later, maybe...
###############################################################################
import tkinter as tk
from tkinter import *
from functools import partial
from threading import Thread
import time

#from gopigo import *
########################################################################

class Direct(tk.Toplevel):
    """"""
    # ----------------------------------------------------------------------
    def __init__(self, original):
        print("Entering Direct Mode!")
        """Constructor"""
        self.original_frame = original
        tk.Toplevel.__init__(self)
        self.title("Direct Mode")

        self.done = 1               # Check if robot is done moving.
        self.first_key = None       # Initial key pressed.
        self.current_key = None     # Used to check if current key is same as initial.
        self.delay = 0.3            # Delay time for check().

        # List of acceptable inputs.
        self.accept = ['q', 'w', 'e', 'a', 's', 'd']

        #check self before rek self
        root.bind_all("<KeyPress>", self.key_input)

        # Instructions
        tk.Label(self, text="  ======================================  \n"
                            "||  Control Rob the Robot with your KEYBOARD!  ||  \n"
                            "  ======================================  ").grid(column = 1, columnspan = 11)

        # Movement directions
        tk.Label(self, text="W to move forward\n"
                            "A to move left\n"
                            "S to move right\n"
                            "D to move backwards\n"
                            "Q to rotate left\n"
                            "E to rotate right\n").grid(column = 1, columnspan = 11)

        # Movement indicator
        tk.Label(self, text="Q").grid(row = 10, column = 5)
        tk.Label(self, text="W").grid(row = 10, column = 6)
        tk.Label(self, text="E").grid(row = 10, column = 7)
        tk.Label(self, text="A").grid(row = 11, column = 5)
        tk.Label(self, text="S").grid(row = 11, column = 6)
        tk.Label(self, text="D").grid(row = 11, column = 7)

        # Space
        tk.Label(self, text="\n\n").grid()

        # Allow user to change the delay value.
        tk.Label(self, text="Delay =").grid(row=12, column=5)
        self.entry = StringVar(self, value=str(self.delay))

        # Check if entry is valid number.
        vcmd = (self.register(self.onValidate), '%P')

        # Entry box. Default delay is set initially.
        self.delay_box = tk.Entry(self, textvariable=self.entry, width=5, validate="key",
                                  validatecommand = vcmd).grid(row=12, column=6)

        # Set delay button
        tk.Button(self, text="Set", command=self.set_delay).grid(row=12, column=7)

        # Back button
        tk.Button(self, text = "Back", command = self.onClose).grid(row = 13, column = 6)

        # Space
        tk.Label(self, text="\n").grid()

        # Pressing the x button will return to the Main Menu.
        self.protocol('WM_DELETE_WINDOW', self.onClose)

    # ----------------------------------------------------------------------

    '''
    Check if what is being typed in the entry box is a number.
    '''
    def onValidate(self, delay_value):
        # Add 0 in front to allow user to backspace all the way and clear the box.
        delay_value = "0" + delay_value
        try:
            float(delay_value)
            return True
        except ValueError:
            return False

    '''
    Set a new delay time.
    '''
    def set_delay(self):
        try:
            self.delay = float(self.entry.get())
        except:
            self.delay = 0

        print("Setting delay to " + str(self.delay) + ".")

    '''
    This function will run if the user presses a key.
    If the key is not a valid key, robot will stop and nothing will happen.
    Otherwise, highlight key currently being pressed and move the robot.
    '''
    def key_input(self, event):
        key_press = event.keysym.lower()

        if key_press not in self.accept:
            #print(key_press, "is not a valid input! Stop.")
            self.done = 1
            #stop()
        else:
            color = "green"
            self.first_key = key_press
            if key_press == 'w':
                if self.done == 1:
                    self.done = 0
                    tk.Label(self, text="W", bg=color).grid(row=10, column=6)
                    print("Robot is moving forward.")
                    #fwd()
            elif key_press == 'a':
                if self.done == 1:
                    self.done = 0
                    tk.Label(self, text="A", bg=color).grid(row=11, column=5)
                    print("Robot is moving left.")
                    #left()
            elif key_press == 's':
                if self.done == 1:
                    self.done = 0
                    tk.Label(self, text="S", bg=color).grid(row=11, column=6)
                    print("Robot is moving backwards.")
                    #bwd()
            elif key_press == 'd':
                if self.done == 1:
                    self.done = 0
                    tk.Label(self, text="D", bg=color).grid(row=11, column=7)
                    print("Robot is moving right.")
                    #right()
            elif key_press == 'q':
                if self.done == 1:
                    self.done = 0
                    tk.Label(self, text="Q", bg=color).grid(row=10, column=5)
                    print("Robot is rotating left.")
                    #left_rot()
            elif key_press == 'e':
                if self.done == 1:
                    self.done = 0
                    tk.Label(self, text="E", bg=color).grid(row=10, column=7)
                    print("Robot is rotating right.")
                    #right_rot()

            Thread(target=self.check).start()

    '''
    This function will determine if the robot should stop.
    It stops if it receives None as an input after a delay (which may be set).
    '''
    def check(self):
        root.bind_all("<KeyPress>", self.set_input)

        time.sleep(self.delay)

        print(self.current_key)

        # If current_key is None, robot will stop.
        if self.current_key == None:
            self.reset_colors()
            # Robot will come to a stop.
            print("Stop the robot!")
            # stop()
            self.done = 1

            root.bind_all("<KeyPress>", self.key_input)

        # Check if current_key is the same as the initial one. Keeps going if so.
        elif self.current_key == self.first_key:
            # Robot keeps going in current direction.
            self.current_key = None  # Resetting the key to None to wait for another input.
            self.check()

        # If keys are different, then the direction is changing.
        # Stop the robot before moving in another direction.
        # Minor bug: Robot will not move in other direction if key is tapped once (must hold).
        else:
            self.reset_colors()
            # Changing directions.
            self.done = 1
            print("Stop the robot!")
            #stop()

            root.bind_all("<KeyPress>", self.key_input)


    '''
    This function sets the current key to the one that is currently being pressed.
    '''
    def set_input(self, event):
        self.current_key = event.keysym.lower()


    '''
    This function should reset the highlights to default.
    '''
    def reset_colors(self):
        color = "white"
        tk.Label(self, text="W", bg=color).grid(row=10, column=6)
        tk.Label(self, text="A", bg=color).grid(row=11, column=5)
        tk.Label(self, text="S", bg=color).grid(row=11, column=6)
        tk.Label(self, text="D", bg=color).grid(row=11, column=7)
        tk.Label(self, text="Q", bg=color).grid(row=10, column=5)
        tk.Label(self, text="E", bg=color).grid(row=10, column=7)


    '''
    This function should close out of Direct Mode.
        - Robot will stop moving (if it isn't stopped already.)
        - Will unbind current keys.
        - Destroy frame and return to Main Menu.
    '''
    # Bug: Lots of errors if you exit in the middle of pressing a key.
    # Thread still continues and frame is being destroyed before it ends.
    def onClose(self):
        """"""
        # Stop the robot if it isn't already stopped.
        if self.done != 1:
            print("Exiting, stopping robot!")
            #stop()

        print("Returning to Main Menu!")
        root.unbind_all("<KeyPress>")
        self.destroy()
        self.original_frame.show()



class Path(tk.Toplevel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, original):
        """Constructor"""
        self.original_frame = original
        tk.Toplevel.__init__(self)
        self.title("Path Mode")
        self.pathButtons = []
        self.path = []
        self.orderindex = 0

        # Instantiation of grid and start buttons
        for x in range(self.dimensions()):
            col = []
            for y in range(self.dimensions()):
                butt = tk.Button(self ,text=" ", command=partial(self.clickpath, x, y))
                butt.grid(column=x, row=y)
                col.append(butt)
            self.pathButtons.append(col)

        start = tk.Button(self, text="Start", command=self.clickstart).grid(
            column=(int(self.dimensions() / 2)-1), row=(self.dimensions()+1),
            columnspan=2)

        back = tk.Button(self, text="Back", command=self.onClose).grid(
            column=(int(self.dimensions() / 2)+1), row=(self.dimensions()+1),
            columnspan=2)

        # Pressing the x button will return to the Main Menu.
        self.protocol('WM_DELETE_WINDOW', self.onClose)

    #----------------------------------------------------------------------
    def onClose(self):
        """"""
        self.destroy()
        self.original_frame.show()

    def dimensions(self):
        return 20

    def clickpath(self, x, y):
        #function to do stuff with index of button on grid/list
        global orderindex #needed to access global variable
        but = self.pathButtons[x][y] #acces button from grid buttons
        if(but.cget('text') == self.orderindex): # if button has text tag
            but.configure(text=" ") #set it blank
            self.path.pop() #remove last patth[] element (coordinate)
            self.orderindex -= 1
        elif(but.cget('text') == ' '):
            but.configure(text=self.orderindex+1) #add order index to button text tag
            self.path.append([x, y]) #append
            self.orderindex += 1

    def clickstart(self):
        # executes start button function(s)
        # for debug purposes at this point
        # will eventually send list of coordinates to the 'directions' module
        print(self.path)
        print(self.orderindex)
    # Instantiation of grid and start buttons

########################################################################
class Menu(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("Gogo Robo Maaaaaaaaaaaaaaaania~")
        self.frame = tk.Frame(parent)
        self.frame.pack()

        dButt = tk.Button(self.frame, text="Direct Mode", command=self.openDirect)
        pButt = tk.Button(self.frame, text="Path Mode", command=self.openPath)
        mButt = tk.Button(self.frame, text="Map Mode", command=self.openMap)
        dButt.pack()
        pButt.pack() #lol
        mButt.pack()

    #----------------------------------------------------------------------
    def hide(self):
        """"""
        self.root.withdraw()

    #----------------------------------------------------------------------
    #Open methods all open path mode till others are implemented
    def openDirect(self):
        """"""
        self.hide()
        subFrame = Direct(self)

    #----------------------------------------------------------------------
    def openPath(self):
        """"""
        self.hide()
        subFrame = Path(self)

    #----------------------------------------------------------------------
    def openMap(self):
        """"""
        self.hide()
        subFrame = Path(self)

    #----------------------------------------------------------------------
    def show(self):
        """"""
        self.root.update()
        self.root.deiconify()

#----------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    main = Menu(root)
    root.mainloop()




