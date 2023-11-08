# TCPClient
from socket import *

serverName = 'localhost'
serverPort = 2023
clientSocket = socket(AF_INET, SOCK_STREAM)  # 设置TCP Socket客户端
clientSocket.connect((serverName, serverPort))  # 连接服务器
address = clientSocket.getsockname()  # 获取并打印服务器地址
print(f"来自服务器{address}:你已连接成功。")
while True:
    sentence = input('Input lowercase sentence:')
    if sentence == exit:
        break
    clientSocket.send(sentence.encode("UTF-8"))  # 向服务器发送TCP数据
    modifiedSentence = clientSocket.recv(1024)  # 接收服务器返回的TCP数据
    print(f"来自服务器{address}:{modifiedSentence.decode('UTF-8')}")
clientSocket.close()
