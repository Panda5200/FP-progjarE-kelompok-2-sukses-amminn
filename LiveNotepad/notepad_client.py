import socket
import select
import sys
import msvcrt
import time
import os
import threading

keyboard = ''

class NotepadLive(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.connect()
        self.cb1 = kwargs.pop('cb1')
        self.myinput = None
        super(NotepadLive, self).__init__(target=self.retrive, *args, **kwargs)

    def connect(self, ip_address='127.0.0.1', port = 8081):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_address, port))
    
    def input(self, _input):
        self.myinput = _input

    def retrive(self):
        while True:
            sockets_list = [self.server]
            read_socket, write_socket, error_socket, = select.select(sockets_list, [], [],1)
            if msvcrt.kbhit():
                read_socket.append(sys.stdin)
            
            if self.myinput != None:
                read_socket.append(self.myinput)

            for socks in read_socket:
                print(socks)
                if socks == self.server:
                    message = socks.recv(2048).decode()
                    # os.system('cls')
                    sys.stdout.flush()
                    sys.stdout.write(message)
                    sys.stdout.flush()
                    self.cb1(message)
                elif self.myinput != None:
                    message = self.myinput
                    if message != 1:
                        self.server.send(message)
                    self.myinput=None
                else:
                    message = msvcrt.getch()
                    if message != 1:
                        self.server.send(message)
    
    def disconnect(self):
        self.server.close()

def printku(message):
    print("MSG ",message)

if __name__ == "__main__":
    th = NotepadLive(
        cb1 = printku
    )
    th.start()