#Client side code, this module will be imported throughtout each subsystem
#When this is fully implemented, we will not have 'from gopigo import *' in any code except for rob_server.py

#NOTE: When sending strings to the server
#      str must be exactly what function you want
#      example: send_command("enc_tgt(1,0,9)") or send_command("fwd()")
#      serverside has a function called eval(), it will treat the string as a function

import socket
s = socket.socket()

host = "192.168.1.1"
port = 8002 

s.connect((host,port))

data = s.recv(64) #when connected will receive up to 64 bytes
print(data)       #print received data, probably the address of the client
s.send("Client is connected".encode())

#'''
outbound = "start" 

while outbound != "quit":
  outbound = raw_input("Enter command: ")
  send_command(outbound)
#'''
  
  #simple function that will be used for every time you call a gopigo function
def send_command(str)
  print("Sending string: ",str)
  s.send(str.encode())
  
