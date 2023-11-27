import socket

myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Prompt the user to input
	#IP Address: 47.147.221.105
server_ip = input("Enter server IP address: ")

	#Port number of the server: 46960
server_port = int(input("Enter server port: "))


	#A message to send to the server
myTCPSocket.connect((server_ip, server_port))

while True:
	#Send a message to the server
	message = input("Enter a message: ")

	#display the server replay by using the same socket
	myTCPSocket.send(message.encode())

	response = myTCPSocket.recv(1024).decode()
	#display an error message if the IP address or port number were entered incorrectly.

	#The client should be able to send multiple messages to the server.
		#May need to create an infinite loop

	print("Server response: ", response)

myTCPSocket.close()