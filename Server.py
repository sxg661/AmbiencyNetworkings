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



    client.sendToUnity("Goodbye") 
    print("client disconnected")
    c.close()






    

if __name__ == "__main__":
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12345                # Reserve a port for your service.
    s.bind(("127.0.0.1", port))        # Bind to the port
    setVenues(VenueClass.getVenues())

    s.listen(5)                 # Now wait for client connection.
    print("server started")
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
           client.send("go away, python client")
           print("client disconnected")
           c.close()

       else:
           error = ("ERROR: INVALID Client Type : {}".format(data))
           client.send(error)
           c.close()
          
                       



