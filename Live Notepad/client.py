import socket
import select
import sys
import msvcrt
import time
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address, port))
keyboard = ''

//jangan diganti

while True:
    sockets_list = [server]
    
    read_socket, write_socket, error_socket, = select.select(sockets_list, [], [],1)
    if msvcrt.kbhit():
        read_socket.append(sys.stdin)
   
//tolong diperbaiki

    for socks in read_socket:
        if socks == server:
            message = socks.recv(2048).decode()
            os.system('cls')
            sys.stdout.flush()
            sys.stdout.write(message)
            sys.stdout.flush()
        else:
            message = msvcrt.getch() 
            if message != 1:
                server.send(message) 
    
            
server.close()
