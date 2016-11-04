## edited by Bailey Durkin (10/31)
## The robot should now be able to make use of both sensors to navigate the
## perimeter of a room and HOPEFULLY map it out on a matrix, provided the
## silly toy wheels and motors can get it there.

from gopigo import *
import time

## Initialize the matrix
i, j = 100, 100
map_mtx = [[0 for x in range(i)] for y in range(j)]

## Define constants
WALL = 50       # Minimum distance (in cm) for wall
MOVE_DIST = 36  # Number of clicks to move (1 click ~= 1.13 cm) ## WALL > MOVE_DIST * 1.13 ##
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
MOVE_FORWARD = 0
MOVE_RIGHT = 1
MOVE_LEFT = 2

## Set start parameters
current_x = 1
current_y = 1           # robot starts at (1,1)  <-- we might have to change this if the room is weird shaped
current_d = RIGHT       # robot starts facing right
start_x = -1
start_y = -1              # set 

def map_mode():
    
    global current_x
    global current_y
    global current_d
    global start_x
    global start_y
    
    # global RIGHT
    # global LEFT
    # global UP
    # global DOWN
    # global WALL
    # global MOVE_DIST
    
    set_speed(200)
    while True:
        dist_left = us_dist(10) # get distance from left sensor
        if dist_left <= WALL: # wall to the left
            print("Wall detected, adding to matrix", dist_left)

            # update the matrix
            if (current_d == UP):
                map_mtx[current_x - 1][current_y] = 1
            elif (current_d == RIGHT):
                map_mtx[current_x][current_y - 1] = 1
            elif (current_d == DOWN):
                map_mtx[current_x + 1][current_y] = 1
            elif (current_d == LEFT):
                map_mtx[current_x][current_y + 1] = 1
            else:
                printf("ERROR: invalid direction")

            dist_front = us_dist(15) # get distance from front sensor
            if dist_front > WALL: # no wall in front
                print("No obstruction detected, moving forward", dist_front)

                # move forward, and stop
                enc_tgt(1,1,MOVE_DIST)
                fwd()
                time.sleep(2)
                stop()

                # update current position
                updatePos(MOVE_FORWARD)

            else: # wall in front
                print("Obstruction detected, making right turn", dist_front)

                # turn right
                enc_tgt(0,1,9)
                right_rot()
                time.sleep(1.5)

                # move forward and stop
                enc_tgt(1,1,MOVE_DIST)
                fwd()
                time.sleep(2)
                stop()

                # update current position
                updatePos(MOVE_RIGHT)

        else: # no wall to the left
            print("No wall detected, making left turn", dist_left)

            # turn left
            enc_tgt(1,0,9)
            left_rot()
            time.sleep(1.5)

            # move forward and stop
            enc_tgt(1,1,MOVE_DIST)
            fwd()
            time.sleep(2)
            stop()

            # update current position
            updatePos(MOVE_LEFT)

    # outside of while loop
    print("Mapping complete.")
    print("Printing matrix...")
    # print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in map_mtx]))

def updatePos(move_direction)
    if (move_direction = MOVE_FORWARD)
        if (current_d == UP):
            current_y = current_y - 1
        elif (current_d == RIGHT):
            current_x = current_x + 1
        elif (current_d == DOWN):
            current_y = current_y + 1
        elif (current_d == LEFT):
            current_x = current_x - 1
        else:
            print("ERROR: invalid direction")
            
    elif (move_direction = MOVE_RIGHT)
        if (current_d == UP):
            current_d = RIGHT
            current_x = current_x + 1
        elif (current_d == RIGHT):
            current_d = DOWN
            current_x = current_y + 1
        elif (current_d == DOWN):
            current_d = LEFT
            current_y = current_x - 1
        elif (current_d == LEFT):
            current_d = UP
            current_x = current_y - 1
        else:
            print("ERROR: invalid direction")
        
    elif (move_direction = MOVE_LEFT)
        if (current_d == UP):
            current_d = LEFT
            current_y = current_x - 1
        elif (current_d == RIGHT):
            current_d = UP
            current_x = current_y - 1
        elif (current_d == DOWN):
            current_d = RIGHT
            current_x = current_x + 1
        elif (current_d == LEFT):
            current_d = DOWN
            current_x = current_y + 1
        else:
            print("ERROR: invalid direction")
            
    else print("ERROR: invalid movement direction")
        
    
## end of definitions

stop()
map_mode()
