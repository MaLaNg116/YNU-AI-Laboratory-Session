# TCPServer
import time
from socket import *

serverPort = 2023  # 设置端口
serverSocket = socket(AF_INET, SOCK_STREAM)  # 创建TCP Socket
serverSocket.bind(('localhost', serverPort))    # 将套接字绑定到地址
serverSocket.listen(1)  # 设置监听器
time_tuple = time.localtime(time.time())    # 获取连接时间
connectionSocket, addr = serverSocket.accept()  # 获取连接体和链接地址
print(
    f"客户端{addr}连接成功，时间为：{time_tuple[0]}年{time_tuple[1]}月{time_tuple[2]}日{time_tuple[3]}时{time_tuple[4]}分{time_tuple[5]}秒。")
while True:
    sentence = connectionSocket.recv(1024)  # 接收客户端TCP数据
    print(f"来自客户端{addr}:{sentence.decode('UTF-8')}")
    msg = input('Input lowercase sentence:')    # 回复客户端TCP数据
    if sentence == exit:
        break
    connectionSocket.send(msg.encode("UTF-8"))
connectionSocket.close()
