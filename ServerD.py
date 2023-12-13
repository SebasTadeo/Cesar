import socket
import ipaddress

import threading
import time
import contextlib
import errno
import random
import sys
from pymongo import MongoClient, database
from datetime import datetime, timedelta

# returns the hostname of the machine
host = socket.gethostname()
# returns the IP address of the machine
ip_address = socket.gethostbyname(host)
maxPacketSize = 1024
defaultPort = 1117  # TODO: Set this to your preferred port
DBName = "test"  # Use this to change which Database we're accessing
connectionURL = "mongodb+srv://diegogar577:al123456@cluster0.mieaij3.mongodb.net/?retryWrites=true&w=majority"  # Put your database URL here
sensorTable = "traffic data"  # Change this to the name of your sensor data table



def QueryDatabase() -> []:
    global DBName
    global connectionURL
    global currentDBName
    global running
    global filterTime
    global sensorTable
    cluster = None
    client = None
    db = None
    try:
        cluster = connectionURL
        client = MongoClient(cluster)
        db = client[DBName]
        # print("Database collections: ", db.list_collection_names())

        # We first ask the user which collection they'd like to draw from.
        sensorTable = db[sensorTable]
        # print("Table:", sensorTable)
        # We convert the cursor that mongo gives us to a list for easier iteration.
        timeCutOff = datetime.now() - timedelta(minutes=0)  # TODO: Set how many minutes you allow

        oldDocuments = QueryToList(sensorTable.find({"time": {"$gte": timeCutOff}}))
        currentDocuments = QueryToList(sensorTable.find({"time": {"$lte": timeCutOff}}))
        # print("Current Docs:", currentDocuments)
        # print("Old Docs:", oldDocuments)
        sensorList = []
        for item in currentDocuments:
            sensorList.append(item['payload'])
        # initialize empty dictionary with two values
        sensorCalc = {}
        for sensor in sensorList:
            if list(sensor)[2] not in sensorCalc:
                sensorCalc[list(sensor)[2]] = {
                    "sensorCount": 1,
                    "sum": list(sensor.values())[2]
                }
            elif list(sensor)[2] in sensorCalc:
                sensorCalc[list(sensor)[2]]["sensorCount"] += 1
                sensorCalc[list(sensor)[2]]["sum"] += list(sensor.values())[2]

        print(sensorCalc)
    except Exception as e:
        print("Please make sure that this machine's IP has access to MongoDB.")
        print("Error:", e)
        exit(0)
    averagesArr = {}
    for sensor in sensorCalc:
        averagesArr[sensor] = sensorCalc[sensor]["sum"] / sensorCalc[sensor]["sensorCount"]

    return averagesArr


def QueryToList(query):
    # Convert the query that you get in this function to a list and return it
    result = []
    for item in query:
        result.append(item)
    return result

    pass

    # HINT: MongoDB queries are iterable


if __name__ == "__main__":
    # tcpThread = threading.Thread(target=LaunchTCPThreads)
    # tcpThread.start()

    # next create a server socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the IP address and port
    server_socket.bind((ip_address, defaultPort))
    print("Socket successfully created")
    print(f'Server ip address {ip_address} on and listening on port {defaultPort}')
    server_socket.listen(1)
    averages = QueryDatabase()
    # find the smallest average and the sensor that it belongs to
    smallest = min(averages, key=averages.get)
    # we can now loop for connections
    while True:
        # accept connection from client
        client, address = server_socket.accept()
        print('Received a connection from', address)
        # receive message from client (max 1024 bytes)
        while True:
            # decode the message to plaintext
            msg = client.recv(1024).decode()
            # if the message is empty, break the loop
            if msg == "":
                print("closing connection")
                break
            # print the message
            print(f'Server received the message: {msg}')
            # convert msg to uppercase
            res = smallest

            # respond to client
            client.send(res.encode())

        # Close the connection with the client
        client.close()
