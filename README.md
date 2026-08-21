# Python

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Dependencies](https://img.shields.io/badge/dependencies-stdlib_only-green)

## Inhalt

- [Python](#python)
  - [Inhalt](#inhalt)
  - [Repository-Struktur](#repository-struktur)
  - [Projekte](#projekte)
    - [Crypto — Kryptoanalyse V2](#crypto--kryptoanalyse-v2)
    - [Games — PentagonQuest](#games--pentagonquest)
    - [Games — TicTacToe](#games--tictactoe)
    - [Network — FerNet](#network--fernet)
    - [Network — ConnectionDemo](#network--connectiondemo)
  - [Python CheatSheet](#python-cheatsheet)
  - [Voraussetzungen](#voraussetzungen)

---

## Repository-Struktur

```
.
├── Crypto/
│   └── KryptoanalyseV2.py      Analyse & Entschlüsselung klassischer Chiffren
├── Games/
│   ├── PentagonQuest.py        Textbasiertes RPG (Konsole)
│   ├── PentagonQuest_GUI.py    Dasselbe Spiel mit grafischer Oberfläche
│   └── TicTacToe.py            Tic-Tac-Toe
├── Network/
│   ├── FerNet.py               Netcat-Nachbau (Client/Server, Socket + Threading)
│   └── ConnectionDemo.py       Minimalbeispiel Client/Server-Socket
├── python_cheatsheet.md        Nachschlagewerk: Syntax, Algorithmen, Module
└── README.md
```

---

## Projekte

### Crypto — Kryptoanalyse V2

Interaktives Werkzeug zur Analyse und Entschlüsselung klassischer Chiffren.
Kombiniert Verschlüsselung, statistische Analyse und manuelle Substitution,
sodass sich ein unbekannter Geheimtext schrittweise knacken lässt.

**Funktionsumfang**

| Bereich | Funktionen |
|---|---|
| Verschlüsselung | Cäsar (inkl. Brute-Force über alle 26 Schlüssel), Vigenère |
| Analyse | absolute & relative Buchstabenhäufigkeiten, n-Gramme (Bi-/Trigramme), Koinzidenzindex zur Sprachbestimmung |
| Substitution | Mehrfachersetzung über ein interaktives Menü |
| Referenz | Vergleichswerte für Englisch und Deutsch |

**Start**

```bash
python Crypto/KryptoanalyseV2.py
```

**Befehle im Hauptmenü**

| Befehl | Wirkung |
|---|---|
| `neu` | Neue Chiffre eingeben |
| `chiffre` | Aktuelle Chiffre anzeigen |
| `analyse [n]` | Häufigkeitsanalyse, optional nur Top-n-Einträge |
| `sprache` | Koinzidenzindex berechnen |
| `info` | Referenztabellen Englisch/Deutsch |
| `multirep` | Substitutionsmenü öffnen |
| `caesar` | Cäsar-Brute-Force (alle 26 Schlüssel) |
| `help` / `exit` | Hilfe anzeigen / beenden |

**Typischer Ablauf:** `neu` → `sprache` (Deutsch oder Englisch?) → `analyse`
(auffällige Häufigkeiten suchen) → `multirep` (Buchstaben ersetzen und Ergebnis
prüfen). Bei Verdacht auf eine reine Verschiebechiffre reicht `caesar`.

---

### Games — PentagonQuest

Textbasiertes RPG auf einer 5×5-Karte. Ziel ist es, sich bis zum Feld (4,4)
durchzukämpfen und dort den **OrkKönig** zu besiegen. Der Schwerpunkt liegt auf
sauberer Objektorientierung: Vererbung, Mixins und Komposition.

**Klassenstruktur**

```
Item                 Basisklasse für aufsammelbare Gegenstände
 ├── Sword           Waffe mit Angriffswert (ad)
 └── HPPlus          Verbrauchsitem, erhöht HP dauerhaft

Character            Basisklasse für kampffähige Einheiten
 ├── Player          Spielerfigur mit Inventar und Ausrüstungsslot
 ├── MobWithDrop     Mixin: Gegner, die beim Tod Items droppen
 │    ├── Goblin      100 HP /10 AD
 │    ├── Ork         300 HP /30 AD
 │    └── Waechter    800 HP /15 AD
 └── OrkKoenig       Endboss, 4000 HP /60 AD, kein Drop

Field                Ein Kartenfeld mit Gegnern und Loot
Map                  5×5-Gitter aus Fields, verwaltet die Spielerposition
```

**Start**

```bash
python Games/PentagonQuest.py          # Konsolenversion
python Games/PentagonQuest_GUI.py      # grafische Oberfläche
```

**Spielbefehle**

| Befehl | Wirkung |
|---|---|
| `forward` / `backwards` / `left` / `right` | Bewegung auf der Karte |
| `fight` | Alle Gegner auf dem aktuellen Feld bekämpfen |
| `pickup N` / `drop N` | Item N aufheben / ablegen |
| `equip N` / `use N` | Item N ausrüsten / benutzen (z. B. HPPlus) |
| `inventar` / `stats` / `map` | Inventar, Spielerstatus, Feldstatus anzeigen |
| `rest` | HP vollständig regenerieren |
| `help` / `quit` | Befehlsübersicht / beenden |

---

### Games — TicTacToe

Klassisches Drei-Gewinnt für zwei Spieler auf einem 3×3-Feld, inklusive
Gewinn- und Unentschieden-Erkennung.

```bash
python Games/TicTacToe.py
```

---

### Network — FerNet

Eigener Netcat-Nachbau auf Basis von `socket` und `threading`: liest und
schreibt Daten über das Netzwerk und kann wahlweise als Client oder als
Listener laufen. Entstanden als Übung zu TCP-Streams, Thread-Handling und
`subprocess`.

**Aufbau**

| Methode | Aufgabe |
|---|---|
| `__init__()` | Socket erstellen, Argumente speichern |
| `run()` | Weiche: `listen()` (Server) oder `send()` (Client) |
| `send()` | Client-Modus: verbinden und senden |
| `listen()` | Server-Modus: auf Clients warten, pro Client ein Thread |
| `handle()` | Pro Verbindung: Command / Upload / Shell |
| `execute()` | Befehl ausführen und Ausgabe zurückgeben |

**Parameter**

| Flag | Bedeutung |
|---|---|
| `-t` | Ziel-IP |
| `-p` | Ziel-Port |
| `-l` | Listener-Modus (Server-Seite) |
| `-c` | Interaktive Command Shell |
| `-e` | Einzelnen Befehl ausführen |
| `-u` | Datei-Upload: empfängt Daten und schreibt sie in eine Datei |

**Beispiel (Bind-Shell, beide Seiten im eigenen Testnetz)**

```bash
# Zielhost stellt die Shell bereit
python Network/FerNet.py -t 10.0.0.5 -p 5555 -l -c

# Gegenstelle verbindet sich
python Network/FerNet.py -t 10.0.0.5 -p 5555
```

Die Gegenstelle erhält den Prompt `#> `, die eingetippten Befehle werden auf
dem Zielhost ausgeführt und die Ausgabe zurückgesendet.

---

### Network — ConnectionDemo

Reduziertes Lernbeispiel zum Einstieg: zeigt in wenigen Zeilen, wie ein Socket
als Endpunkt aus IP-Adresse und Port entsteht, wie `bind()` / `listen()` /
`accept()` auf Serverseite zusammenspielen und wie `connect()` auf Clientseite
die Verbindung herstellt. Der zentrale Punkt: `accept()` liefert einen **neuen**
Socket für den jeweiligen Client.

---

## Python CheatSheet

[`python_cheatsheet.md`](python_cheatsheet.md) ist das Nachschlagewerk zu den
Projekten: 16 Kapitel von der Grundsyntax über Datenstrukturen, Algorithmen mit
Komplexitätstabelle und OOP bis zu `socket`, `subprocess`, `re` und
Kryptoanalyse-Techniken. Jeder Codeblock ist zeilenweise kommentiert, zwei
Verzeichnisse (Kapitelübersicht + Detailverzeichnis) führen direkt zur richtigen
Stelle.

---

## Voraussetzungen

- **Python 3.10 oder neuer** (wegen der Schreibweise `int | None` bei Type Hints)
- Nur Standardbibliothek — keine Installation per `pip` nötig
- Für `PentagonQuest_GUI.py` zusätzlich `tkinter` (unter Debian/Ubuntu:
  `sudo apt install python3-tk`; unter Windows und macOS bereits enthalten)

```bash
git clone <repo-url>
cd <repo>
python Games/PentagonQuest.py
```

---