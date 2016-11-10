###############################################################################
## Map Mode gui output testing
##  latest version just cleans up unnecessary code and adds relevant comments
##  this version will be running on the client side, and will await a matrix from
##  map mode on the robot to display. Not sure exactly how that's supposed to
##  happen. This version will be mashed into main as its own class very soon!
#####################################################################t#########
from tkinter import *
###############################################################################
m = [[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ','x','x',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ','x',' ',' ','x',' ',' ',' '],
    [' ',' ',' ',' ',' ','x',' ',' ',' ','x',' ',' '],
    [' ','x',' ',' ',' ','x',' ',' ','x',' ',' ',' '],
    ['x',' ','x',' ',' ','x','x',' ',' ','x',' ',' '],
    ['x',' ','x',' ',' ',' ',' ','x',' ','x',' ',' '],
    ['x',' ',' ','x','x','x','x',' ',' ',' ','x',' '],
    [' ','x',' ',' ',' ',' ',' ',' ',' ',' ','x',' '],
    [' ','x',' ','x','x','x',' ',' ','x','x',' ',' '],
    [' ',' ','x',' ',' ',' ','x','x',' ',' ',' ',' ']]

weem = []

#dimensions of window are dependant of dimensions of canvas
#  canvas is NOT dynamic at the moment, matrices with very different
#  length and width will appear stretched depending on the difference
canvasX = 900
canvasY = 900

# removes rows with no relevant data
for x in m:
    if('x' in x):
        weem.append(x)

min_y = 9999 # arbitrarily high
max_y = 0 #arbitrarily low, no negs.

#slices remaining rows based on leftmost(min_y) relevant data and
#  rightmost(max_y) relevant data
for x in weem:
    for y in range (len(x)):
        if(x[y] == 'x'):
            if(min_y > y):
                min_y = y
            if(max_y < y):
                max_y = y

for x in range(len(weem)):
    weem[x] = weem[x][min_y:max_y+1]

#determines dimensions of individual squares, the "resolution" of the mapping
xlen = int(canvasX/len(weem[0]))
ylen = int(canvasY/len(weem))

#windos/tk stuff
root = Tk()
can = Canvas(root, width=canvasX, height=canvasY)
can.pack()
#draws the squares on screen
for y in range(len(weem)):
    for x in range(len(weem[0])):
        if (weem[y][x] == ' '):
            can.create_rectangle(x*xlen, y*ylen, (x+1)*xlen, (y+1)*ylen)
        else:
            can.create_rectangle(x*xlen, y*ylen, (x+1)*xlen, (y+1)*ylen, fill="black")

mainloop()
