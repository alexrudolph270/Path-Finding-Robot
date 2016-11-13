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

	for i in range(0,MAX_COMMAND_SIZE - len(str_cmd)): #padding the string by message_size - len(str) amount
		str_cmd += "*"  

	print("Sending string <" + str_cmd + "> of size " + str(len(str_cmd))) #orginal string padded
	s.send(str_cmd.encode()) #SEND
	#return


def request_map_mode():
	#let the server know we want to activate map mode
	send_command("server_mapmode()")

	bytes_string = s.recv(8).decode()
	print("string: " + bytes_string + " cast as int: " + str(int(bytes_string)))
	
	matrix_string = s.recv(int(bytes_string)).decode()
	print(matrix_string)

	matrix = []
	exec("matrix = " + matrix_string)
	#return the matrix to the GUI so it can be displayed
	return matrix

s = socket.socket()

#host = socket.gethostname()
host = "192.168.1.1"
port = 8002 

s.connect((host,port))

#handshake
data = s.recv(MAX_COMMAND_SIZE).decode() #when connected will receive up to 64 bytes
print(data)       #print received data, probably the address of the client

#s.send("Connected to host".encode())
send_command("Hello Mr. Robot")
#handshake

'''
send_command("print('f')")
m = request_map_mode()
print("matrix received" + str(m))
send_command("print('gg')")
'''

