import hashlib
import json
import os
import socket
import sys
import threading

from Cryptodome.Cipher import AES

global storage_dictionary, downloadedfile
storage_dictionary = {}
downloadedfile = ""


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
        print('  ip_address_storage:          {}'.format(ip))
        print('  source port_server: {}'.format(sport))
        print('  dest port_server:   {}\n'.format(dport))

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.bind(('0.0.0.0', source_port))
        sock.sendto(b'0', (ip, dport))

        print('ready to exchange\n')


        def listen():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("0.0.0.0", sport))

            while True:
                # data = sock.recv(1024)
                # global storage_dictionary
                # storage_dictionary = json.loads(data.decode())
                # print(storage_dictionary)
                data = sock.recv(1024).decode()
                function = data.split(';')[0]
                dataload = data.split(';')[1]
                msg = self.respGot(function, dataload)
                print(msg)

        listener = threading.Thread(target=listen, daemon=True);
        listener.start()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', dport))

    def respGot(self, functionName, data):
        promena = "GOOD"
        if functionName == "DownloadFile":
            global downloadedfile
            with open('prijaty_soubor', 'wb') as file:
                while True:
                    if not data:
                        break
                    file.write(data)
            file = downloadedfile
            return file

        if functionName == "Storage":
            global storage_dictionary
            storageDict = json.loads(data)
            print(storageDict)
        return promena

    def downloadFileCommand(self, name):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', dport))
        dataToSend = connectionClient.sendDownloadCommand(self, name)
        sock.sendto(dataToSend.encode(), (ip, sport))

    def sendDownloadCommand(self, name):
        format = ""
        data = ""
        return "DownloadFile;" + name + ";" + format + ";" + data

    def getDownloadFile(self, data):
        with open('prijaty_soubor', 'wb') as file:
            while True:
                if not data:
                    break
                file.write(data)
        return file

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
        global storage_dictionary
        storageDictionary = storageDict
        return storageDictionary


    # Definujte konstanty
    BUFFER_SIZE = 1024
    KEY = b'muj_tajny_klic16'  # 16 bajtů (128 bitů)
    IV = os.urandom(AES.block_size)  # Náhodný inicializační vektor

    # Funkce pro zašifrování dat pomocí AES
    def encrypt_data(self, data, key, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(data)
        return ciphertext






