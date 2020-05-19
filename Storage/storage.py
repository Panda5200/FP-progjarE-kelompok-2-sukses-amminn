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

#print('Input user: ') 
user = 'daus'
#print('Input password: ')
pswd = 'abcd1234'
#print('Input IP FTP: ')
#ipftp = input()

f = FTP('localhost')
f.login(user, pswd)

print('Input Action (LIST/RETR/STOR/MKD/PWD/UF/RENAME/CD/DF) + (File Name)')

while True:
    print('>>', end='')
    action = input()
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
        names = f.nlst()                                        
        print('List of directory: ' + str(names))

    elif action.count(act2) == 1:                               #DOWNLOAD
        fl = action.replace('RETR ', '')                           
        f.retrbinary("RETR " + fl, open(fl, 'wb').write)

    elif action.count(act3) == 1:                               #UPLOAD
        fl = action.replace('STOR ', '')
        f.storbinary('STOR ' + fl, open(fl, 'rb'))              

    elif action.count(act4) == 1:                               #BUAT DIRECTORY
        fl = action.replace('MKD ', '')                                           
        f.mkd(fl)                                               
    
    elif action.count(act5) == 1:                               #PRESENT WORK DIRECTORY
        print('Current working directory:' + f.pwd())

    elif action.count(act6) == 1:                               #UPLOAD FOLDER
        fl = action.replace('UF ', '')
        f.cwd('/')
        f.mkd(fl)
        f.cwd(fl)
        uploadFolder(f, fl)  
             
    elif action.count(act7) == 1:                               #RENAME FILE/FOLDER
        fl = action.replace('RENAME ', '')
        toname = input()
        f.rename(fl, toname)

    elif action.count(act8) == 1:                               #CHANGE WORKING DIRECTORY
        fl = action.replace('CD ', '')
        f.cwd(fl)

    elif action.count(act9) == 1:                               #DL FOLDER
        owd = os.getcwd()
        fl = action.replace('DF ', '')
        shutil.make_archive('./filezilla/' + fl, 'zip', './filezilla/' + fl)
        fz = fl + '.zip'                   
        f.retrbinary("RETR " + fz, open(fz, 'wb').write)
        f.delete(fz)
        os.mkdir(fl)
        with zipfile.ZipFile(fz, 'r') as zip_ref:
            zip_ref.extractall(os.chdir(fl))
        os.chdir(owd)
        os.remove(fz)

    else:
        print('Wrong Command')
        print('Input Action (LIST/RETR/STOR/MKD/PWD/UF/RENAME/CD/DF) + (File Name)')
f.quit()
