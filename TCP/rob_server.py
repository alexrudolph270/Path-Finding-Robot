#Server side code, this is the only thing that will run on the robot in our final version (if agreed upon)
#Only code that will have the gopigo library imported

#NOTE: When sending strings to this program through 'rob_client.py:send_command(str)' 
#      str must be exactly what function you want
#      example: send_command("enc_tgt(1,0,9)").
#      exec() will treat the string as a function

from gopigo import *
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

def receive_command():
	inbound = c.recv(MAX_COMMAND_SIZE).decode()
	print("Received string : " + inbound)
	terminator = inbound.find("*")
	if(terminator == -1):
		return "quit"
	print("Receiving alter : " + inbound[:terminator])
	'''
	if(inbound == "mapmode()"):
		server_mapmode()
	else
		exec(inbound[:terminator])
	'''
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
	print("loop:" + received + ":loop")

c.close()
