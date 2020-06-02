import socket
import sys
import threading
import os
import json
import zipfile

_user = None

def flushBuffer():
  sys.stdout.flush()

class ClientThread(threading.Thread):
  def __init__(self, *args, **kwargs):
    self.__stop =  False
    self.s = None
    self.cb = kwargs.pop('cb')
    super(ClientThread, self).__init__(target=self.client_thread, *args, **kwargs)
    # threading.Thread.__init__(self, target=self.client_thread)

  def stop(self):
    self.__stop =  True

  def client_thread(self, port=50000, addr="239.192.1.100", buf_size=1024):
    # Create the socket
    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set some options to make it multicast-friendly
    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
      self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except AttributeError:
      pass # Some systems don't support SO_REUSEPORT

    self.s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
    self.s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)
    
    # Bind to the port
    self.s.bind(('', port))

    # Set some more multicast options
    intf = socket.gethostbyname(socket.gethostname())
    self.s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(intf))
    self.s.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton(intf))

    while True:
      # Receive the data, then unregister multicast receive membership, then close the port
      data, sender_addr = self.s.recvfrom(buf_size)
      if(self.__stop):
        self.s.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton('0.0.0.0'))
        self.s.close()
        break

      dataObj = json.loads(data.decode())
      _cmd = dataObj.get('cmd')
      if(_cmd == "chat"):
        print('>> ',dataObj.get('sender'),"says:  ", dataObj.get('message'))
        self.cb(dataObj.get('sender'), dataObj.get('message'))
        flushBuffer()
      elif(_cmd == "recv"):
        self.receiveFile(dataObj.get('path'))
      else:
        pass
      
  def send(self, data, port=50000, addr='239.192.1.100'):
    """send(data[, port[, addr]]) - multicasts a UDP datagram."""
    # Create the socket
    # self. s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # # Make the socket multicast-aware, and set TTL.
    # s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit
    # Send the data
    self.s.sendto(data, (addr, port))

  def sendFile(self, path, port=50000, host='239.192.1.100'):
    global _user
    _path = _user+"/"+path
    buf =1024
    addr = (host,port)

    _data = {
      "cmd":"recv",
      "path": path 
    }
    __data = json.dumps(_data)
    self.s.sendto(str(__data).encode(),addr)

    if os.path.isfile(_path):
      c=0
      sizeS = os.stat(_path)
      packetSize = sizeS.st_size #number of packets

      print(_path)

      NumS = int(packetSize/buf)
      NumS = NumS+1

      msgEn = str(NumS).encode('utf-8')
      self.s.sendto(msgEn, addr)

      _check = int(NumS)
      f=open(_path,"rb")
      
      while _check!=0:
        data = f.read(buf)
        self.s.sendto(data,addr)
        c += 1
        _check -= 1
        print("Packet number:" + str(c))
        print("Data sending in process:")
      f.close()
      print("Done sended")
    
    else:
      msg = "Error: File does not exist"
      msgEn = msg.encode('utf-8')
      self.s.sendto(msgEn, addr)
      print("Message Sent.")

  def uptractFolder(self, path):
    _path = _user+'/'+path

    if os.path.isdir(_path):
      owd = os.getcwd()

      folderPath = _path.split('/')
      folder_name = folderPath[len(folderPath)-1]

      print(_path[:len(_path)-len(folder_name)])
      os.chdir(_path[:len(_path)-len(folder_name)])
      
      zipPath = '{}.zip' . format(folder_name)
      zipf = zipfile.ZipFile( zipPath, 'w', zipfile.ZIP_DEFLATED)
      self.zipdir(folder_name +'/', zipf)
      zipf.close()

      os.chdir(owd)
    else:
      print("directory doesn't exist")
      return
    
    self.sendFile(path+'.zip')
    os.remove(_path+'.zip')

  def zipdir(self, path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):      
      for _dir in dirs:
        ziph.write(os.path.join(root, _dir))
      for file in files:
        ziph.write(os.path.join(root, file))

  def receiveFile(self, path):
    buf = 1024
    global _user
    _path = _user+"/"+path

    try:
      # number of paclets
      CountC, countaddress = self.s.recvfrom(buf)
      packetCnt = int(CountC.decode('utf8'))
    except ValueError:
      print("Error: File does not exist")
      return

    flag=False
    if os.path.isfile(_path) == False:
      print(_user, " will receive")
      flag = True
      f = open(_path , "wb")

    d=0
    _check = int(packetCnt)
    try:
      while _check != 0:
        data,addr = self.s.recvfrom(buf)
        if flag:
          f.write(data)
          d+=1
          print("Packet number:" + str(d))
        _check -= 1
      
      if flag:
        print("received by ",_user)
    except:
      f.close()
      self.s.close()
      print ("File Downloaded")

class ChatService():
  def __init__(self, **kwargs):
	  self._user = None
	  self.cb = None
	  self.__dict__.update(kwargs)
	  self.x = ClientThread(
		  cb = self.cb
	  )
	  self.x.start()

  def Exit(self):
    self.x.stop()
    print('bye')
    _data = {
    	"cmd":"exit",
			"sender": self._user
		}
    __data = json.dumps(_data)
    self.x.send(str(__data).encode())
    self.x.join()
			
  def SendData(self, syn):
    _data = {
			"cmd":"chat",
			"sender": self._user ,
			"message": syn
		}
    __data = json.dumps(_data)
    self.x.send(str(__data).encode())

def NoNeed(*args):
	print(args)

if __name__ == "__main__":
  cs = ChatService(
		_user="Foreign",
		cb=NoNeed
	)
  while True:
    myInput = input()
    if myInput.split()[0] == 'exit':
      cs.Exit()
    else:
      cs.SendData(str(myInput))