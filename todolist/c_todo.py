import socket
import sys
import select
from ftplib import FTP

s_add = ('127.0.0.1', 5000)
c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_sock.connect(s_add)

uname = str(input('username : '))
c_sock.send(uname.encode())
pwd = str(input('password : '))
c_sock.send(pwd.encode())
host = str(input('ip ftp server : '))
c_sock.send(host.encode())

try:
    while True:
        sys.stdout.write('\ncommand :\n`list` untuk melihat daftar agenda\n`create <filename tanpa extensi>` untuk membuat agenda baru\n`read <filename tanpa extensi>` untuk melihat isi agenda\n`update <filename tanpa extensi>` untuk memperbaharui agenda\n`delete <filename.txt>` untuk menghapus agenda\n`done <filename.txt>` untuk menyelesaikan agenda\n')
        sys.stdout.write('>> ')
        msg = str(input())
        if 'create' in msg:
            c_sock.send(msg.encode())
            # sys.stdout.write(c_sock.recv(1024).decode())
            
            agenda = input("agenda : ")
            durasi = input("batas waktu : ")
            teks = "agenda : {}\nbatas waktu : {}".format(agenda, durasi)
            c_sock.send(teks.encode())
            sys.stdout.write(c_sock.recv(1024).decode())
        elif 'update' in msg:
            c_sock.send(msg.encode())
            # sys.stdout.write(c_sock.recv(1024).decode())
            
            agenda = input("agenda : ")
            durasi = input("batas waktu : ")
            teks = "agenda : {}\nbatas waktu : {}".format(agenda, durasi)
            c_sock.send(teks.encode())
            sys.stdout.write(c_sock.recv(1024).decode())
        else:
            c_sock.send(msg.encode())
            sys.stdout.write(c_sock.recv(1024).decode())
        
except KeyboardInterrupt:
    c_sock.close()
    sys.exit(0)
