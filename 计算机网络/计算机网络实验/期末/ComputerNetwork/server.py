import socket
import threading
import os
import struct
import json


def server(conn, addr, home):
    print('新客户端：' + str(addr))
    # 进入当前用户主目录
    os.chdir(home)
    while True:
        data = conn.recv(100).decode().lower()
        # 显示客户端输入的每一条命令
        print(data)
        # 客户端退出
        if data in ('quit', 'q'):
            break
        # 查看当前文件夹的文件列表
        elif data in ('list', 'ls', 'dir'):
            files = str(os.listdir(os.getcwd()))
            files = files.encode()
            conn.send(struct.pack('I', len(files)))
            conn.send(files)
        # 切换至上一级目录
        elif ''.join(data.split()) == 'cd..':
            cwd = os.getcwd()
            newCwd = cwd[:cwd.rindex('\\')]
            # 考虑根目录的情况
            if newCwd[-1] == ':':
                newCwd += '\\'
            # 限定用户主目录
            if newCwd.lower().startswith(home):
                os.chdir(newCwd)
                conn.send(b'ok')
            else:
                conn.send(b'error')
        # 查看当前目录
        elif data in ('cwd', 'cd'):
            conn.send(str(os.getcwd()).encode())
        elif data.startswith('cd '):
            # 指定最大分隔次数，考虑目标文件夹带有空格的情况
            # 只允许使用相对路径进行跳转
            data = data.split(maxsplit=1)
            if len(data) == 2 and os.path.isdir(data[1]) \
                    and data[1] != os.path.abspath(data[1]):
                os.chdir(data[1])
                conn.send(b'ok')
            else:
                conn.send(b'error')

        # 从客户端上传文件
        elif data.startswith('upload '):
            isFileExist = conn.recv(20)
            # 文件不存在
            if isFileExist != b'ok':
                print('error')
            # 文件存在，开始下载
            else:
                print('uploading.', end='')
                fp = open(data.split()[1], 'wb')
                while True:
                    print('.', end='')
                    data = conn.recv(4096)
                    if data == b'overxxxx':
                        break
                    fp.write(data)
                    conn.send(b'ok')
                fp.close()
                print('ok')

        # 下载文件
        elif data.startswith('get '):
            data = data.split(maxsplit=1)
            # 检查文件是否存在
            if len(data) == 2 and os.path.isfile(data[1]):
                conn.send(b'ok')
                fp = open(data[1], 'rb')
                while True:
                    content = fp.read(4096)
                    # 发送文件结束
                    if not content:
                        conn.send(b'overxxxx')
                        break
                    # 发送文件内容
                    conn.send(content)
                    if conn.recv(10) == b'ok':
                        continue
                fp.close()
            else:
                conn.send(b'no')
        # 无效命令
        else:
            pass
    conn.close()
    print(str(addr) + '关闭连接')


# 创建Socket，监听本地端口，等待客户端连接
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('10.103.185.104', 5000))
sock.listen(5)
while True:
    conn, addr = sock.accept()
    # 验证客户端输入的用户名和密码是否正确
    with open("./users.json", "r", encoding="UTF-8") as users:
        users = json.load(users)
    userinfo = None
    userId, userPwd = conn.recv(1024).decode().split(',')
    for i in range(len(users)):
        if userId == users[i]["username"] and userPwd == users[i]["password"]:
            userinfo = users[i]
            break
    if userinfo:
        conn.send(b'ok')
        # 为每个客户端连接创建并启动一个线程，参数为连接、客户端地址、客户主目录
        home = userinfo["home"]
        t = threading.Thread(target=server, args=(conn, addr, home))
        t.daemon = True
        t.start()
    else:
        conn.send(b'error')
