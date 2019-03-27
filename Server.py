#!/usr/bin/python           # This is server.py file

import threading

import socket               # Import socket module

import VenueClass

import copy

from socketWrapper import SocketWrapper

from threading import Lock, Thread

venues = []

lock = Lock()

'''messages are seperated by double new lines, so that new lines can be
used as seperators inside messages'''



def setVenues(newVenues):
    global lock
    global venues
    lock.acquire()
    venues = newVenues
    lock.release()

def replaceVenues(newVenue):
    return

def getVenues():
    global lock
    global venues
    lock.acquire()
    venuesCopy = copy.deepcopy(venues)
    lock.release()
    return venuesCopy

    

def appClient(c, client):

    client.sendToUnity("thank you for connecting, C# client")
    
    currentVenues = []
    running = True

    '''this is incase a message decides to split itself over two
      packets >:('''
    leftover = ""


    
    while(running):
    
        command = client.recv()
        print("got command " + command)

        if command == "SEARCH":
            venueType = client.recv()
            print("searching for venues of type {}".format(venueType))
            venuesToSend = VenueClass.filter(getVenues(), venueType)

            for venue in venuesToSend:

                print("SendingVenueData")
                client.sendToUnity("VENUE")
                client.sendToUnity(str(venue))

            client.sendToUnity("DISPLAY") 
        elif command == "DISCONNECT":         
            running = False
        else:
            error = "Invalid Command : {}".format(command)
            client.sendToUnity(error)



    


def piClient(c, client):

    running = True
    while(running):
        command = client.recv()

        if(command == "UPDATE"):
            print("VENUE: " + client.recv())
        elif(command == "DISCONNECT"):
            running = False
        else:
            error = "Invalid Command : {}".format(command)
            print(error)
            client.send(error)
    return
    

def clientThr(c,client):

    running = True
    while(running):
        clientType = client.recv()

        if(clientType == "app"):
           print("app connected")
           appClient(c, client)
           running = False
        elif (clientType == "pi"):
           print("python client connected")
           piClient(c,client)
           running = False
        elif (clientType == "DISCONNECT"):
           running = False
        else:
           error = ("ERROR: INVALID Client Type : {}".format(clientType))
           print(error)
           client.send(error)

    client.send("goodbye")
    print("Client Disconnected")
    c.close()
          
    

if __name__ == "__main__":
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12345                # Reserve a port for your service.
    #s.bind(("192.168.0.101", port))        # Bind to the port
    s.bind(("192.168.0.101", port)) 
    setVenues(VenueClass.getVenues())

    s.listen(5)                 # Now wait for client connection.
    print("server started")
    while True:
       c, addr = s.accept()     # Establish connection with client.
       client = SocketWrapper(c)
       print('Got connection')
       #read a byte array from a socket

       clientThread = threading.Thread(target = clientThr, args = (c, client, ))
       clientThread.start()
       
                       



