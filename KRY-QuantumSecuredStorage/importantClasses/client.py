import socket
import sys
import threading

rendezvous = ('192.168.64.154', 55555)

# connect to rendezvous
print('connecting to rendezvous server')
peerToPeerPort = 5033
str_val = str(peerToPeerPort )
byte_val = str_val.encode()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50006))
sock.sendto(byte_val, rendezvous)

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
        return "CreateFile;"+name+";"+format+";"+"testString"

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
