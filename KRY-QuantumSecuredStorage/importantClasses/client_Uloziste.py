import socket
import sys
import threading
import shutil
import os

rendezvous = ('100.64.129.130', 55555)

# connect to rendezvous
print('connecting to rendezvous server')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50001))
sock.sendto(b'0', rendezvous)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

data = sock.recv(1024).decode()
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))
print('  dest port:   {}\n'.format(dport))

# punch hole
# equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
print('punching hole')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(b'0', (ip, dport))

print('ready to exchange messages\n')
def getFiles():
    dirs=os.listdir()
    fileNamesString=';'.join(dirs)
    return fileNamesString

def delFileOrDir(x):
    shutil.rmtree(x)
    return returnDirectoryInfo()

def delFile(x):
    shutil.rmtree(x)
    return returnDirectoryInfo()

def createDir(x):
    os.mkdir(x)
    return returnDirectoryInfo()

def createFileBinary(x,data):
    binary_file = open(x, "wb")
    binary_file.write(data)
    binary_file.close()
    return returnDirectoryInfo()

def createFileText(x, data):
    f = open(x, "w")
    f.write(data)
    f.close()
    return returnDirectoryInfo()

#def sendFile(name):


def moveFile(x,y):
    os.replace(x, y)
    return returnDirectoryInfo()

def getFile(path):
    data = open(path, "rb")
    return data

def respGot(functionName, params,format,data):
    currentDirInfo=""
    if functionName=="Move":
        fromPlace,toPlace=params.split(',')
        currentDirInfo=moveFile(fromPlace,toPlace)

    if functionName=="CreateFile":
        currentDirInfo=createFileText("Uloziste/"+params+format, data)

    if functionName=="DeleteFile":
        currentDirInfo=delFile("Uloziste/"+params)

    if functionName=="DownloadFile":
        fileData=getFile("Uloziste/"+params)
        sock.sendto(fileData, (ip, sport))
        currentDirInfo =returnDirectoryInfo()

    if functionName=="EditFile":
        currentDirInfo=createFileText("Uloziste/"+params+format, data)

    return currentDirInfo

def returnDirectoryInfo():
    dirInfo=os.listdir('Uloziste/')
    return ";".join(dirInfo)


# equiv: nc -u -l 50001
def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))

    while True:
        data = sock.recv(1024).decode()
        function = data.split(';')[0]
        params = data.split(';')[1]
        format = data.split(';')[2]
        dataToFile = data.split(';')[3]
        msg=respGot(function,params,format,dataToFile)
        print('\rpeer: {}\n> '.format(data), end='')
        sock.sendto(msg.encode(), (ip, sport))








listener = threading.Thread(target=listen, daemon=True);
listener.start()

# send messages
# equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dport))

while True:
    msg = input('> ')
    sock.sendto(msg.encode(), (ip, sport))
