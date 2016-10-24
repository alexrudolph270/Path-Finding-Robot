from gopigo import *

speed = 100
sleep_t = 2

set_speed(speed) #robot will go half as slow as default

print("Rotate 90")
rotate = 90 
enc_tgt(1,1,int(rotate * 0.1))	
right_rot()
sleep(sleep_t)

print("Rotate 180")
rotate = 180 
enc_tgt(1,1,int(rotate * 0.1))	
right_rot()
sleep(sleep_t)

print("Rotate 270")
rotate = 270 
enc_tgt(1,1,int(rotate * 0.1))	
right_rot()
sleep(sleep_t)