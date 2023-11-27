import socket

#recieves the messages from the client
myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
myTCPSocket.bind(("localhost", 1024))

myTCPSocket.listen(5)

#Port: 46960
#IP Address: 47.147.221.105
while True:

	client_socket, client_address = myTCPSocket.accept()

	while True:

		myData = str(client_socket.recv(1024).decode())

		#Changes the letters of the message to "capital letters" and send it back to the client by using the same socket.
		if not myData:
			break
		response = myData.upper()
		print("This is my data" + myData)

		client_socket.send(response.encode())

	client_socket.close()


#The server should be able to send multiple messages to the client.
	#May need to have an infinite loop here