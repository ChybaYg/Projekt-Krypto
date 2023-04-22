import hashlib
import json
import socket
import threading

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from pynewhope import newhope

# Inicializace globálních proměnných a konstanty BUFFER_SIZE
global storage_dictionary, key_AES, iv_AES, warning_message, verification_logs, authenticated_access
authenticated_access = ""
verification_logs = ""
warning_message = ""
storage_dictionary = {}
BUFFER_SIZE = 65000
key_AES = b''
iv_AES = b''


class ConnectionClient():

    # Převod ze získaného Post-kvantového klíče na klíč pro použití AES-256 a inicializační vektor
    # AES klíč je tvořen prvními 32 číslicemi sdíleného klíče, IV 16 číslicemi
    def keyToBytes(self, key):
        global key_AES, iv_AES
        string = ''.join(str(x) for x in bytes(key))
        key_AES = string[:32]
        key_AES = bytes(key_AES, 'utf-8')
        iv_AES = string[:16]
        iv_AES = bytes(iv_AES, 'utf-8')

    # Metoda pro šifrování dat, využívá se AES-256 v módu CBC
    def encryptData(self, data, key, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(data)
        return ciphertext

    # Metoda pro dešifrování dat a vyjmutí nul z přenesené zprávy
    def decryptData(self, data, key, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(data)
        return plaintext.rstrip(b'\0')

    # Metoda implementující post-kvantovou výměnu klíčů
    def keyExchange(self):
        global client_key
        client_key, client_message = newhope.keygen()  # Vytvoření nové dvojice klíčů pomocí alg. NewHope
        client_kem = str(client_message)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', destination_port))
        data_to_send = "KEM<EoR><EoR>" + client_kem + "<EoR>"
        message = data_to_send.encode().ljust(BUFFER_SIZE, b'\0')  # Doplnění zprávy "0" do velikosti BUFFER_SIZE
        message_to_send = b'<UNCRYPTED>' + message + b'<END>'
        sock.sendto(message_to_send, (ip_address_storage, source_port))  # Odeslání zprávy socketem

    # Metoda, jenž vytvoří otisk hesla a ten spolu s jménem uživatele
    def getAccess(self, user, password):
        hash_password = hashlib.sha256(password.encode()).hexdigest()  # Vytvoření hash otisku hesla
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', destination_port))
        data_to_send = "GetAccess<EoR>" + user + "<EoR>" + hash_password + "<EoR><EoR>"
        message = data_to_send.encode().ljust(BUFFER_SIZE, b'\0')  # Doplnění zprávy "0" do velikosti BUFFER_SIZE
        message_to_send = b'<UNCRYPTED>' + message + b'<END>'
        sock.sendto(message_to_send, (ip_address_storage, source_port))  # Odeslání zprávy socketem

    # Metoda vracející hodnotu dotazu o přístup do uložiště
    def returnAccessInfo(self):
        if authenticated_access != "":
            access = authenticated_access
            self.authenticated = ""
            return access
        else:
            return authenticated_access

    # Metoda pro připojení k serveru, následně k uložišti a naslouchání/příjem dat
    def connection(self, ip_address_server, port_server):
        # Připojení k serveru (a odeslání požadavku o připojení k uložišti)
        rendezvous = (ip_address_server, port_server)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', 50001))
        sock.sendto(b'0', rendezvous)

        while True:
            data = sock.recv(1024).decode()
            if data.strip() == 'ready':
                break

        data = sock.recv(1024).decode()
        # Po přijetí zprávy od serveru klient ze zprávy zjistí ip_address adresu a port uložiště
        global ip_address_storage, source_port, destination_port
        ip_address_storage, source_port, destination_port = data.split(' ')
        source_port = int(source_port)
        destination_port = int(destination_port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b'0', (ip_address_storage, destination_port))

        # Funkce naslouchání klienta
        def listen():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("0.0.0.0", source_port))
            ciphertext = b''
            while True:
                while True:
                    data_recieved = sock.recv(BUFFER_SIZE)

                    if b'<UNCRYPTED>' in data_recieved:
                        data_recieved = data_recieved.removeprefix(b'<UNCRYPTED>')  # Odstranění prefixu ze zprávy
                        if b'<END>' in data_recieved:
                            data_recieved = data_recieved.removesuffix(b'<END>')    # Odstranění suffixu ze zprávy
                        ciphertext += data_recieved
                        recieved_data_decoded = ciphertext.decode()     # Převod přijaté zprávy
                        # Rozdělení přijatých dat, na jednotlivé proměnné (jenž jsou rozděleny značkou
                        # <EoR> značící "End of region")
                        function = recieved_data_decoded.split('<EoR>')[0]
                        filename = recieved_data_decoded.split('<EoR>')[1]
                        # Volání funkce gotResponse
                        self.gotResponse(function, filename)
                        ciphertext = b''
                        break

                    ciphertext += data_recieved
                    decrypted_message = self.decryptData(ciphertext, key_AES, iv_AES)
                    if b'<END>' in decrypted_message:
                        decrypted_message = decrypted_message.removesuffix(b'<END>')    # Odstranění suffixu ze zprávy
                    decrypted_message = decrypted_message.decode()      # Převod přijaté zprávy
                    # Rozdělení přijatých dat, na jednotlivé proměnné (jenž jsou rozděleny značkou
                    # <EoR> značící "End of region")
                    function = decrypted_message.split('<EoR>')[0]
                    filename = decrypted_message.split('<EoR>')[1]
                    # Volání funkce gotResponse
                    self.gotResponse(function, filename)
                    ciphertext = b''

        listener = threading.Thread(target=listen, daemon=True)
        listener.start()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', destination_port))

    # Metoda, která určí dle přijatých dat, co se má dále provést za akci
    def gotResponse(self, function, data):
        global verification_logs, authenticated_access

        # Akce spojené s přístupem do databáze (zda jsou přihlašovací údaje legitimní či nikoli)
        if function == "Authenticated":
            authenticated_access = "Authenticated"
        if function == "Non-authenticated_access":
            authenticated_access = "Non-authenticated_access"

        # Akce spojené s ověřováním logů, které může využít pouze uživatel Admin
        if function == "Same":
            verification_logs = "Same"
        if function == "Different":
            verification_logs = "Different"

        # Akce pro stažení souboru z uložiště
        if function == "DownloadFile":
            global download_path
            data = data.encode()
            path = download_path
            with open(path, 'wb') as file:      # Vytvoření nového souboru na základě cesty, kterou jsme vybrali
                # if not data:
                #     file.close()
                # else:
                if data:
                    file.write(data)            # Zápis přijatých dat do souboru
            file.close()

        # Akce pro získání výpisu uložiště daného uživatele
        if function == "MyStorage":
            global storage_dictionary
            storage_dictionary = json.loads(data)       # Převod přenešené zprávy na slovník

        # Akce provedená v případě, kdy se jedná o výměnu klíče mezi uživatelem a uložištěm
        if function == "KEM response":
            storage_message = eval(data)
            shared_key = newhope.sharedA(storage_message, client_key)   # Vytvoření sdíleného klíče
            self.keyToBytes(shared_key)     # Převod sdíleného post-kvantového klíče na klíč pro AES

    # Metoda odesílající požadavek na uložiště o stažení daného souboru
    def downloadFile(self, user, filename):
        data_to_send = "DownloadFile<EoR>" + user + "<EoR>" + filename + "<EoR>"
        self.sendData(data_to_send)

    # Metoda pro předání cesty, kam má být stahovaný soubor uložen
    def getPathDownloadedFile(self, path):
        global download_path
        download_path = path

    # Metoda odesílající soubor s potřebnými daty na uložiště
    def uploadFile(self, user, filename, data):
        data_to_send = "UploadFile<EoR>" + user + "<EoR>" + data + "<EoR>" + filename + "<EoR>"
        self.sendData(data_to_send)

    # Metoda odesílající příkaz uložišti o odstranění souboru
    def deleteFile(self, user, filename):
        data_to_send = "DeleteFile<EoR>" + user + "<EoR><EoR>" + filename + "<EoR>"
        self.sendData(data_to_send)

    # Metoda odesílající požadavek na uložiště o získání seznamu souborů na uložišti
    def getStorage(self, user):
        data_to_send = "MyStorage<EoR>" + user + "<EoR><EoR>"
        self.sendData(data_to_send)

    # Metoda vracející proměnnou s informacemi, jaké soubory se v uložišti nachází
    def getStorageFull(self):
        return storage_dictionary

    # Metoda odesílající požadavek na ověření záznamů (logů)
    def verifyLogs(self):
        data_to_send = "VerifyLogs<EoR><EoR><EoR>"
        self.sendData(data_to_send)
        return verification_logs

    # Metoda vracející hodnotu ověřených záznamů
    def returnLogsInfo(self):
        return verification_logs

    # Metoda pro odeslání zprávy na uložiště
    def sendData(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', destination_port))
        message = data.encode().ljust(BUFFER_SIZE, b'\0')     # Doplnění zprávy "0" na velikost BUFFER_SIZE
        message_to_send = message + b'<END>'      # Přidání suffixu na konec zprávy, aby bylo zřetelné, kde končí data
        padded_data = pad(message_to_send, 16)    # Pad zprávy na bloky velké 16B (nutnost, jestliže je využíván CBC mod)
        # Zašifrování a odeslání zprávy
        sock.sendto(self.encryptData(padded_data, key_AES, iv_AES), (ip_address_storage, source_port))

    # Metoda uzavírající socket
    def closeConnection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', destination_port))
        data_to_send = "CloseConnection<EoR><EoR><EoR>"
        message = data_to_send.encode().ljust(BUFFER_SIZE, b'\0')   # Doplnění zprávy "0" na velikost BUFFER_SIZE
        message_to_send = b'<UNCRYPTED>' + message + b'<END>'       # Přidání prefixu a suffixu
        sock.sendto(message_to_send, (ip_address_storage, source_port))     # Odeslání zprávy
        sock.close()        # Uzavření socketu
