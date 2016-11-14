#Server side code, this is the only thing that will run on the robot in our final version (if agreed upon)
#Only code that will have the gopigo library imported

#NOTE: When sending strings to this program through 'rob_client.py:send_command(str)' 
#      str must be exactly what function you want
#      example: send_command("enc_tgt(1,0,9)").
#      exec() will treat the string as a function

#from gopigo import *
import socket 
from time import sleep
s = socket.socket()

MAX_COMMAND_SIZE = 50

host = "192.168.1.1"
#host = socket.gethostname() #Get the ip address of the robot itself
print("Host IP: " + str(host)) #Print ip address
port = 8002 #This port should be fine

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # <*> this fixes "address already in use"
s.bind((host,port))  #I have a vauge idea of what this does

s.listen(1) #We will only listen for one client
c, addr = s.accept() #vauge idea of what this does

def map_mode():
	m = [[1,2,3],[4,5,6],[7,8,9],[4,4,4]]
	return m

def server_mapmode():
	print("server_mapmode activated")

	#get the matrix map mode returns
	matrix = map_mode()

	#convert to a string
	matrix_string = str(matrix)
	print("server: " + matrix_string)
	
	#send how many bytes the matrix string will be
	matrix_string_size = str(len(matrix_string))
	for i in range(0,8 - len(matrix_string_size)): 	#padding
		matrix_string_size += " " 

	c.send(matrix_string_size.encode())

	#send the matrix string
	c.send(matrix_string.encode())

def receive_command():
	inbound = c.recv(MAX_COMMAND_SIZE).decode()
	#print("Received string : " + inbound)
	terminator = inbound.find("*")
	if(terminator == -1):
		return "quit"

	#print("Receiving alter : " + inbound[:terminator])

	exec(inbound[:terminator])

	return inbound[:terminator]

#handshake
greeting = 'Connected, your address is ' + str(addr)
c.send(greeting.encode()) #Send the ip address of accepted client

inbound = c.recv(MAX_COMMAND_SIZE).decode() #Receive "Hello Mr. Robot" message
print(inbound)
#receive_command()
#handshake

received = "start"

while(received != "quit"):
	received = receive_command()
	print("Received and executed: " + received)

c.close()

