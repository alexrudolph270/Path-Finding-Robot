#!/usr/bin/python

#Stormon Force
#Text Server Lab
#September 11th, 2016

import socket

def CommandSend():
	return raw_input("Enter command: ")
	
s = socket.socket()
outbound = ""
host = socket.gethostname()
port = 8001

print("All commands are four letters\n" +
	  "help for list of commands\n"     +
	  "quit to disconnect from server\n")

s.connect((host,port))
print(s.recv(64)) # c.send("Connected, your address is")
while outbound != "quit":
    outbound = CommandSend().encode() 
    s.send(outbound) 	#Outbound 
    if outbound == "quit":
		break 
    print(s.recv(256)) #Inbound
print("Disconnected")
s.close
