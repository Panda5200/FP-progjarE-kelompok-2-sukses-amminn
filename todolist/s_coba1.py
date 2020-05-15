import socket
import select
import sys
from ftplib import FTP

server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

flag = 1
try:
    while True:
        read_ready, while_ready, exception = select.select(
            input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
            else:
                data = sock.recv(1024).decode()
                print(str(sock.getpeername()), str(data))
                if str(data):
                    if(flag == 1):
                        username = data
                        flag += 1
                    elif (flag == 2):
                        password = data
                        flag += 1
                    elif (flag == 3):
                        host = data
                        f = FTP(host)
                        f.login(username, password)
                        print('Welcome: ' + f.getwelcome())
                        flag += 1
                    else:
                        if (data == 'list'):
                            names = f.nlst()
                            message = 'List dir: ' + str(names) + '\n'
                            client_socket.send(message.encode())
                        # elif (data == 'dir'):
                        #     message = 'Present working dir: ' + f.pwd() + '\n'
                        #     client_socket.send(message.encode())
                        elif 'download' in data:
                            ffile = data.strip('download ')
                            fd = open(ffile, 'wb')
                            message = f.retrbinary(
                                'RETR ' + ffile, fd.write, 1024) + '\n'
                            client_socket.send(message.encode())
                        elif 'upload' in data:
                            ffile = data.strip('upload ')
                            message = f.storbinary(
                                'STOR ' + ffile, open(ffile, 'rb')) + '\n'
                            client_socket.send(message.encode())
                        # elif 'create' in data:
                        #     ffile = data.strip('create ')
                        #     message = f.mkd(ffile) + '\n'
                        #     client_socket.send(message.encode())
                else:
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
