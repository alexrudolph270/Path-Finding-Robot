import socket

s = socket.socket()

host = socket.gethostname()
port = 8001 

s.connect((host,port))

data = s.recv(64)
print(data)

s.send("sentFromClient".encode())

outbound = "start" 

while outbound != "quit":
  outbound = raw_input("Enter command: ")
  print("sending outbound: ",outbound)
  s.send(outbound.encode())
  
