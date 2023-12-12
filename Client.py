import socket
import ipaddress
import threading
import time
import contextlib
import errno

maxPacketSize = 1024
defaultPort = 64444 # TODO: Change this to your expected port
serverIP = '10.39.54.86' #TODO: Change this to your instance IP

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    tcpPort = int(input("Please enter the TCP port of the host..."))
except:
    tcpPort = 0
if tcpPort == 0:
    tcpPort = defaultPort
tcpSocket.connect((serverIP, tcpPort))

clientMessage = "Which freeway is the fastest"
while clientMessage != "exit":
    clientMessage = input("Please type the message that you'd like to send (Or type \"exit\" to exit):\n>")

    #TODO: Send the message to your server
    #TODO: Receive a reply from the server for the best highway to take
    #TODO: Print the best highway to take
    bytes2send = str.encode(clientMessage)
    tcpSocket.sendall(bytes2send)
    msgFromServer = tcpSocket.recv(1024)
    print("Message from Server {}".format(msgFromServer))
    
tcpSocket.close()