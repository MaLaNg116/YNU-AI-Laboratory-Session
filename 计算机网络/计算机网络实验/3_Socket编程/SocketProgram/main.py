from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)

# 绑定 IP 地址和端口号
serverSocket.bind(('192.168.64.1', 6789))

# 开始监听连接
print('Server is running on http://192.168.64.1:6789')

while True:
    # 等待客户端连接
    print('Ready to serve...')
    serverSocket.listen(1)
    connectionSocket, addr = serverSocket.accept()

    try:
        # 接收客户端请求
        message = connectionSocket.recv(1024).decode()

        # 获取请求的文件路径
        filename = message.split()[1][1:]

        # 读取文件内容
        with open(filename, 'r', encoding='utf-8') as f:
            outputdata = f.readlines()

        # 构造 HTTP 响应
        response = 'HTTP/1.1 200 OK\r\n\r\n'
        response += ''.join(outputdata)

        # 发送响应给客户端
        connectionSocket.sendall(response.encode())

        # 关闭连接
        connectionSocket.close()

    except IOError:
        # 构造 HTTP 响应
        response = 'HTTP/1.1 404 Not Found\r\n\r\n'
        response += '<h1>404 Not Found</h1>'

        # 发送响应给客户端
        connectionSocket.sendall(response.encode())

        # 关闭连接
        connectionSocket.close()

serverSocket.close()
sys.exit()
