from pymongo import MongoClient, database
import subprocess
import threading
from datetime import datetime, timedelta
import time

DBName = "test"  # Use this to change which Database we're accessing
connectionURL = "mongodb+srv://diegogar577:al123456@cluster0.mieaij3.mongodb.net/?retryWrites=true&w=majority"  # Put your database URL here
sensorTable = "traffic data"  # Change this to the name of your sensor data table


def QueryToList(query):
    # Convert the query that you get in this function to a list and return it
    result = []
    for item in query:
        result.append(item)
    return result

    pass

    # HINT: MongoDB queries are iterable


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
        client = MongoClient(connectionURL)
        db = client[DBName]
        print("Database collections: ", db.list_collection_names())

        # We first ask the user which collection they'd like to draw from.
        sensorTable = db[sensorTable]
        # We convert the cursor that mongo gives us to a list for easier iteration.
        timeCutOff = datetime.now() - timedelta(minutes=0)  # TODO: Set how many minutes you allow

        oldDocuments = QueryToList(sensorTable.find({"time": {"$gte": timeCutOff}}))
        currentDocuments = QueryToList(sensorTable.find({"time": {"$lte": timeCutOff}}))

        print("Current Docs:", currentDocuments)
        print("Old Docs:", oldDocuments)
        # access the item in the list with key payload
        sensorList = []
        for item in currentDocuments:
            sensorList.append(item['payload'])
        for sensor in sensorList:
            print(list(sensor)[2])
            print(list(sensor.values())[2])
            


    # TODO: Parse the documents that you get back for the sensor data that you need
    # Return that sensor data as a list


    except Exception as e:
        print("Please make sure that this machine's IP has access to MongoDB.")
        print("Error:", e)
        exit(0)


QueryDatabase()
