import threading
import time
import socket
import socketWrapper
exitFlag = 0

class PiToArd(threading.Thread):

    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print ("Starting " + self.name)
        print ("Exiting " + self.name)

class PiToServer(threading.Thread):

    state = None
    sock = None
    wrapper = None
    counter = 0
    
    def __init__(self,name,ip,port):
        threading.Thread.__init__(self)
        self.name = name
        self.running = True
        self.state = "need_connection"
        self.sock = socket.socket()
        self.destIp = ip
        self.destPort = port

    def run(self):
        print ("Starting " + self.name)
        while(self.running):
            if(self.counter > 5):
                self.running = False
            if(self.state == "need_connection"):
                self.connect_to_server()
            elif(self.state == "running"):
                self.when_connected()
        print("Closing socket to server...")
        self.sock.close()
        print ("Exiting " + self.name)
    
    def connect_to_server(self):
        try:
            self.sock.connect((self.destIp,self.destPort))
            self.wrapper = socketWrapper.SocketWrapper(self.sock)
            print("connected to server!")
            self.state = "running"
        except Exception as e:
            print(e)
            print("retrying in 1 second...")
            time.sleep(1)
            self.counter += 1

    def when_connected(self):
        self.wrapper.send("pi")
        self.counter += 1
        time.sleep(1)



'''
-----------------
THE LAUNCHER CODE
-----------------
'''

# Create new threads
piToArd = PiToArd("pi to arduino")
piToSrv = PiToServer("pi to server","127.0.0.1",12345)

# Start new Threads
piToArd.start()
piToSrv.start()

piToArd.join()
piToSrv.join()
print ("Exiting Main Thread")
