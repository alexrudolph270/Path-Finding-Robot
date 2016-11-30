## Bailey Durkin & Alex Rudolph
## The robot should now be able to make use of both sensors to navigate the
## perimeter of a room and HOPEFULLY map it out on a matrix, provided the
## silly toy wheels and motors can get it there.

import time

## map_mode() uses the robot and two ultrasonic sensors to navigate and create an
## apporximate map of the perimerter of a room. Coordinates are represented as 
## coordinate pairs inside a matrix. Returns the map matrix after mapping is complete.
def map_mode():
    # create globals
    global current_x
    global current_y
    global current_d
    global start_x
    global start_y
    global map_mtx

    # Initialize the matrix
    i, j = 100, 100
    map_mtx = [['-' for x in range(i)] for y in range(j)]

    # Define constants
    WALL = 25       # Minimum distance (in cm) for wall
    MOVE_DIST = 20  # Number of clicks to move (1 click ~= 1.13 cm) ## WALL > MOVE_DIST * 1.13 ##
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    MOVE_FORWARD = 0
    MOVE_RIGHT = 1
    MOVE_LEFT = 2

    # Set start parameters
    current_x = 50
    current_y = 50          # robot starts in the middle of the matrix
    current_d = UP          # robot starts facing UP; top of matrix is relative to robots starting orientation
    start_x = -1
    start_y = -1

    ## addWall() adds the wall to the left of the robot to the map matrix 
    ## relative to the robot's current position.
    def addWall():
        # import globals that need to be modified
        global map_mtx

        # add wall relative to current orientation of the robot
        if (current_d == UP):
            map_mtx[current_x - 1][current_y] = 'X'
            print("[WALL] ", current_x - 1, ",", current_y, " added to matrix")
        elif (current_d == RIGHT):
            map_mtx[current_x][current_y - 1] = 'X'
            print("[WALL] ", current_x, ",", current_y - 1, " added to matrix")
        elif (current_d == DOWN):
            map_mtx[current_x + 1][current_y] = 'X'
            print("[WALL] ", current_x + 1, ",", current_y, " added to matrix")
        elif (current_d == LEFT):
            map_mtx[current_x][current_y + 1] = 'X'
            print("[WALL] ", current_x, ",", current_y + 1, " added to matrix")
        else:
            print("[ERROR] invalid direction")
            return -1

    ## updatePos() updates the position of the robot when given a movement direction
    ## both the current position and the current direction are updated
    def updatePos(move_direction):
        # import globals that need to be modified
        global current_x
        global current_y
        global current_d

        if (move_direction == MOVE_FORWARD):
            if (current_d == UP):
                current_y = current_y - 1
            elif (current_d == RIGHT):
                current_x = current_x + 1
            elif (current_d == DOWN):
                current_y = current_y + 1
            elif (current_d == LEFT):
                current_x = current_x - 1
            else:
                print("[ERROR] invalid direction")
                return -1

            print("[DIRECTION] current direction is now ", current_d)
            print("[POSITION] Current position is now ", current_x, ",", current_y)

        elif (move_direction == MOVE_RIGHT):
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
                print("[ERROR] invalid direction")
                return -1

            print("[DIRECTION] current direction is now ", current_d)
            print("[POSITION] Current position is now ", current_x, ",", current_y)
            
        elif (move_direction == MOVE_LEFT):
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
                print("[ERROR] invalid direction")
                return -1

            print("[DIRECTION] current direction is now ", current_d)
            print("[POSITION] current position is now ", current_x, ",", current_y)
                
        else: # this should never happen, but here it is anyways
            print("[ERROR] invalid movement direction")
            return -1

    # set speed of the robot, slower is probably more accurate
    send_command("set_speed(100)")

    ## the robot can start from any position in the room
    ## robot will drive forward until it reaches a wall
    ## and then orient itself to the wall
    wall_found = False
    corrected = False
    while (wall_found != True):
        # poll sensors and print the value to the console
        dist_left = send_command("us_dist(10)") # get distance from left sensor
        time.sleep(0.3)
        dist_front = send_command("us_dist(15)") # get distance from front sensor
        print("[DISTANCE] distance front: ", dist_front)
        print("[DISTANCE] distance left: ", dist_left)
        
        if (dist_left > WALL and dist_front > WALL and corrected == False):  # no wall found      
            # move forward, and stop
            send_command("enc_tgt(1,1," + str(MOVE_DIST) + ")")
            send_command("fwd()")
            time.sleep(3)
            send_command("stop()")

            # update current position
            updatePos(MOVE_FORWARD)

            # correct if too close to a wall
            dist_front = send_command("us_dist(15)")
            if (dist_front < (WALL - 5)):
                adjust_dist = MOVE_DIST - dist_front
                send_command("enc_tgt(1,1," + str(adjust_dist) + ")")
                send_command("fwd()")
                time.sleep(3)
                send_command("stop()")
                corrected = True # if we corrected the distance, we know we are also at a wall
            
        else: # wall found
            wall_found = True
            
            # set current position as the start position
            start_x = current_x
            start_y = current_y
            print ("[START POSITION] start position is ", start_x, ",", start_y)

    if (dist_front <= (WALL + 5)):
        # turn right
        send_command("enc_tgt(0,1,9)")
        send_command("right_rot()")
        time.sleep(3)
        send_command("stop()")
        current_d = RIGHT # robot starts facing UP, but is now facing RIGHT 

    ## the robot is now oriented to the wall
    # add adjacent wall to matrix
    addWall()

    ## now we move the robot one unit forward
    # move forward, and stop
    send_command("enc_tgt(1,1," + str(MOVE_DIST) + ")")
    send_command("fwd()")
    time.sleep(3)
    send_command("stop()")

    # update current position
    updatePos(MOVE_FORWARD)

    ## now that the start position is different from the current position
    ## we can use the current position and the start position as the stop condition
    ## as the robot moves, it will try to keep itself at a set distance from the wall.
    while (current_x != start_x or current_y != start_y):
        dist_left = send_command("us_dist(10)") # get distance from left sensor
        time.sleep(0.3)
        dist_front = send_command("us_dist(15)") # get distance from front sensor
        print("[DISTANCE] distance front: ", dist_front)
        print("[DISTANCE] distance left: ", dist_left)

        if (dist_left <= (WALL + 25)): # wall to the left
            print("[EVENT] wall detected, adding to matrix")

            # update the matrix
            addWall()

            if (dist_front > WALL): # no wall in front
                print("[EVENT] no obstruction detected, moving forward")

                # flag for movement correction
                flag = 0
                
                # correct position if too close to wall
                if (dist_left <= (WALL - 5)):
                    send_command("enc_tgt(0,1,2)")
                    send_command("right_rot()")
                    time.sleep(2)
                    send_command("stop()")
                    flag = 1

                # correct position if too far from wall
                if (dist_left > WALL + 5):
                    send_command("enc_tgt(1,0,2)")
                    send_command("left_rot()")
                    time.sleep(2)
                    send_command("stop()")
                    flag = 2                    
                
                # move forward, and stop
                send_command("enc_tgt(1,1," + str(MOVE_DIST) + ")")
                send_command("fwd()")
                time.sleep(3)
                send_command("stop()")

                # if we corrected the direction, correct back
                if (flag == 1):
                    send_command("enc_tgt(1,0,1)")
                    send_command("left_rot()")
                    time.sleep(2)
                    send_command("stop()")
                    flag = 0

                if (flag == 2):
                    send_command("enc_tgt(0,1,1)")
                    send_command("right_rot()")
                    time.sleep(2)
                    send_command("stop()")
                    flag = 0

                # update current position
                updatePos(MOVE_FORWARD)

                # correct if too close to a wall
                dist_front = send_command("us_dist(15)")
                if (dist_front < (WALL - 5)):
                    adjust_dist = MOVE_DIST - dist_front
                    send_command("enc_tgt(1,1," + str(adjust_dist) + ")")
                    send_command("fwd()")
                    time.sleep(3)
                    send_command("stop()")

            else: # wall in front
                print("[EVENT] obstruction detected, making right turn")

                # turn right
                send_command("enc_tgt(0,1,9)")
                send_command("right_rot()")
                time.sleep(3)
                send_command("stop()")

                # move forward and stop
                send_command("enc_tgt(1,1," + str(MOVE_DIST) + ")")
                send_command("fwd()")
                time.sleep(3)
                send_command("stop()")

                # update current position
                updatePos(MOVE_RIGHT)

        else: # no wall to the left
            print("[EVENT] no wall detected, making left turn")

            # turn left
            send_command("enc_tgt(1,0,9)")
            send_command("left_rot()")
            time.sleep(3)
            send_command("stop()")

            # move forward and stop
            send_command("enc_tgt(1,1," + str(MOVE_DIST) + ")")
            send_command("fwd()")
            time.sleep(3)
            send_command("stop()")

            # update current position
            updatePos(MOVE_LEFT)

    ## outside of while loop
    print("[STOP] mapping complete.")
    #print("Printing matrix...")
    #print('\n'.join([''.join(['{:4}'.format(item) for item in row])
    #    for row in map_mtx]))   
    return map_mtx     
    
## end of definitions
