'''
Algoritm to describe the method of movement for path_mode for robot
Given a list of coordinates, it performs operations to move the robot physically
	accross the floor, adhering to a virtual predefined matrix
	

Changes since last meeting Oct 20
	All logic now exclusive to function calls
	Orient function should work as intended, only of 90 degree angles however (no 45's)

Changes as of November 12 
	path mode now operatable with tcp rob_client + rob_server connection
	all robot commands converted to strings that will send to the robot server 
'''

import time
import math
from rob_client import *
#from gopigo import *

#test paths
#sample path(s), usually will get path from matrix_draw methods (pedro code)
#path = [[1,2], [1,3], [2, 3], [3,3], [3,2], [3,4]]
#path = [[1 , 2] ,[1, 4]]
#path = [[1, 6],[2,6]]

def orient(theta, dif = []): 
	#Given the difference of the location and next point,
	#this function finds the new orientation the robot has to make, and rotates appropriatly 
	
	print("We are currently facing " + str(theta))
	
	#currently the orientation of robot is set up so that
	#                      0 ^ top of matrix
	# left of matrix < 270       90 > right of matrix
	#                    180 v bottom of matrix
	# Pedro proposes we set 0 degrees to be the right of matrix, 
	# this aligns with standardized way of presenting the unit circle
	
	
	#Finds what direction we need to face to move to next coordinate
	#Uses the difference between next location and current location
	if(dif[0] > 0): #if Xnew - Xcurrent > 0 , then we know we must go to right
		next_theta = 90
	elif(dif[0] < 0): #go left
		next_theta = 270
	elif(dif[1] > 0): #if Ynew - Ycurrent > 0 , then we know we must go up
		next_theta = 0
	elif(dif[1] < 0): #go down
		next_theta = 180
		
	print("We want to face " + str(next_theta)) 
	
	#Finds how much we have to rotate to acquire new orientation of next_theta
	rotate = next_theta - theta
	print("We must rotate " + str(rotate) + " degrees or " + str(rotate * 0.1) + " spokes of wheels");
	
	#if the difference is 0 , we dip out, no need to rotate
	if(rotate == 0):
		print("Both directions are the same, robot will not be rotated")
		return next_theta
	
	#Because enc_tgt cannot take negatives, we have to change this to a positive
	#This will result in some rotational inefficiency, we can only rotate right
	#Suppose we are at 0 and want to face 270,  function will compute we must rotate 270 degrees
	#This is easily fixable but will take some work to implement
	if(rotate < 0):
		rotate = 360 + rotate
		print("Since rotate is negative, we are going to rotate instead " + str(rotate) + " degrees")
	
	#~~~~robot stuff~~~~
	send_command("set_speed(100)") #robot will go half as slow as default
	#enc_tgt(1,1,int(rotate * 0.1))
	send_command("enc_tgt(1,1,int(" +str(rotate * 0.1) + "))" )		
	send_command("right_rot()")
	send_command("set_speed(200)") #change speed back
	#~~~~~~~~~~~~~~~~~~~~
	
	#I want to have a real calculation for this, over shot to ensure rotation is carried out in full 
	time.sleep(3)
	
	return next_theta 

		
def dimensions():
	## Determines the dimensions of the grid, always squared
	#    unless we decide to change that further on
	return 20


def path_mode(path = []):
	#default starting location will be in the middle of matrix
	#default_location = [int(dimensions() / 2) , int(dimensions() / 2)]
	default_location = [1,1]
	
	#location = default_location
	location = path[0] #starting location is the first member in set of coordinates
	path.pop(0)
	print ("Default location is ",default_location)
	#python is so slick you don't even need a /n for nextline, but what if I didn't want it? ug?

	#default starting orientation will be "north"
	#relative to the matrix, not true north
	theta = 0 

	#approximate velocity
	approx_velocity = 1.18 #this is in feet/sec

	#Imperial units for right now, GO AMERICA
	#feet per unit, how big each cell is on matrix
	feet_per_unit = 1

	print ("We are going to follow the path ",path)	
	
	#while path is "true" aka it has at least one member in set, python is so easy
	while path:
		#we are going to the next coordinate in the list
		next_location = path[0]
		print("\nMoving from " + str(location) + " to " + str(next_location))
		
		# [Xnew - X , Ynew - Y]
		difference = [next_location[0] - location[0], next_location[1] - location[1]]
		
		#change orientation if neccesary
		print("~start rotation~")
		theta = orient(theta, difference)
		print("~end rotation~")
		
		#distance is in the units of the MATRIX itself, not feet or anything, we must convert later
		distance = math.sqrt( math.pow(difference[0],2) + math.pow(difference[1],2))
		print("Distance in units of matrix: " ,distance)
		print("Distance in feet: ", distance * feet_per_unit)
		
		print("~~start movement~~")	
		#distance converted to clicks of the wheel
		# 12 * (18/8) = 27 
		move_distance = 27 * distance * feet_per_unit 
		# move_distance = 12        *      (18/8)         *  distance * feet_per_unit
						# 12 inches	   18 clicks of wheel	 n units      F feet 
						# --------- *  ------------------ *  -------  *  -------- = move_distance is in clicks of wheel
						#  1 foot		   8 inches              1        1 unit
						# Cancel the units, and you're left with move_distance in wheels clicks		
		print("Distance in clicks of wheel: ", move_distance)
				
		#~~~~robot stuff~~~~
		#enc_tgt(1,1,int(move_distance))
		send_command("enc_tgt(1,1,int(" + str(move_distance) + "))")
		send_command("fwd()")
		#~~~~~~~~~~~~~~~~~~~~
		
		# I was wrong, we should be able to use the speed of robot in clicks/sec
		# time = distance / rate 
		# rate is currently in feet / sec
		print("Waiting " + str( ((distance * feet_per_unit) / approx_velocity) * 1.3) + " seconds for robot to arrive")
		time.sleep( ( (distance * feet_per_unit) / approx_velocity) * 1.3) #
		
		print("~~end movement~~")
		#We now 'should' be at the next coordinate in the list
		location = next_location
		
		path.pop(0) #pop first member of set, path.pop() default pops the last member of the set
		
	print("Hooray! We are now at ", location)
	
#If running path_mode function from another file, comment this out
#path_mode(path)

