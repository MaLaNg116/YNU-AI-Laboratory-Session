# UDPServer

from socket import *
import time

serverPort = 2023
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("localhost", serverPort))
time_tuple = time.localtime(time.time())
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print(f"接收到来自{clientAddress}的信息，时间为：{time_tuple[0]}年{time_tuple[1]}月{time_tuple[2]}日{time_tuple[3]}时{time_tuple[4]}分{time_tuple[5]}秒。")
    modifiedMessage = message.decode("UTF-8")
    print(modifiedMessage)
    serverSocket.sendto(message, clientAddress)