#Server side code, this is the only thing that will run on the robot in our final version (if agreed upon)
#Only code that will have the gopigo library imported

#NOTE: When sending strings to this program through 'rob_client.py:send_command(str)' 
#      str must be exactly what function you want
#      example: send_command("enc_tgt(1,0,9)").
#      exec() will treat the string as a function

#from gopigo import *
import socket 
from time import sleep
#import map_mode_tcp
#from map_mode_tcp import *
s = socket.socket()

MAX_COMMAND_SIZE = 50

host = "192.168.1.1"
#host = socket.gethostname() #Get the ip address of the robot itself
print("Host IP: " + str(host)) #Print ip address
port = 8002 #This port should be fine

# <*> this fixes "address already in use", update: might not actually fix "address already in use"
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.bind((host,port))  #I have a vauge idea of what this does

s.listen(1) 	#We will only listen for one client
c, addr = s.accept() #vauge idea of what this does

def receive_command():
	#receive MAX_COMMAND_SIZE bytes from client
	inbound = c.recv(MAX_COMMAND_SIZE).decode()

	#Find the end of the string, to remove padding
	terminator = inbound.find("*")
	if(terminator == -1):
		return "quit"

	#print("Receiving alter : " + inbound[:terminator])
	outbound = 0 #pretty sure we need this

	#Set outbound value to whatever command we have been given
	#This will usually be boolean value to denote success or failure
	#except for command 'us_dist()' the outbound value will be distance measured
	exec("outbound = " + inbound[:terminator])
	print("outbound: ",outbound)

	outbound_str = str(outbound) #set outbound_str as sendable data (bytes/chars)
	for i in range(8 - len(outbound_str)): #Pad so total size is 8 bytes
		outbound_str += ' '

	#send the padded value
	c.send(outbound_str.encode())

	#returning the received command to print out in the server loop
	return inbound[:terminator]

#handshake
greeting = 'Connected, your address is ' + str(addr)
c.send(greeting.encode()) #Send the ip address of accepted client

greetingBytes = 15
inbound = c.recv(greetingBytes).decode() #Receive "Hello Mr. Robot" message
print(inbound)
#receive_command()
#handshake

received = "start"

while(received != "quit"):
	received = receive_command()
	print("Received and executed: " + received)

c.close()
