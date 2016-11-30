#Client side code, this module will be imported throughtout each subsystem
#When this is fully implemented, we will not have 'from gopigo import *' in any code except for rob_server.py

#NOTE: When sending strings to the server
#      str must be exactly what function you want
#      example: send_command("enc_tgt(1,0,9)") or send_command("fwd()")
#      serverside has a function called eval(), it will treat the string as a function

import socket
from time import sleep

MAX_COMMAND_SIZE = 50

 #simple function that will be used for every time you call a gopigo function
def send_command( str_cmd ):
	print("Sending string <" + str_cmd + "> of size " + str(len(str_cmd))) #original string

	#padding the string by message_size - len(str) amount
	for i in range(0,MAX_COMMAND_SIZE - len(str_cmd)): 
		str_cmd += "*"  

	#print("Sending string <" + str_cmd + "> of size " + str(len(str_cmd))) #orginal string padded
	s.send(str_cmd.encode()) #sending padded string

	#receive the value of our executed command we sent in string form
	data_string = s.recv(8).decode()
	#convert to an integer
	if(data_string != "None    "):
		data = int(data_string)
	else:
		data = 0
	#return the integer to whichever module called it
	#This function can be called and treated as void
	#So it shouldn't break any exisiting code fingers crossed
	return data

s = socket.socket()

#host = socket.gethostname()
host = "192.168.1.1"
port = 8002 

s.connect((host,port))

#handshake
data = s.recv(MAX_COMMAND_SIZE).decode() #when connected will receive up to 64 bytes
print(data)       #print received data, probably the address of the client

#s.send("Connected to host".encode())
s.send("Hello Mr. Robot".encode())
#send_command("Hello Mr. Robot")
#handshake

#x = send_command("1 + 2")
##print(x)
