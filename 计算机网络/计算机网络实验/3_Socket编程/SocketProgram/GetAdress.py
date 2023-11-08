import socket


while True:
    url = input("请输入你要查询的URL地址：")   # 设置循环从而不断输入URL地址
    if url == "host":   # 判断当输入host时，返回本机的ip地址
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print(f"本机IP地址为{ip}")
    elif url == "exit":    # 程序出口
        break
    else:   # 当输入不为"exit"也不为"host"时，返回对应URL的IP地址
        ip = socket.gethostbyname(url)
        print(f"{url}对应的IP地址为{ip}")