import socket
import sys
import select
from ftplib import FTP

server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# username = 'trythis'
# password = 'try123'
# host = 'localhost'
# client_socket.send(username.encode())
# client_socket.send(password.encode())
# client_socket.send(host.encode())

sys.stdout.write('>>')
username = str(input('username : '))
client_socket.send(username.encode())
sys.stdout.write('>>')
password = str(input('password : '))
client_socket.send(password.encode())
sys.stdout.write('>>')
host = str(input('IP FTP server : '))
client_socket.send(host.encode())

try:
    while True:
        sys.stdout.write('>> ')
        msg = str(input())
        client_socket.send(msg.encode())
        sys.stdout.write(client_socket.recv(1024).decode())
    
except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)