import socket
import ipaddress
import threading
import time
import contextlib
import errno

maxPacketSize = 1024
defaultPort = 1117  # TODO: Change this to your expected port
# serverIP = 'localhost'  # TODO: Change this to your instance IP

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # take user input for the server address and port
    server = input("Please input an address: ")
except socket.error as e:
    print(f"Error connection to server: {e}")
    tcpSocket.close()
    exit()
tcpSocket.connect((server, defaultPort))

while True:
    message = input("What info would you like? (type 'exit' to quit): ")
    if message == "exit" or message == "":
        print("closing connection")
        break
    # send the message to the server
    tcpSocket.send(message.encode())
    # receive the response from the server
    response = tcpSocket.recv(1024).decode()
    print(f'Received message from server: {response}')
tcpSocket.close()
