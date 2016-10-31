## First pass at implementing the auto-map-mode with the sonic sensors
## fucking here goes nothing
## Alex Rudolph

## edited by Bailey Durkin (10/31)
## The robot should now be able to make use of both sensors to navigate the
## perimeter of a room and HOPEFULLY map it out on a matrix, provided the
## silly toy wheels and motors can get it there.

from gopigo import *
import time

## main processes

## Initialize the matrix
i, j = 100, 100
map_mtx = [[0 for x in range(i)] for y in range(j)]

## 0 0 0 0 0 0
## 0 X - - > 0
## 0 0 0 0 0 0
## 0 0 0 0 0 0
## 0 0 0 0 0 0
## 
## this code assumes the robot will start in the top left corner of the room
## robot will move clockwise around the room  (starts facing right, relative to the matrix)

## auto movement
WALL = 20       # Minimum distance (in cm) for wall
MOVE_DIST = 15  # Number of clicks to move (1 click ~= 1.13 cm) ## WALL > MOVE_DIST * 1.13 ##
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

## Set start parameters
current_x = 1
current_y = 1           # robot starts at (1,1)  <-- we might have to change this if the room is weird shaped
current_d = RIGHT       # robot starts facing right
end_x = current_x
end_y = current_y + 1   # robot should hopefully end one unit below its starting position

## map_mtx[0][0] = 1

## print(map_mtx[0][0]) test

## print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in map_mtx]))
## Will be used, prints out the entire matrix

def map_mode():
    enable_encoders()
    set_speed(50)
    dist_front = us_dist(15)  ## enable the ultrasonic sensor(s)
    dist_left = us_dist(10)   ## 15 = front, 10 = left
    while current_x != end_x and current_y != end_y:
        if dist_left <= WALL: # wall to the left
            print("\nWall detected, adding to matrix", dist_left)
            if (current_d == UP):
                map_mtx[current_x - 1][current_y] = 1
            elif (current_d == RIGHT):
                map_mtx[current_x][current_y - 1] = 1
            elif (current_d == DOWN):
                map_mtx[current_x + 1][current_y] = 1
            elif (current_d == LEFT):
                map_mtx[current_x][current_y + 1] = 1
            else:
                printf("\nERROR: invalid direction")

            if dist_front > WALL: # no wall in front
                print("\nNo obstruction detected, moving forward", dist_front)
                enc_tgt(1,1,move_dist)
                fwd()
                time.sleep(3)
                stop()

                # update current position
                if (current_d == UP):
                    current_y = current_y - 1
                elif (current_d == RIGHT):
                    current_x = current_x + 1
                elif (current_d == DOWN):
                    current_y = current_y + 1
                elif (current_d == LEFT):
                    current_x = current_x - 1
                else:
                    printf("\nERROR: invalid direction")
                    
            else: # wall in front
                printf("\nObstruction detected, making right turn", dist_front)
                enc_tgt(0,1,9)
                right_rot()
                time.sleep(3)
                enc_tgt(1,1,move_dist)
                fwd()
                time.sleep(3)
                stop()

                # update current position
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
                    printf("\nERROR: invalid direction")
                
        else: # no wall to the left
            print("\nNo wall detected, making left turn", dist_left)
            enc_tgt(1,0,9)
            left_rot()
            time.sleep(3)
            enc_tgt(1,1,move_dist)
            fwd()
            time.sleep(3)
            stop()

            # update current position
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
                printf("\nERROR: invalid direction")

    # outside of while loop
    print("\nMapping complete.")
    print("\nPrinting matrix...")
    # print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in map_mtx]))

## end of definitions

stop()
map_mode()
