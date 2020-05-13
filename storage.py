#https://docs.python.org/3/library/ftplib.html                                              SEMUA TUTORIAL TERSEDIA DISINI

from ftplib import FTP
import shutil

#print('Input user: ') 
user = 'daus'
#print('Input password: ')
pswd = 'abcd1234'
#print('Input IP FTP: ')
#ipftp = input()

f = FTP('localhost')
f.login(user, pswd)

print('Input Action (LIST/RETR/STOR/MKD/PWD/DOWNPRESS) + (File Name)')

while True:
    print('>>', end='')
    action = input()
    act1 = 'LIST'
    act2 = 'RETR'
    act3 = 'STOR'
    act4 = 'MKD'
    act5 = 'PWD'
    act6 = 'DOWNPRESS'
    act7 = 'RENAME'
    act8 = 'CD'

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

    elif action.count(act6) == 1:                               #DOWNPRESS (FILE DIRECTORY DIUBAH SECARA MANUAL)
        fl = action.replace('DOWNPRESS ', '')  
        shutil.make_archive('./filezilla/' + fl, 'zip', './filezilla/' + fl)
        fz = fl + '.zip'                   
        f.retrbinary("RETR " + fz, open(fz, 'wb').write)
        f.delete(fz)

    elif action.count(act7) == 1:                               #RENAME FILE/FOLDER
        fl = action.replace('RENAME ', '')
        toname = input()
        f.rename(fl, toname)

    elif action.count(act8) == 1: 
        fl = action.replace('CD ', '')
        f.cwd(fl) 

    else:
        print('Wrong Command')
        #print('Input Action (LIST/RETR/STOR/MKD/PWD/DOWNPRESS) + (File Name)')
f.quit()
