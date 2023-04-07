import json
import socket
import sys
import threading

global storageDict
storageDict = {}

class connectionClient():
    def connection(self, ipAddress, port):
        rendezvous = (ipAddress, port)
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
        global ip,sport,dport
        ip, sport, dport = data.split(' ')
        sport = int(sport)
        dport = int(dport)

        print('\ngot peer')
        print('  ip:          {}'.format(ip))
        print('  source port: {}'.format(sport))
        print('  dest port:   {}\n'.format(dport))

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.bind(('0.0.0.0', sport))
        sock.sendto(b'0', (ip, dport))

        print('ready to exchange\n')


        def listen():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("0.0.0.0", sport))

            while True:
                data = sock.recv(1024)
                global storageDict
                storageDict = json.loads(data.decode())
                print(storageDict)
                #print('\rpeer: {}\n> '.format(data.decode()), end='')

        listener = threading.Thread(target=listen, daemon=True);
        listener.start()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', dport))

    def sendDeleteFileCommand(self,name):
        data = self.getDataTextUserInput()
        return "DeleteFile;" + name + ";" + data

    def sendCreateFileCommand(self, name, format):
        if format == ".txt":
            data = self.getDataTextUserInput()
            return "CreateFile;" + name + ";" + format + ";" + data

    def getDataTextUserInput(self):
        data = input('> ')
        return data

    # def sendDownloadFileCommand():

    # def sendUploadFileCommand():

    # def sendEditFileCommand():

    def sendMess(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', dport))
        msg = 'JSEM BUH'
        format = ".txt"
        dataToSend = connectionClient.sendCreateFileCommand(self, msg, '.txt')
        sock.sendto(dataToSend.encode(), (ip, sport))

    def uploadFile(self,path):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', dport))
        with open(path, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(1024)
                if not bytes_read:
                    # file transmitting is done
                    break
                sock.sendto(bytes_read, (ip, sport))

    def sendStorageCommand(self):
        name = "Uloziste"
        format = ""
        data = ""
        return "MyStorage;" + name + ";" + format + ";" + data

    def getStorage(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', dport))
        dataToSend = connectionClient.sendStorageCommand(self)
        sock.sendto(dataToSend.encode(), (ip, sport))

    def getStorageFull(self):
        global storageDict
        storageDictionary = storageDict
        return storageDictionary





