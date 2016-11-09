###############################################################################
## Map Mode gui output testing
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

canvasX = 900
canvasY = 900

min_y = 9999 # arbitrarily high
max_y = 0 #arbitrarily low, no negs.

for x in m:
    if('x' in x):
        weem.append(x)

#for x in weem:
#    print(x)

for x in weem:
    for y in range (len(x)):
        if(x[y] == 'x'):
            if(min_y > y):
                min_y = y
            if(max_y < y):
                max_y = y

print(min_y, max_y)
for x in range(len(weem)):
    weem[x] = weem[x][min_y:max_y+1]

for x in weem:
    print(x)

xlen = int(900/len(weem[0]))
ylen = int(900/len(weem))

print(xlen, ylen)

root = Tk()

can = Canvas(root, width=900, height=900)
can.pack()

counter = 1
for y in range(len(weem)):
    for x in range(len(weem[0])):
        if (weem[y][x] == ' '):
            can.create_rectangle(x*xlen, y*ylen, (x+1)*xlen, (y+1)*ylen)
            print(x, y)
        else:
            can.create_rectangle(x*xlen, y*ylen, (x+1)*xlen, (y+1)*ylen, fill="black")
            print(x, y)
        counter += 1

#can.create_rectangle(0,0,300,300, fill="red")
#can.create_rectangle(300,0,600,300, fill="black")
#can.create_rectangle(0,300,300,600, fill="black")
#can.create_rectangle(300,300,600,600, fill="red")

mainloop()
