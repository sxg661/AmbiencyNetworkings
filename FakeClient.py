import socket               # Import socket module


s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.


s.connect(("127.0.0.1", port))
print("hello")

s.send(b"app\n\n")
print(s.recv(1024).decode('utf-8'))

s.send(b"SEA")
for i in range(0,100):
    print("cake")
s.send(b"RC")
for i in range(0,100):
    print("cake")
s.send(b"H\n\n")
s.send(b"Bar\n\n")

response = s.recv(2048).decode('utf-8')
print(response)


print(s.recv(1024).decode('utf-8'))

s.send(b"cake\n\n")
print("sent a cake")
print(s.recv(1024).decode('utf-8'))


s.send(b"DISCONNECT\n\n")
print(s.recv(1024).decode('utf-8'))

s.close()                     # Close the socket when done
