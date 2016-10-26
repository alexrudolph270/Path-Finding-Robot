#!/usr/bin/python

#Stormon Force
#Text Server Lab
#September 11th, 2016

import socket

inbound = ""
def PerformCommand(prompt):
	if  prompt[0:4] == "REVW":
		return prompt[:4:-1]
	elif prompt[0:4] == "SORT":
		return CommandSort(prompt[4:])
	elif prompt[0:4] == "UPPR":
		return prompt[4:].upper()
	elif prompt[0:4] == "NVWL":
		return CommandNoVowel(prompt[4:])
	elif prompt[0:4] == "LENG":
		return str(len(prompt[5:]))
	elif prompt[0:4] == "SLCT":
		return str(CommandCountChar(prompt[4:]))
	elif prompt == "help":
		return CommandHelp()
	elif prompt == "quit":
		return "QUIT"
	else:
		return "Bad Command"

def CommandCountChar(str):
	Char = str[1]
	Count = 0 
	for c in str[2:]:
		if c.lower() == Char.lower():
			Count += 1
	return Count
		
				
def CommandNoVowel(str):
	v = ["a","e","i","o","u"]
	ToReturn = []
	for c in str:
		if c.lower() not in v:
			ToReturn.append(c)	
	return "".join(ToReturn)
	
		
def CommandSort(str):
	StringArray = str.split()
	StringArray.sort()
	return ' '.join(StringArray)
	
def CommandHelp():
	return """	REVW Reverse string
	SORT alphabetize list
	UPPR all uppercase
	NVWL remove all vowels
	LENG returns char count
	SLCT counts times char c appears, example: "SLCT e seven" returns 2"""
		
def CommandReceive( str ):
	print ("COMMAND " + str)
	return "OK " + PerformCommand(str)

s = socket.socket()

host = socket.gethostname()
print(host)
port = 8001 
s.bind((host,port))  

s.listen(5)
while True:
    c, addr = s.accept()
    print ('Connection from',addr)
    c.send("Connected, your address is " + str(addr))
    while inbound != "quit":
        inbound = c.recv(128).decode("ascii") #Inbound 
        c.send(CommandReceive(inbound)) 	   #Outbound
        if inbound == "quit":
			break 
    inbound = ""
    print ('Disconnected ',addr)
    c.close()