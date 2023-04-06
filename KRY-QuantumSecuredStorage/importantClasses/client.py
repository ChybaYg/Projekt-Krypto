import socket
import sys
import threading

from importantClasses.ConnectionObject import ConnectionObject

rendezvous = ('100.64.129.130', 55555)
connectionInfo=ConnectionObject("User","TajneHeslo")
hostname, hashedPassword = "user", "hashedPassword"
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
#sock.bind(('0.0.0.0', sport))
sock.sendto(b'0', (ip, dport))

print('ready to exchange messages\n')

# listen for
# equiv: nc -u -l 50001
def connect(hostname,hashedPassword,connectionInfo):
    request = ("Validate"+";"+hostname+";"+hashedPassword).encode()
    sock.sendto(request, (ip, sport))
    connectionInfo.connected = sock.recv(1024).decode().Split(";")[1]

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))

    while True:
        if connectionInfo.connected==False:
            connect(hostname, hashedPassword,connectionInfo)
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')


def sendDeleteFileCommand(name):
    return ("DeleteFile;"+name).encode()

def sendCreateFileCommand(name):
    data=getDataTextUserInput()
    return ("CreateFile;"+name+";"+data).encode()

def getDataTextUserInput():
    data = input('> ')
    return data

def sendDownloadFileCommand(path):
    return ("DownloadFile;" + path + ";" "nothing else matter").encode()

def sendUploadFileCommand(pathFrom):
    fileData=open(pathFrom, "rb")
    name,format=pathFrom.split("\\")[-1].split(".")
    return ("CreateFile;" + name + ";" + fileData).encode()

def sendEditFileCommand(path):
    downloadCommand=sendDownloadFileCommand(path)
    sock.sendto(downloadCommand, (ip, sport))
    data = sock.recv(1024).decode()
    #editedData=showDataInUIEditorWhichAllowsEditing
    #return ("CreateFile;" + name + ";" + editedData).encode()




#def sendEditFileCommand():


listener = threading.Thread(target=listen, daemon=True);
listener.start()

# send messages
# equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dport))

while True:
    msg = input('> ')
    dataToSend=sendCreateFileCommand(msg,format)
    sock.sendto(dataToSend, (ip, sport))
