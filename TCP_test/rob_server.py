#Server side code, this is the only thing that will run on the robot in our final version (if agreed upon)
#Only code that will have the gopigo library imported

#NOTE: When sending strings to this program through 'rob_client.py:send_command(str)' 
#      str must be exactly what function you want
#      example: send_command("enc_tgt(1,0,9)").
#      exec() will treat the string as a function

#from gopigo import *
import socket

s = socket.socket()

host = socket.gethostname() #Get the ip address of the robot itself
print(host) #Print ip address
port = 8002 #This port should be fine
s.bind((host,port))  #I have a vauge idea of what this does

s.listen(1) #We will only listen for one client
c, addr = s.accept() #vauge idea of what this does

c.send("Connected, your address is " + str(addr)) #Send the ip address of accepted client

inbound = c.recv(64).decode("ascii") #Receive "Client connected" message
print(inbound)

while inbound != "quit":
  inbound = c.recv(64).decode("ascii") #receive sent string
  print("Receiving string: " + inbound)
  exec(inbound) #Eval takes a string and treats it as a function

c.close()
