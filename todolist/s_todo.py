import socket
import sys
import select
import os
from ftplib import FTP

s_add = ('127.0.0.1', 5001)
s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_sock.bind(s_add)
s_sock.listen(5)
input_sock = [s_sock]

flag = 1
try:
    while True:
        readable, writable, exeptional = select.select(input_sock, [], [])
        for s in readable:
            if s == s_sock:
                c_sock, c_add = s_sock.accept()
                input_sock.append(c_sock)
            else:
                todo = s.recv(1024).decode()
                print(str(s.getpeername()), str(todo))
                if str(todo):
                    if(flag == 1):
                        uname = todo
                        flag += 1
                    elif(flag == 2):
                        psw = todo
                        flag += 1
                    elif(flag == 3):
                        host = todo
                        your = FTP(host)
                        your.login(uname, psw)
                        print('Selamat Datang: ' + your.getwelcome())
                        flag += 1
                    else:
                        if(todo == 'list'):
                            cmd = your.nlst()
                            msg = 'Daftar agenda: ' + str(cmd) + '\n'
                            c_sock.send(msg.encode())
                        elif 'read' in todo:
                            baca = todo.strip('read ')
                            cmd = open(baca+".txt", "r")
                            msg = cmd.read()
                            c_sock.send(msg.encode())
                        elif 'delete' in todo: # masih error -> ftplib.error_perm: 550 File not found
                            cmd = todo.strip('delete ')
                            msg = your.delete(cmd)
                            c_sock.send(msg.encode())
                        elif 'done' in todo:
                            cmd = todo.strip('done ')
                            msg = your.rename(cmd, '[COMPLETED]'+cmd)
                            c_sock.send(msg.encode())
                        elif 'create' or 'update' or 'agenda' in todo:
                            if 'create' in todo:
                                buat = todo.strip('create ')
                            elif 'update' in todo:
                                buat = todo.strip('update ')
                            elif 'agenda' in todo:
                                cmd = open(buat+".txt", "w")
                                msg = cmd.write(todo)
                                note = 'OK'
                                c_sock.send(note.encode())
                else:
                    s.close()
                    input_sock.remove(s)            
except KeyboardInterrupt:
    s_sock.close()
    sys.exit(0)
