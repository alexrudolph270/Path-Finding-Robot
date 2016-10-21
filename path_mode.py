'''
Algoritm to describe the method of movement for path_mode for robot
Given a list of coordinates, it performs operations to move the robot physically
	accross the floor, adhering to a virtual predefined matrix
	
TODO: 
	* fix orient function, currently can get a divide by 0 
	* determine how gopigo function operates to rotate robot a certain number of degrees
      place that code in the orient() function
'''

import time
import math
from gopigo import *

#test paths
#sample path, usually will get path from matrixdraw methods (pedro code)
#path = [[1 , 2], [1 , 3] ,[2, 3]]
path = [[1 , 2] ,[1, 4]]

def orient(dif = []): #<-------- needs to be expanded upon
	#Given the difference of the location and next point,
	 #this function finds the new orientation the robot has to make, and rotates appropriatly 
	
	#Getting the new orientation
	#This will cause problems if dif[1] == 0, need to fix
	next_theta = math.atan(dif[0]/dif[1])

	if  (dif[0] < 0 and dif[0] < 0):
		next_theta = next_theta + 270 
	elif(dif[1] < 0):
		next_theta = next_theta + 180
	elif(dif[0] < 0):
		next_theta = next_theta + 360
		
	#rotate (next_theta - theta)
		
	return next_theta

		
def dimensions():
	## Determines the dimensions of the grid, always squared
	#    unless we decide to change that further on
	return 20

#default starting location will be in the middle of matrix
#default_location = [int(dimensions() / 2) , int(dimensions() / 2)]
default_location = [1,1]
location = default_location
print ("Default location is %d",default_location)
#python is so slick you don't even need a /n for nextline, but what if I didn't want it? ug?

#default starting orientation will be "north"
#relative to the matrix, not true north
theta = 0 

#approximate velocity
#approx_velocity = 200 #this is in abitrary gopigo units/ sce
approx_velocity = 1.18 #this is in feet/sec
#probably need in clicks/sec, this is default speed of robot
#however, this seems way to fast, sleep doesn't seem to wait long enough

#Imperial units for right now, GO AMERICA
#feet per unit, how big each cell is on matrix
feet_per_unit = 1

print ("We are going to follow the path ",path)

#while path is "true" aka it has at least one member in set, python is so easy
while path:
	#we are going to the next coordinate in the list
	next_location = path[0]
	print("Moving from " + str(location) + " to " + str(next_location))
	
	# [Xnew - X , Ynew - Y]
	difference = [next_location[0] - location[0], next_location[1] - location[1]]
	
	#change orientation if neccesary
	#theta = orient(difference)
	
	#distance is in the units of the MATRIX itself, not feet or anything, we must convert later
	distance = math.sqrt( math.pow(difference[0],2) + math.pow(difference[1],2))
	print("Distance in units of matrix: " ,distance)
	print("Distance in feet: ", distance * feet_per_unit)
	
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
	enc_tgt(1,1,int(move_distance))
	fwd()
	#~~~~~~~~~~~~~~~~~~~~
	
	# I was wrong, we should be able to use the speed of robot in clicks/sec
	# time = distance / rate 
	#time.sleep((move_distance / approx_velocity) * 1.3)
	time.sleep( ( (distance * feet_per_unit) / approx_velocity) * 1.3) #
	
	#We now 'should' be at the next coordinate in the list
	location = next_location
	
	path.pop(0) #pop first member of set, path.pop() default pops the last member of the set
	
print("Hooray! We are now at ", location)
