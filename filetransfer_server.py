import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
f = open('torecv.png','wb')
s.listen(5)                 # Now wait for client connection.

c, addr = s.accept()     # Establish connection with client.
print('Got connection from', addr)
print("Receiving...")
data = c.recv(1024)
while data:
    print("Receiving...")
    f.write(data)
    data = c.recv(1024)
f.close()
print("Done Receiving")
c.close()                # Close the connection