import socket

s = socket.socket()

host = "192.168.1.1"
port = 8002 

s.connect((host,port))

data = s.recv(64)
print(data)

s.send("sentFromClient".encode())

outbound = "start" 

while outbound != "quit":
  outbound = input("Enter command: ")
  print("sending outbound: ",outbound)
  s.send(outbound.encode())
  
