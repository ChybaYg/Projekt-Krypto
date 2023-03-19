import socket
import sys
import threading


# connect to rendezvous

#ip, sport, dport = data.split(' ')
ip ="192.168.64.131"
sport = 5002
dport = 5001
host = socket.gethostname()


# punch hole
# equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
print('punching hole')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, sport))
sock.sendto((ip, dport))
print('ready to exchange messages\n')

# listen for
# equiv: nc -u -l 50001
def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')


def sendDeleteFileCommand(name):

    data=getDataTextUserInput()
    return "CreateFile;"+name+";"+data

def sendCreateFileCommand(name,format):
    if format=="txt":
        data=getDataTextUserInput()
        return "CreateFile;"+name+";"+format+";"+data

def getDataTextUserInput():
    data = input('> ')
    return data

#def sendDownloadFileCommand():


#def sendUploadFileCommand():

#def sendMoveFileCommand():

#def sendEditFileCommand():


listener = threading.Thread(target=listen, daemon=True);
listener.start()

# send messages
# equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dport))

while True:
    msg = input('> ')
    format="txt"
    dataToSend=sendCreateFileCommand(msg,format)
    sock.sendto(dataToSend.encode(), (ip, sport))
