from ftplib import FTP
import socket
import select
import sys
import os
import uuid
import io
import pickle

server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

def CreateFile():
    nama='{}.txt' . format(uuid.uuid4())
    print("create ops {}" . format(nama))
    try:
        if os.path.exists(nama):
            return "File Exist"
        File = open(nama,'w+')
        File.write("Our Task")
        File.close()
        return nama
    except:
        return None

def DeleteFile(nama):
    try:
        os.remove(nama)
    except:
        pass

username = 'todo'
password = '123'
host = 'localhost'
f = FTP(host)
f.login(username, password)

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
                if (data == 'list'):
                    names = f.nlst()
                    message = 'List todo: ' + str(names) + '\n'
                    Tasks = []
                    for name in names:
                        r = io.BytesIO()
                        task = f.retrbinary('RETR ' + name, r.write) + '\n'
                        val = r.getvalue().decode()
                        Tasks.append(val)
                    message += 'Isi Todo ' +str(Tasks)
                    res_data = {"files":names, "tasks":Tasks}
                    res = pickle.dumps(res_data)
                    client_socket.send(res)
                elif 'download' in data:
                    ffile = data.split()[1]
                    print(ffile)
                    fd = open(ffile, 'wb')
                    message = f.retrbinary(
                        'RETR ' + ffile, fd.write, 1024) + '\n'
                    client_socket.send(message.encode())
                elif 'upload' in data:
                    ffile = data.split()[1]
                    message = f.storbinary(
                        'STOR ' + ffile, open(ffile, 'rb')) + '\n'
                    client_socket.send(message.encode())
                elif 'create' in data:
                    ffile = CreateFile()
                    print(ffile)
                    message = f.storbinary(
                        'STOR ' + ffile, open(ffile, 'rb')) + '\n'
                    client_socket.send(message.encode())
                    DeleteFile(ffile)
                elif 'delete' in data:
                    ffile = data.split()[1]
                    message = f.delete(ffile)
                    # client_socket.send(res)
                elif 'rename' in data:
                    dataku = data.split()
                    f.rename(dataku[1], dataku[2])
            else:
                sock.close()
                input_socket.remove(sock)
                

# except KeyboardInterrupt:
#     server_socket.close()
#     sys.exit(0)

# else:
    #     sock.close()
    #     input_socket.remove(sock)
