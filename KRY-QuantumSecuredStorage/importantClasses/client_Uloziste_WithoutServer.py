import socket
import sys
import threading
import shutil
import os



# connect to rendezvous

#ip, sport, dport = data.split(' ')
ip ="192.168.64.131"
sport = 5001
dport = 5002
host = socket.gethostname()


# punch hole
# equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
print('punching hole')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, sport))
sock.sendto((ip, dport))

print('ready to exchange messages\n')
def getFiles():
    dirs=os.listdir()
    fileNamesString=';'.join(dirs)
    return fileNamesString

def delFileOrDir(x):
    shutil.rmtree(x)

def createDir(x):
    os.mkdir(x)

def createFileBinary(x,data):
    binary_file = open(x, "wb")
    binary_file.write(data)
    binary_file.close()

def createFileText(x, data):
    f = open(x, "w")
    f.write(data)
    f.close()

def moveFile(x,y):
    os.replace(x, y)

def respGot(functionName, params,data):
    if functionName=="Move":
        fromPlace,toPlace=params.split(',')
        moveFile(fromPlace,toPlace)
    if functionName=="CreateFile":
        createFileText(params, data)

# equiv: nc -u -l 50001
def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, sport))

    while True:
        data = sock.recv(1024)
        function = data.split(';')[3]
        params = data.split(';')[4]
        dataToFile = data.split(';')[5]
        respGot(function,params,dataToFile)
        print('\rpeer: {}\n> '.format(data.decode()), end='')








listener = threading.Thread(target=listen, daemon=True);
listener.start()

# send messages
# equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dport))

while True:
    msg = input('> ')
    sock.sendto(msg.encode(), (ip, sport))
