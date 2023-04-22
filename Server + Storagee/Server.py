import socket

# Nastavení portu, na kterých bude klient a uložiště komunikovat
known_port = 50002
known_port2 = 50003

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 55555))

while True:
    clients = []

    while True:
        data, address, = sock.recvfrom(128)
        clients.append(address)
        sock.sendto(b'ready', address)
        # Pokud se na server připojí dva klienti (klient a uložiště), odešle jim informace o druhé straně a spojí je
        if len(clients) == 2:
            break

    # Odeslání informací (ip_address adresa a port) klientům připojeným na server
    client_1 = clients.pop()
    client_1_address, client_1_port = client_1
    client_2 = clients.pop()
    client_2_address, client_2_port = client_2
    sock.sendto('{} {} {}'.format(client_1_address, client_1_port, known_port).encode(), client_2)
    sock.sendto('{} {} {}'.format(client_2_address, client_2_port, known_port).encode(), client_1)