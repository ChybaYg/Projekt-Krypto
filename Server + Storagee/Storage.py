import hashlib
import json
import logging
import threading
import re
import socket
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from pynewhope import newhope

global keyAES, ivAES, should_stop
should_stop = False
keyAES = b''
ivAES = b''

# Nastavení ip_address adresy a portu serveru
rendezvous = ('192.168.184.128', 55555)

# Připojení na server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50001))
sock.sendto(b'0', rendezvous)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready': #V případě přijmutí zprávy 'ready' je uložiště připojeno na server
        break

# Na základě přijaté zprávy, nastavení ip adresy a portu uživatele do proměnných
data = sock.recv(1024).decode()
ip_address, source_port, destination_port = data.split(' ')
source_port = int(source_port)
destination_port = int(destination_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b'0', (ip_address, destination_port))


# Metoda převádějící sdílený post-kvantový klíč na klíč (32B) a inicializační vektor(16B) AES-256
def keyToBytes(key):
    global keyAES, ivAES
    string = ''.join(str(x) for x in bytes(key))
    keyAES = string[:32]
    keyAES = bytes(keyAES, 'utf-8')
    ivAES = string[:16]
    ivAES = bytes(ivAES, 'utf-8')


# Metoda, která určí dle přijatých dat, co se má dále provést za akci a vrací potřebné informace
def gotResponse(function, user, data, filename):
    # V případě, že uživatel posílá žádost o přístup k uložišti
    if function == "GetAccess":
        # Volání metody "verifyAccess", kde se předává jméno uživatele a hash hesla, metoda vrací výsledek přístupu
        message = verifyAccess(user, data)
        return message

    # Pokud uživatel posílá žádost o ustanovení klíčů
    if function == "KEM":
        tuple = eval(data)
        storage_shared_key, storage_message = newhope.sharedB(tuple) # Vytvoření klíče a zprávy odesílající uživateli
        keyToBytes(storage_shared_key)  # Převod sdíleného klíče na klíč a IV pro AES-256
        kem = "KEM response<EoR>" + str(storage_message) + "<EoR>"
        return kem

    # Jestliže uživatel žádá výpis obsahu uložiště
    if function == "MyStorage":
        message = getStorage(user) # Uložení obsahu uložiště do proměnné
        storage = "MyStorage<EoR>" + json.dumps(message) + "<EoR>"
        return storage

    # Nahrání souboru
    if function == "UploadFile":
        path = f"{user}/{filename}"     # Určení cesty, kam se má soubor nahrát a jak se má jmenovat
        data = data.encode()
        with open(path, 'wb') as file:  # Vytvoření a zapsání do souboru
            # if not data:
            #     file.close()
            # else:
            #     file.write(data)
            if data:
                file.write(data)
        file.close()
        logs(function, user, filename)  # Zapsání provedené akce do souboru se záznamy
        return "Uploaded<EoR>"

    # Požadavek na stažení souboru
    if function == "DownloadFile":
        path = f"{user}/{data}"     # Určení o jaký soubor z kterého adresáře se jedná
        logs(function, user, data)  # Zápis o žádost o stažení souboru do souboru se záznamy
        if os.path.exists(path) and os.path.getsize(path) < 65000:  # Kontrola, že daný sobor existuje a je menší než 65kB
            with open(path, 'rb') as f:     # Načtení dat souboru do proměnné
                file = f.read()
                message = "DownloadFile<EoR>" + file.decode() + "<EoR>"
                return message

    # Provedení požadavku na smazání souboru z uložiště
    if function == "DeleteFile":
        path = f"{user}/{filename}"     # Určení souboru a adresáře
        if os.path.exists(path):        # Zjištění, zda soubor existuje
            logs(function, user, filename)  # Zápis o požadavku do souboru se zápisy
            os.remove(path)     # Smazání daného souboru
        return "Deleted<EoR>"

    # Ověření nepozměněného souboru se záznamy
    if function == "VerifyLogs":
        message = verifyingLogs()
        return message


# Metoda na získání výpisu obsahu uložiště
def getStorage(start_path):
    result = {}

    for root, dirs, files in os.walk(start_path):
        if root == start_path:
            # add top-level directory to the result dictionary
            result[os.path.basename(root)] = set(dirs + files)
        else:
            # get the parent directory name
            parent = os.path.basename(os.path.dirname(root))
            # add subdirectory to its parent node in the result dictionary
            if parent in result:
                result[parent].add(os.path.basename(root))
            else:
                result[parent] = set()
                result[parent].add(os.path.basename(root))
            # add files to the subdirectory node in the result dictionary
            result[os.path.basename(root)] = set(files)
    result[f"{start_path}"] = list(result[f"{start_path}"])
    return result

# Dešifrování dat
def decrypt_data(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(data)
    return plaintext.rstrip(b'\0')

# Šifrování dat
def encrypt_data(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(data)
    return ciphertext


# Metoda pro zápis záznamu (logu) do souboru
def logs(function, user, filename):
    func = function
    username = user
    fname = filename
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # Definice, jaký bude mít jednotlivý záznam formát (datum;čas;uživatel;akce;název souboru;veliksot souboru)
    formatter = logging.Formatter('%(asctime)s;%(username)s;%(func)s;%(fname)s;%(filesize)s',
                                  datefmt='%Y-%m-%d;%H:%M:%S')
    file_handler = logging.FileHandler('Admin/Logs.txt')        # Cesta k souboru s logy
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    path = f"{username}/{fname}"
    filesize = str(os.path.getsize(path)) + 'B'
    logger.info('', extra={'username': username, 'func': func, 'fname': fname, 'filesize': filesize})
    # Zápis do souboru a odstranění duplicitních řádků
    with open('Admin/Logs.txt', 'r') as file:
        lines = file.readlines()
    unique_lines = list(set(lines))
    with open('Admin/Logs.txt', 'w') as file:
        for line in unique_lines:
            file.write(line)
    # Seřazení záznamů od nejnovějších po nejstarší
    datetime_regex = re.compile(r'^(\d{4}-\d{2}-\d{2});(\d{2}:\d{2}:\d{2})')
    with open('Admin/Logs.txt', 'r') as file:
        lines = file.readlines()
        sorted_lines = sorted(lines, key=lambda x: tuple(datetime_regex.search(x).groups()))
    reversed_lines = list(reversed(sorted_lines))
    with open('Admin/Logs.txt', 'w') as file:
        file.writelines(reversed_lines)
    # vytvoření nového otisku souboru se záznamy
    hashLogs()


# Metoda pro vytvoření hashe souboru se záznamy a uložení do souboru s otiskem
def hashLogs():
    with open('Admin/Logs.txt', 'rb') as file:
        file_hash = hashlib.sha256(file.read()).hexdigest()
    with open('Admin/hash_logs.txt', 'w') as hash_file:
        hash_file.write(file_hash)


# Metoda, která kontroluje zda nebyl soubor se záznamy pozměněn na základě situace, zda se shoduje otisk souboru s
# otiskem uloženým v souboru
def verifyingLogs():
    with open('Admin/Logs.txt', 'rb') as file:
        file_hash = hashlib.sha256(file.read()).hexdigest()     # Vytvoření hashe (SHA-256) a převedí na hexadecimální tvar
    with open('Admin/hash_logs.txt', 'r') as hash_file:
        saved_hash = hash_file.read().strip()
    # Vrácení hodnota na základě toho, zda se hashe shodují či nikoli
    if file_hash == saved_hash:
        return "Same<EoR>"
    else:
        return "Different<EoR>"


# Metoda, která ověřuje zda se poslaná kombinace uživatelského jména a hashe hesla shoduje s tím,
# které má uložiště uložené ve svém souboru
def verifyAccess(user, password):
    with open("users.json", "r") as credentialsfile: # načtení souboru do proměnné
        loaded_users = json.load(credentialsfile)

    # Kontrola zda se kombinace v daném tvaru nachází v souboru. Na základě shody se vrací hodnota
    if user in loaded_users and loaded_users[user] == password:
        return "Authenticated<EoR>"
    else:
        return "Non-authenticated<EoR>"

# Metoda, ve které je definováno naslouchání uložiště
def listen():
    global should_stop
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', source_port))
    ciphertext = b''
    while not should_stop:
        while True:
            recieved_data = sock.recv(65507) # Příjem přenesených dat

            if b'<UNCRYPTED>' in recieved_data:
                recieved_data = recieved_data.removeprefix(b'<UNCRYPTED>')    # Odstranění prefixu ze zprávy
                if b'<END>' in recieved_data:
                    recieved_data = recieved_data.removesuffix(b'<END>')    # Odstranění suffixu ze zprávy (Značí konec směrodatných inf.)
                ciphertext += recieved_data
                recieved_data_decoded = ciphertext.decode()       # Převedení přijaté zpravy
                # Rozdělení přijatých dat, na jednotlivé proměnné (jenž jsou rozděleny značkou
                # <EoR> značící "End of region")
                function = recieved_data_decoded.split('<EoR>')[0]
                user = recieved_data_decoded.split('<EoR>')[1]
                data = recieved_data_decoded.split('<EoR>')[2]
                filename = recieved_data_decoded.split('<EoR>')[3]
                # Pokud se bude jednat o příkaz zavření socketu (ukončení spojení), spojení se zavře
                # a změní se globální proměnná should_stop, což bude mít za následek, že uložiště následně přestane
                # naslouchat a vypne se
                if function == "CloseConnection":
                    sock.close()
                    should_stop = True
                    break
                else: # Pokud nešlo o ukončení spojení, provede se následující
                    message = gotResponse(function, user, data, filename)
                    # Odeslání nezašifrované zprávy uživateli na dané ip adrese a portu
                    sock.sendto(b'<UNCRYPTED>' + message.encode(), (ip_address, source_port))
                    ciphertext = b''
                    break

            else:
                if b'<END>' in recieved_data:
                    recieved_data = recieved_data.removesuffix(b"<END>")        # Odstranění suffixu zprávy
                ciphertext += recieved_data
                decrypt_message = decrypt_data(ciphertext, keyAES, ivAES)       # Dešifrování přijaté zprávy
                decrypted_message = decrypt_message.decode()       # Převedení přijaté zpravy
                # Rozdělení přijatých dat, na jednotlivé proměnné (jenž jsou rozděleny značkou
                # <EoR> značící "End of region")
                function = decrypted_message.split('<EoR>')[0]
                user = decrypted_message.split('<EoR>')[1]
                data = decrypted_message.split('<EoR>')[2]
                filename = decrypted_message.split('<EoR>')[3]
                if not filename:
                    filename = ""
                # Odeslání zašifrované, paddované, zprávy uživateli na dané ip adrese a portu
                sock.sendto(
                    encrypt_data(pad(gotResponse(function, user, data, filename).encode() + b'<END>', 16), keyAES, ivAES),
                    (ip_address, source_port))
                ciphertext = b''


listener = threading.Thread(target=listen, daemon=True)
listener.start()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', destination_port))

# Dokud není proměnná should_stop True, uložiště bude stále spuštěné
while True:
    if should_stop:
        break