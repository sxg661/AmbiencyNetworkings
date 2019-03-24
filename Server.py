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


def getVenues():
    global lock
    global venues
    lock.acquire()
    venuesCopy = copy.deepcopy(venues)
    lock.release()
    return venuesCopy

    

def appClientThread(c, client):

    client.send("thank you for connecting, C# client")
    
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
                
                client.send("VENUE")
                client.send(str(venue))

            client.send("DISPLAY") 
        elif command == "DISCONNECT":         
            running = False
        else:
            error = "Invalid Command : {}".format(command)
            client.send(error)



    client.send("Goodbye") 
    print("client disconnected")
    c.close()






    

if __name__ == "__main__":
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12345                # Reserve a port for your service.
    s.bind((host, port))        # Bind to the port
    setVenues(VenueClass.getVenues())

    s.listen(5)                 # Now wait for client connection.
    while True:
       c, addr = s.accept()     # Establish connection with client.
       client = SocketWrapper(c)
       print('Got connection')
       #read a byte array from a socket
       clientType = client.recv()
      
       if(clientType == "app"):
           appThread = threading.Thread(target = appClientThread, args = (c, client))
           appThread.start()
           
       elif (clientType == "pi"):
           client.send("thank you for connecting, python client")
           client.send("goodbye")
           c.close()

       else:
           error = ("ERROR: INVALID Client Type : {}".format(data))
           client.send(error)
           c.close()
          
                       



