import socket

s = socket.socket()

host = socket.gethostname()
print(host)
port = 8001 
s.bind((host,port)) 

s.listen(1)
c, addr = s.accept() 

c.send("Connected, your address is " + str(addr))

inbound = c.recv(64).decode("ascii")
print(inbound)
c.close()
