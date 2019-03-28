import socket               # Import socket module


s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.


s.connect(("192.168.0.1", port))
'''
print("hello")

s.send(b"app||")
print(s.recv(1024).decode('utf-8'))

s.send(b"SEA")
for i in range(0,100):
    print("cake")
s.send(b"RC")
for i in range(0,100):
    print("cake")
s.send(b"H||")
s.send(b"Bar||")

response = s.recv(2048).decode('utf-8')
print(response)


print(s.recv(1024).decode('utf-8'))

s.send(b"cake||")
print("sent a cake")
print(s.recv(1024).decode('utf-8'))

'''

s.send(b"pi")
s.send(b"UPDATE")
s.send(b
s.send(b"DISCONNECT||")
print(s.recv(1024).decode('utf-8'))

s.close()                     # Close the socket when done
