import socket
import select
import sys
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address,port))
server.listen(100)
list_of_clients = []

text = ''

def clientthread(conn,addr,ms):
    global text
    
    while True:
        
        try:  
            message = conn.recv(2048)
            
            if ord(message) not in (13,3):
                if ord(message) in (127,8):
                    text = text[:-1]
                    sys.stdout.write(f"\r{' '*100}\r")
                    sys.stdout.flush()
                    sys.stdout.flush()            
                else:
                    message = message.decode()
                    text = text + message
                    sys.stdout.flush()
            print(text)
            # if text:
            message_to_send = text
            broadcast(message_to_send, conn)
            # else:
                # remove(conn)
        except:
            continue

def broadcast(message,connection):
    for clients in list_of_clients:
        try:
            clients.send(message.encode())
        except:
            clients.close()
            remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print (addr[0] + ' connected')
    # ms =''
    sys.stdout.write(f"\r{' '*100}\r")
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

    threading.Thread(target=clientthread,args=(conn, addr,text)).start()

conn.close()