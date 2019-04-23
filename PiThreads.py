import threading
import time
import socket
import socketWrapper
import queue
import serial
import json
import VenueClass
import math

#author James Adey

exitFlag = 0

class PiToArd(threading.Thread):

    srvInputQueue = None
    ser = None
    state = None
    
    def __init__(self,name,qToSrv,serialName,serialRate):
        threading.Thread.__init__(self)
        self.name = name
        self.running = True
        self.srvInputQueue = qToSrv
        self.serialName = serialName
        self.serialRate = serialRate
        self.state = "need_serial"
        

    def run(self):
        print ("Starting " + self.name)
        while(self.running):
            if(self.state == "need_serial"):
                self.open_serial()
            elif(self.state == "has_serial"):
                self.has_serial()
        print ("Exiting " + self.name)

    def open_serial(self):
        try:
            #self.ser = serial.Serial(self.serialName,self.serialRate)
            self.state = "has_serial"
        except Exception as e:
            print(e)
            print("error opening serial, retrying in 1 second...")
            time.sleep(1)

    def has_serial(self):
        blah = ((math.sin(time.time())+1)/2)*100
        data = (time.time(),blah)
        self.srvInputQueue.put(data)
        time.sleep(0.4)

        
class PiToServer(threading.Thread):

    state = None
    sock = None
    wrapper = None
    counter = 0
    ardOutputQueue = None
    
    def __init__(self,name,qFromArd,ip,port):
        threading.Thread.__init__(self)
        self.name = name
        self.running = True
        self.state = "need_connection"
        self.sock = socket.socket()
        self.destIp = ip
        self.destPort = port
        self.ardOutputQueue = qFromArd
        # id is important, must be 12
        self.venueInfo = VenueClass.VenueInfo(12,"Joe's Bar", "Bar", 50, 0, 50, 1000, 23, 60)

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
            print("\nattempting connection to "+self.destIp + ":"+str(self.destPort))
            self.sock.connect((self.destIp,self.destPort))
            self.wrapper = socketWrapper.SocketWrapper(self.sock)
            print("connected to server!")
            self.wrapper.send("pi")
            print("sent hello")
            self.state = "running"
        except Exception as e:
            print(e)
            print("retrying in 1 second...")
            time.sleep(1)
    
    def when_connected(self):
        if(self.ardOutputQueue.empty()):
            try:
                print("no arduino data, sending keep alive")
                self.wrapper.send("crap")
            except Exception as e:
                print(e)
                print("error in keep alive, restarting connection...")
                self.sock.close()
                self.sock = socket.socket()
                self.state = "need_connection"
        else:
            while(not self.ardOutputQueue.empty()):
                (timestamp,data) = self.ardOutputQueue.get()
                try:
                    self.update_venue("occupancy", data)
                    self.wrapper.send("UPDATE")
                    self.wrapper.send(str(self.venueInfo))
                    print(str(self.venueInfo))
                    self.running = False
                except Exception as e:
                    print(e)
                    print("error when connected, restarting connection...")
                    self.sock.close()
                    self.sock = socket.socket()
                    self.state = "need_connection"
                    break        
            
        # only check every second
        time.sleep(1)
    
    def update_venue(self,sensorType, data):
        if(sensorType == "occupancy"):
            self.venueInfo.occupancy = data
        elif(sensorType == "humidity"):
            self.venueInfo.humidity = data
        elif(sensorType == "light"):
            self.venueInfo.light = data
        elif(sensorType == "temperature"):
            self.venueInfo.temperature = data
        elif(sensorType == "sound"):
            self.venueInfo.sound = data
        elif(sensorType == "distance"):
            self.venueInfo.distance = data
        else:
            print("UPDATING INVALID SENSOR TYPE")

'''
-----------------
THE LAUNCHER CODE
-----------------
'''

# load the config file
file = open("pi_cfg.json")
configData = json.load(file)
file.close()

# get config data
ipAddr = configData["ip"]
port = int(configData["port"])
serialName = configData["serial"]
serialRate = int(configData["serialrate"])

# establish communication queue
qArdToSrv = queue.Queue()

# Create new threads
piToArd = PiToArd("pi to arduino",qArdToSrv,serialName,serialRate)
piToSrv = PiToServer("pi to server",qArdToSrv,ipAddr,port)

# Start new Threads
piToArd.start()
piToSrv.start()

piToArd.join()
piToSrv.join()
print ("Exiting Main Thread")
