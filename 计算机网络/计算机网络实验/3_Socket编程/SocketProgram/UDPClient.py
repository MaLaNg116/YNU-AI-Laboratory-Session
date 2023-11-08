# UDPClient
from socket import *

serverName = "localhost"
serverPort = 2023
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input("Input lowercase sentence:")
clientSocket.sendto(message.encode("UTF-8"), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
modifiedMessage.decode("UTF-8")
clientSocket.close()
