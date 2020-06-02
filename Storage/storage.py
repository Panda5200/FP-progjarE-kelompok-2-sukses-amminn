#https://docs.python.org/3/library/ftplib.html                                              SEMUA TUTORIAL TERSEDIA DISINI

import shutil
import os.path, os
from ftplib import FTP, error_perm
import sys
import zipfile

def uploadFolder(ftp, path):
    for name in os.listdir(path):
        localpath = os.path.join(path, name)
        if os.path.isfile(localpath):
            print("STOR", name, localpath)
            ftp.storbinary('STOR ' + name, open(localpath,'rb'))
        elif os.path.isdir(localpath):
            print("MKD", name)

            try:
                ftp.mkd(name)

            # ignore "directory already exists"
            except error_perm as e:
                if not e.args[0].startswith('550'): 
                    raise

            print("CWD", name)
            ftp.cwd(name)
            uploadFolder(ftp, localpath)           
            print("CWD", "..")
            ftp.cwd("..")

print('Input Action (LIST/RETR/STOR/MKD/PWD/UF/RENAME/CD/DF) + (File Name)')

class Storage():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Connect()
    
    def Connect(self):
        #print('Input user: ') 
        user = 'daus'
        #print('Input password: ')
        pswd = '123'
        #print('Input IP FTP: ')
        #ipftp = input()

        self.f = FTP('localhost')
        self.f.login(user, pswd)
    
    def Disconnect(self):
        self.f.quit()

    def StorageMethods(self, actionInput):
        # print('>>', end='')
        action = actionInput
        act1 = 'LIST'               #COMMAND MELIST FILE DAN FOLDER
        act2 = 'RETR'               #COMMAND DOWNLOAD
        act3 = 'STOR'               #COMMAND UPLOAD
        act4 = 'MKD'                #COMMAND MEMBUAT FOLDER
        act5 = 'PWD'                #COMMAND MENDAPATKAN Present Working Directory
        act6 = 'UF'                 #COMMAND UPLOAD FOLDER
        act7 = 'RENAME'             #COMMAND RENAME
        act8 = 'CD'                 #COMMAND CHANGE DIRECTORY
        act9 = 'DF'                 #COMMAND DONWLOAD FOLDER

        if action.count(act1) == 1:                                 #LIST DIRECTORY
            names = self.f.nlst()                                        
            print('List of directory: ' + str(names))
            return names

        elif action.count(act2) == 1:                               #DOWNLOAD
            fl = action.replace('RETR ', '')                           
            self.f.retrbinary("RETR " + fl, open(fl, 'wb').write)

        elif action.count(act3) == 1:                               #UPLOAD
            fl = action.replace('STOR ', '')
            self.f.storbinary('STOR ' + fl, open(fl, 'rb'))              

        elif action.count(act4) == 1:                               #BUAT DIRECTORY
            fl = action.replace('MKD ', '')                                           
            self.f.mkd(fl)                                               
        
        elif action.count(act5) == 1:                               #PRESENT WORK DIRECTORY
            res = self.f.pwd()
            print('Current working directory:' + str(res) )
            return res
            

        elif action.count(act6) == 1:                               #UPLOAD FOLDER
            fl = action.replace('UF ', '')
            self.f.cwd('/')
            self.f.mkd(fl)
            self.f.cwd(fl)
            uploadFolder(self.f, fl)  
                
        elif action.count(act7) == 1:                               #RENAME FILE/FOLDER
            myAction = action.split()
            fl = myAction[1]
            toname = myAction[2]
            self.f.rename(fl, toname)

        elif action.count(act8) == 1:                               #CHANGE WORKING DIRECTORY
            fl = action.replace('CD ', '')
            self.f.cwd(fl)

        elif action.count(act9) == 1:                               #DL FOLDER
            owd = os.getcwd()
            fl = action.replace('DF ', '')
            shutil.make_archive('./filezilla/' + fl, 'zip', './filezilla/' + fl)
            fz = fl + '.zip'                   
            self.f.retrbinary("RETR " + fz, open(fz, 'wb').write)
            self.f.delete(fz)
            os.mkdir(fl)
            with zipfile.ZipFile(fz, 'r') as zip_ref:
                zip_ref.extractall(os.chdir(fl))
            os.chdir(owd)
            os.remove(fz)

        else:
            print('Wrong Command')
            print('Input Action (LIST/RETR/STOR/MKD/PWD/UF/RENAME/CD/DF) + (File Name)')

if __name__ == "__main__":
    s = Storage()
    s.StorageMethods("LIST")
    s.StorageMethods("RETR tes.txt")
    s.StorageMethods("STOR login.kv")