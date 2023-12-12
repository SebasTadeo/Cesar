import socket
import ipaddress
import threading
import time
import contextlib
import errno
from dataclasses import dataclass
import random
import sys

maxPacketSize = 1024
defaultPort = 64444

def GetFreePort(minPort: int = 1024, maxPort: int = 65535):
    for i in range(minPort, maxPort):
        print("Testing port",i)
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as potentialPort:
            try:
                potentialPort.bind(('127.0.0.1', i))
                potentialPort.close()
                print("Server listening on port",i)
                return i
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    print("Port",i,"already in use. Checking next...")
                else:
                    print("An exotic error occurred:",e)

def GetServerData() -> list[str]:
    import MongoDBConnection as mongo
    return mongo.QueryDatabase()

def ListenOnTCP(tcpSocket: socket.socket, socketAddress):
    count91 = 0
    sum91 = 0
    count5 = 0
    sum5 = 0
    count605 = 0
    sum605 = 0
    print("tcp server listening...")
    while True:
        dataClient = tcpSocket.recv(1024)
        if not dataClient:
            continue
        msgClient = "Message From Client: {}".format(dataClient)
        print(msgClient)
        payloads = GetServerData()
        for payload in payloads:
        #print(payload)
            if "Traffic Sensor 5" in payload.keys():
                count5 += 1
                sum5 += payload.get("Traffic Sensor 5")
            elif "Traffic Sensor 91" in payload.keys():
                count91 += 1
                sum91 += payload.get("Traffic Sensor 91")
            elif "Traffic Sensor 605" in payload.keys():
                count605 += 1
                sum605 += payload.get("Traffic Sensor 605")
        avg91 = sum91 / count91
        avg5 = sum5 /count5
        avg605 = sum605 / count605
        fasthwy = min(avg605, avg5, avg91)
        print(fasthwy)
        print(avg91, avg5, avg605)
        message2Client = ""
        if fasthwy == avg5:
            message2Client = "The fastest is Freeway 5!"
        elif fasthwy == avg605:
            message2Client = "The fastest is Freeway 605!"
        else:
            message2Client = "The fastest is Freeway 91"
        bytes2send = str.encode(message2Client)
        tcpSocket.sendall(bytes2send)
def CreateTCPSocket() -> socket.socket:
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpPort = defaultPort
    print("TCP Port:",tcpPort)
    tcpSocket.bind(('127.0.0.1', tcpPort))
    return tcpSocket

def LaunchTCPThreads():
    tcpSocket = CreateTCPSocket()
    tcpSocket.listen(5)
    while True:
        connectionSocket, connectionAddress = tcpSocket.accept()
        connectionThread = threading.Thread(target=ListenOnTCP, args=[connectionSocket, connectionAddress])
        connectionThread.start()

if __name__ == "__main__":
    tcpThread = threading.Thread(target=LaunchTCPThreads)
    tcpThread.start()
    exitSignal = True 
    
    while not exitSignal:
        time.sleep(1)
        print("Ending program by exit signal...")