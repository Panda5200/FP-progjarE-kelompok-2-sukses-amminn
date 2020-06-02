import socket
import sys
import select
from ftplib import FTP
import pickle

class todolistClient():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect()

    def connect(self):
        server_address = ('localhost', 5000)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(server_address)
    
    def GetTask(self):
        msg = 'list'
        self.client_socket.send(msg.encode())
        res = self.client_socket.recv(1024)
        return pickle.loads(res)

    def DeleteTask(self, filename):
        msg = 'delete {}'.format(filename)
        self.client_socket.send(msg.encode())

    def CreateTask(self, taskku):
        msg = 'create {}'.format(taskku)
        self.client_socket.send(msg.encode())
        res = self.client_socket.recv(1024)
        print(res.decode())
        # return 
    
    def SetTaskComplete(self, filename, isComplete):
        fss = filename.split("~")
        if len(fss)>1 and isComplete == False:
            msg = 'rename {} {}'.format(filename, fss[1])
            self.client_socket.send(msg.encode())
        elif len(fss)==1 and isComplete == True:
            msg = 'rename {} ~{}'.format(filename, filename)
            self.client_socket.send(msg.encode())

    def TodoThread(self):
        try:
            while True:
                sys.stdout.write('>> ')
                msg = str(input())
                self.client_socket.send(msg.encode())
                res = self.client_socket.recv(1024)
                print(pickle.loads(res))
            
        except KeyboardInterrupt:
            self.client_socket.close()
            sys.exit(0)

if __name__ == '__main__':
    t = todolistClient()
    print(t.GetTask())
    # t.DeleteTask("e1b8c666-6351-4f4c-8cf6-ad8cf8c1ab3b.txt")
    