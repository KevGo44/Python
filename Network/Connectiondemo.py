# =============================================================================
# imports
# =============================================================================
import argparse
import shlex
import socket
import subprocess
import sys
import textwrap
import threading

# =============================================================================
# Socket: Netzwerk-Kommunikation 
# (IP-Adresse, Port) <-> Socket
# Socket: Endpunkt für die Kommunikation

# Server
#server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.bind(('localhost', 8080))
#server.listen(1)
# (client_socket, client_address) = server.accept()
#client_sock, addr = server.accept()  # <- Neuer Socket für Client

# Client  
#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(('localhost', 8080))   # <- Verbindung zum Socket
# =============================================================================

# =============================================================================
# 1. TCP CLIENT
# =============================================================================

def tcp_client_demo():
    """
    Minimaler TCP Client: Verbindet sich, sendet einen HTTP-Request,
    empfängt die Antwort und gibt sie aus.
    """
    target_host = "localhost" # 127.0.0.1
    target_port = 4554

    # create a socket object
    # socket.AF_INET        = IPv4
    # socket.SOCK_STREAM    = TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect the client
    # connect() erwartet TUPLE: (host, port)
    # TCP: Verbindung aufbauen (3-Way-Handshake)
    client.connect((target_host, target_port))

    # send some data
    # HTTP-Request: GET / HTTP/1.1\r\nHost: google.com\r\n\r\n 
    # \r\n\r\n = leere Zeile; Ende des HTTP-Headers
    client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

    # receive some data
    response = client.recv(4096)
    # recv() blockiert bis Daten empfangen wurden oder Verbindung geschlossen wurde
    # response ist ein bytes-Objekt; muss dekodiert werden
    # uft-8: 8-Bit Unicode Transformation Format, Standard für Textkodierung
    print(response.decode("uft-8"))
    client.close() # Verbindung schließen

# =============================================================================
# 2. UDP CLIENT    
# =============================================================================
# Unterschiede zu TCP:
#   - SOCK_DGRAM statt SOCK_STREAM
#   - sendto() statt send() (weil keine Verbindung besteht)
#   - recvfrom() statt recv() (gibt auch Absender-Adresse zurück)
#   - Kein connect() nötig (UDP ist "verbindungslos")
#
# Typische UDP-Protokolle: DNS (Port 53), DHCP, SNMP, Syslog

def udp_client_demo():
    """
    Minimaler UDP Client: Verbindet sich, sendet eine Nachricht und empfängt die Antwort.
    """
    target_host = "localhost" # 127.0.0.1
    target_port = 4554

    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # send some dat
    message = b"Hello, UDP Server!" # Nachricht als bytes-Objekt
    client.sendto(message, (target_host, target_port)) # Nachricht senden

    # receive some data
    response, server_address = client.recvfrom(4096) # Antwort empfangen
    # server_address ist ein Tuple: (IP-Adresse, Port)
    # Alternativ: response, client_ip, client_port = client.recvfrom(4096)
    # Zugriff auf Tupel: server_address[0] = IP-Adresse, server_address[1] = Port
    print(f"Received from {server_address}: {response.decode()}")

    client.close() # Socket schließen

# =============================================================================    
# 3. TCP SERVER
# =============================================================================
# Ablauf eines TCP-Servers:
#   1. socket()  -> Socket erstellen
#   2. bind()    -> An IP + Port binden ("hier höre ich zu")
#   3. listen()  -> Bereit für eingehende Verbindungen
#   4. accept()  -> Auf Verbindung warten (blockiert!)
#   5. recv/send -> Daten austauschen
#
# Threading: Jeder Client bekommt seinen eigenen Thread,
# damit der Server nicht blockiert und weitere Clients annehmen kann.

def tcp_server_demo():
    """
    Minimaler TCP Server: Wartet auf Verbindungsanfragen, empfängt Daten und antwortet mit 'ACK'.
    """
    ip = '0.0.0.0' # Alle verfügbaren Netzwerkschnittstellen
    port = 4554     # Port, auf dem der Server horcht

    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to the IP and port
    # bind() verknüpft socket mit ip und port
    # Prozess wird auf diesem Port aufgesetzt
    server.bind((ip, port))
    print(f'[*] Server running on {ip}:{port}')

    # listen for incoming connections
    server.listen()  # Erstellt Warteschlange für Verbindungen im Betriebsystem-Kernel
    print(f'[*] Server listening on {ip}:{port}')

    while True:
        # accept() blockiert, bis ein Client sich verbindet
        # Gibt zurück: (neuer_socket_für_diesen_client, (client_ip, client_port))
        client_socket, addr = server.accept()
        print(f'[*] Received connection from {addr[0]}:{addr[1]}')

        # Startet einen neuen Thread, um den Client zu bedienen
        client_handler = threading.Thread(
            target = handle_client, # Funktion, die im Thread ausgeführt wird target=function
            args = (client_socket,) # Argumente für die Funktion args=(arg1, arg2, ...
        )
        # Thread starten
        # Lebenszyklus: Thread erstellen -> .start() -> prozess -> Funktion (target) endet -> Thread endet "dead"
        client_handler.start()

def handle_client(client_socket):
    """
    Funktion, die in einem Thread für jeden Client ausgeführt wird.
    Empfängt Daten und antwortet mit 'ACK'.
    """
    with client_socket as sock: # 'with' schließt den Socket automatisch
        request = sock.recv(1024)
        print(f"[*] Received: {request.decode("uft-8")}")
        sock.send(b"ACK") # Antwort senden