## Bailey Durkin & Alex Rudolph
## The robot should now be able to make use of both sensors to navigate the
## perimeter of a room and HOPEFULLY map it out on a matrix, provided the
## silly toy wheels and motors can get it there.

from gopigo import *
import time

## Initialize the matrix
i, j = 100, 100
map_mtx = [['-' for x in range(i)] for y in range(j)]

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
current_x = 50
current_y = 50          # robot starts in the middle of the matrix
current_d = UP          # robot starts facing UP; top of matrix is relative to robots starting orientation
start_x = -1
start_y = -1

def map_mode():
    # import globals that need to be modified (read-only variables don't need to be imported)
    global current_x
    global current_y
    global current_d
    global start_x
    global start_y

    # set speed of the robot, slower is probably more accurate
    set_speed(200)

    ## the robot can start from anywhere in the room
    ## robot will drive forward until it reaches a wall
    ## and then orient itself to the wall
    wall_found = False
    while (wall_found != True):
        dist_left = us_dist(10)
        dist_front = us_dist(15)
        if (dist_left > WALL and dist_front > WALL):  # no wall found      
            # move forward, and stop
            enc_tgt(1,1,MOVE_DIST)
            fwd()
            time.sleep(3)
            stop()

            # update current position
            updatePos(MOVE_FORWARD)
            
        else: # wall found
            wall_found = True
            
            # set current position as the start position
            start_x = current_x
            start_y = current_y
            print("Start position is now (", start_x, ",", start_y, ")")

    if (dist_front == WALL):
        # turn right
        enc_tgt(0,1,9)
        right_rot()
        time.sleep(3)
        current_d = RIGHT # robot starts facing UP, but is now facing RIGHT 

    ## the robot is now oriented to the wall
    # add adjacent wall to matrix
    addWall()

    ## now we move the robot one unit forward
    # move forward, and stop
    enc_tgt(1,1,MOVE_DIST)
    fwd()
    time.sleep(3)
    stop()

    # update current position
    updatePos(MOVE_FORWARD)

    ## now that the start position is different from the current position
    ## we can use the current position and the start position as the stop condition
    
    x = 0    
    while (current_x != start_x and current_y != start_y):
        x = x + 1
        dist_left = us_dist(10) # get distance from left sensor
        if (dist_left <= WALL): # wall to the left
            print("Wall detected, adding to matrix; dist_left = ", dist_left)

            # update the matrix
            addWall()

            dist_front = us_dist(15) # get distance from front sensor
            if (dist_front > WALL): # no wall in front
                print("No obstruction detected, moving forward; dist_front = ", dist_front)

                # move forward, and stop
                enc_tgt(1,1,MOVE_DIST)
                fwd()
                time.sleep(3)
                stop()

                # update current position
                updatePos(MOVE_FORWARD)

            else: # wall in front
                print("Obstruction detected, making right turn; dist_front = ", dist_front)

                # turn right
                enc_tgt(0,1,9)
                right_rot()
                time.sleep(3)

                # move forward and stop
                enc_tgt(1,1,MOVE_DIST)
                fwd()
                time.sleep(3)
                stop()

                # update current position
                updatePos(MOVE_RIGHT)

        else: # no wall to the left
            print("No wall detected, making left turn; dist_left = ", dist_left)

            # turn left
            enc_tgt(1,0,9)
            left_rot()
            time.sleep(3)

            # move forward and stop
            enc_tgt(1,1,MOVE_DIST)
            fwd()
            time.sleep(3)
            stop()

            # update current position
            updatePos(MOVE_LEFT)

    ## outside of while loop
    print("Mapping complete.")
    print("Printing matrix...")
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
        for row in map_mtx]))

def addWall()
    # import globals that need to be modified
    global map_mtx

    if (current_d == UP):
        map_mtx[current_x - 1][current_y] = X
        print("(", current_x - 1, ",", current_y, ") added to matrix")
    elif (current_d == RIGHT):
        map_mtx[current_x][current_y - 1] = X
        print("(", current_x, ",", current_y - 1, ") added to matrix")
    elif (current_d == DOWN):
        map_mtx[current_x + 1][current_y] = X
        print("(", current_x + 1, ",", current_y, ") added to matrix")
    elif (current_d == LEFT):
        map_mtx[current_x][current_y + 1] = X
        print("(", current_x, ",", current_y + 1, ") added to matrix")
    else:
        print("ERROR: invalid direction")

def updatePos(move_direction)
    # import globals that need to be modified
    global current_x
    global current_y
    global current_d

    if (move_direction = MOVE_FORWARD):
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

        print("Current position is now (", current_x, ",", current_y, "); direction = ", current_d)

    elif (move_direction = MOVE_RIGHT):
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

        print("Current position is now (", current_x, ",", current_y, "); direction = ", current_d)
        
    elif (move_direction = MOVE_LEFT):
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

        print("Current position is now (", current_x, ",", current_y, "); direction = ", current_d)
            
    else:
        print("ERROR: invalid movement direction")
        
    
## end of definitions

stop()
map_mode()
