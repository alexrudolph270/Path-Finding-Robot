## First pass at implementing the auto-map-mode with the sonic sensors
## fucking here goes nothing
## Alex Rudolph

## At its most base, this should allow the robot to move until it perceives an
## object.  Once the object finds it cannot move any further, it will backup,
## turn around, and move in a new direction until it hits another object and the
## process repeats

from gopigo import *
import time

## main processes

## Initialize the matrix
i, j = 100, 100
map_mtx = [[0 for x in range(i)] for y in range(j)]

map_mtx[0][0] = 1

## print(map_mtx[0][0]) test

## print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in map_mtx]))
## Will be used, prints out the entire matrix

## auto movement
min_distance = 80 ## we can narrow down the best number later

def_mapmode():
  no_wall = true ## There is no object in the robots way
  while no_wall:
    dist = us_dist(15)  ## enable the ultrasonic sensor(s)
    if dist > min_distance:
        print("FWD OK", dist)
        fwd()
        time.sleep(1)
    else:
        printf("OBSTRUCTION DETECTED", dist)
        stop()
        bwd()
        time.sleep(.5)
        stop()
        right_rot()
        time.sleep(.5)
        stop()
## Code for adding the map should go here
## Can use the autonomy method to fill the map.  Every time a wall is hit
## a space in the matrix will be filled


## end of definitions

stop()
map_mode()
