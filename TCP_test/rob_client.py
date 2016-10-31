import socket

s = socket.socket()

host = "192.168.1.1"
port = 8002 

s.connect((host,port))

data = s.recv(64) #when connected will receive up to 64 bytes
print(data)       #print received data, probably the IP address of server
s.send("Client is connected".encode())

#'''
outbound = "start" 

while outbound != "quit":
  outbound = input("Enter command: ")
  send_command(outbound)
#'''
  
  #simple function that will be used for every time you call a gopigo function
def send_command(str)
  print("Sending string: ",str)
  s.send(str.encode())
  
