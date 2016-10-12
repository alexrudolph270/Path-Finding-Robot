# Path Mode GUI dealy
# currently breaks if you try to backtrack out of order
# works otherwise
# prints alist of path elements(coordinates) so far, final version will send 
#	list to the direction module

#  to change grid "resolution" change x and y ranges in instantiation


from tkinter import *
from functools import partial

window = Tk()

# holds buttons in a 2d list
pathButtons = []
# keeps 2d list of coordinates representing the path to take
path = []
# used for keeping track of selection/deselection
order = [] #might not be necessary
# keeps track of number of path buttons selected to maintain order
orderindex = 0

def dimensions():
	## Determines the dimensions of the grid, always squared
	#    unless we decide to change that further on
	return 20

def clickpath(x, y):
	#function to do stuff with index of button on grid/list
	global orderindex #needed to access global variable
	but = pathButtons[x][y] #acces button from grid buttons
	if(but.cget('text') == orderindex): # if button has text tag
		but.configure(text=" ") #set it blank
		order.pop() #remove last order[] element (order of coordinates)
		path.pop() #remove last patth[] element (coordinate)
		orderindex -= 1
	else:
		but.configure(text=orderindex+1) #add order index to button text tag
		order.append(orderindex+1) #append order index to order[]
		path.append([x, y]) #append coordinates to path[]
		orderindex += 1 

def clickstart():
	# executes start button function(s)
	# for debug purposes at this point
	# will eventually send list of coordinates to the 'directions' module
	print(path)
	print(orderindex)
	print(order)

# Instantiation of grid and start buttons
for x in range(dimensions()):
	col = []
	for y in range(dimensions()):
		butt = Button(window ,text=" ", command=partial(clickpath, x, y))
		butt.grid(column=x, row=y)
		col.append(butt)
	pathButtons.append(col)

start = Button(window, text="Start", command=clickstart).grid(
	column=(int(dimensions() / 2)), row=(dimensions()+1), columnspan=2)

window.mainloop()