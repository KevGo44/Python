# Python CheatSheet

---

## Inhaltsverzeichnis
1. [Grundsyntax](#1-grundsyntax)
2. [Datenstrukturen](#2-datenstrukturen)
3. [Kontrollfluss & Schleifen](#3-kontrollfluss--schleifen)
4. [Funktionen](#4-funktionen)
5. [Algorithmen](#5-algorithmen)
6. [Klassen (OOP)](#6-klassen-oop)
7. [String-Manipulation](#7-string-manipulation)
8. [Datei-I/O](#8-datei-io)
9. [Fehlerbehandlung](#9-fehlerbehandlung)
10. [Standard-Bibliothek](#10-standard-bibliothek)
11. [Netzwerk (socket / FerNet-Pattern)](#11-netzwerk-socket--fernet-pattern)
12. [Kryptoanalyse-Techniken](#12-kryptoanalyse-techniken)
13. [Web: requests & BeautifulSoup](#13-web-requests--beautifulsoup)
14. [Wichtige Idiome & Muster](#14-wichtige-idiome--muster)

---

## 1. Grundsyntax

```python
# Variablen (keine Typangabe nötig)
x = 42
name = "Alice"
pi = 3.14
flag = True

# Mehrfachzuweisung
a, b, c = 1, 2, 3
a, b = b, a          # Tauschen

# Typ prüfen
type(x)              # <class 'int'>
isinstance(x, int)   # True

# Konvertierung
int("42")   str(42)   float("3.14")   list("abc")  # ['a','b','c']

# Ausgabe
print(f"Name: {name}, Wert: {x:.2f}")   # f-String
print(f"{x:3d}: {name}")                # Formatiert: Breite 3, linksbündig Zahl
```

---

## 2. Datenstrukturen

### Liste (mutable, geordnet)
```python
lst = [1, 2, 3, 4, 5]
lst.append(6)           # Anhängen
lst.insert(0, 0)        # An Index einfügen
lst.pop()               # Letztes entfernen
lst.pop(0)              # Index 0 entfernen
lst.remove(3)           # Ersten Treffer entfernen
lst[1:3]                # Slice [2, 3]
lst[::-1]               # Umkehren
lst.sort()              # In-place sortieren
sorted(lst)             # Neue sortierte Liste
len(lst)
```

### Dictionary (mutable, ungeordnet ab 3.7 geordnet)
```python
d = {"a": 1, "b": 2}
d["c"] = 3              # Hinzufügen / Überschreiben
d.get("x", 0)           # Sicherer Zugriff, Default 0
d.keys()   d.values()   d.items()
del d["a"]
"b" in d                # True

# Häufigkeiten zählen (klassisches Muster)
freq = {}
for item in collection:
    freq[item] = freq.get(item, 0) + 1
```

### Tuple (immutable)
```python
t = (1, 2, 3)
a, b, c = t             # Unpacking
t[0]                    # Zugriff
```

### Set
```python
s = {1, 2, 3}
s.add(4)
s.discard(2)            # Kein Fehler wenn nicht vorhanden
s1 & s2   s1 | s2   s1 - s2   # Schnittmenge, Vereinigung, Differenz
s1.union(s2)   s1.intersection(s2)   s1.difference(s2)
```

### Stack & Queue
```python
from collections import deque

# Stack (LIFO) — mit Liste
stack = []
stack.append("a")   # push
stack.pop()         # pop (vom Ende)

# Queue (FIFO) — deque ist effizienter als liste.pop(0)
queue = deque()
queue.append("Erstes")
queue.append("Zweites")
queue.popleft()     # 'Erstes'  (O(1) statt O(n) bei list.pop(0))
```

---

## 3. Kontrollfluss & Schleifen

```python
# if / elif / else
if x > 10:
    pass
elif x == 10:
    pass
else:
    pass

# Ternary
result = "ja" if x > 0 else "nein"

# for-Schleifen
for i in range(10):          # 0..9
    pass
for i in range(2, 10, 2):    # 2,4,6,8
    pass
for i, val in enumerate(lst):              # Index + Wert (Start 0)
    pass
for pos, val in enumerate(lst, start=1):  # Start bei 1
    pass
for i, (k, v) in enumerate(d.items(), start=1):
    pass
for k, v in d.items():
    pass

# while
while condition:
    break       # Schleife abbrechen
    continue    # Nächste Iteration

# List Comprehension
squares   = [x**2 for x in range(10)]
filtered  = [x for x in lst if x > 0]
flat      = [item for sub in matrix for item in sub]

# Dict Comprehension
inverted  = {v: k for k, v in d.items()}
rel_freq  = {k: v / total * 100 for k, v in freq.items()}
```

---

## 4. Funktionen

```python
def greet(name, greeting="Hallo"):
    return f"{greeting}, {name}!"

# *args und **kwargs
def func(*args, **kwargs):
    for a in args: ...
    for k, v in kwargs.items(): ...

# Lambda
square = lambda x: x ** 2
sorted_list = sorted(items, key=lambda item: item[1], reverse=True)

# Verschachtelte Funktion (Closure)
def outer(n):
    def inner(x):
        return x + n
    return inner

add5 = outer(5)
add5(3)   # 8
```

---

## 5. Algorithmen

### 5.1 Iteration vs. Rekursion — Fibonacci

```python
# Iterativ (effizienter, kein Stack-Overflow)
def fib_iter(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Rekursiv (elegant, aber O(2^n) ohne Memoization)
def fib_rek(n):
    if n <= 1:
        return n
    return fib_rek(n - 1) + fib_rek(n - 2)
```

### 5.2 Suchalgorithmen

```python
# Lineare Suche — O(n), unsortierte Liste
def linear_search(liste, ziel):
    for i in range(len(liste)):
        if liste[i] == ziel:
            return i
    return -1
# Randfälle: leere Liste -> -1 | mehrere Treffer -> erstes Vorkommen

# Binäre Suche — O(log n), NUR auf sortierter Liste
def binary_search(liste, ziel):
    links, rechts = 0, len(liste) - 1
    while links <= rechts:
        mid = (links + rechts) // 2
        if liste[mid] == ziel:
            return mid
        elif liste[mid] < ziel:
            links = mid + 1
        else:
            rechts = mid - 1
    return -1
# Randfälle: leere Liste -> links=0, rechts=-1 -> kein Schleifendurchlauf -> -1
# mehrere Treffer -> irgendein Vorkommen, nicht zwingend das erste
```

### 5.3 Sortieralgorithmen

```python
# Bubble Sort — O(n²) | einfach, langsam
# Vergleicht benachbarte Elemente, schiebt größtes ans Ende
def bubble_sort(liste):
    n = len(liste)
    for i in range(n):
        for j in range(0, n - i - 1):
            if liste[j] > liste[j + 1]:
                liste[j], liste[j + 1] = liste[j + 1], liste[j]

# Selection Sort — O(n²) | findet Minimum, tauscht an Position i
def selection_sort(liste):
    n = len(liste)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if liste[j] < liste[min_index]:
                min_index = j
        liste[i], liste[min_index] = liste[min_index], liste[i]

# Insertion Sort — O(n²) worst, schnell bei fast-sortierten Listen
# Baut sortierte Teilliste auf, schiebt neues Element an richtige Stelle
def insertion_sort(liste):
    for i in range(1, len(liste)):
        key = liste[i]
        j = i - 1
        while j >= 0 and liste[j] > key:
            liste[j + 1] = liste[j]
            j -= 1
        liste[j + 1] = key

# Mergesort — O(n log n) best/avg/worst | stabil
# Teilen -> rekursiv sortieren -> zusammenführen (3-Zeiger-Merge)
def mergesort(liste):
    if len(liste) > 1:
        mid = len(liste) // 2
        left  = liste[:mid]
        right = liste[mid:]
        mergesort(left)
        mergesort(right)
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                liste[k] = left[i];  i += 1
            else:
                liste[k] = right[j]; j += 1
            k += 1
        while i < len(left):
            liste[k] = left[i];  i += 1; k += 1
        while j < len(right):
            liste[k] = right[j]; j += 1; k += 1

# Quicksort — O(n log n) avg, O(n²) worst (extremes Pivot)
# Pivot wählen -> links/rechts aufteilen -> rekursiv -> zusammensetzen
def quicksort(liste):
    if len(liste) <= 1:
        return liste
    pivot = liste[0]
    left  = [x for x in liste[1:] if x <= pivot]
    right = [x for x in liste[1:] if x > pivot]
    return quicksort(left) + [pivot] + quicksort(right)
```

### Komplexitäts-Übersicht

| Algorithmus    | Best      | Average   | Worst     | Stabil |
|----------------|-----------|-----------|-----------|--------|
| Bubble Sort    | O(n)      | O(n²)     | O(n²)     | ja     |
| Selection Sort | O(n²)     | O(n²)     | O(n²)     | nein   |
| Insertion Sort | O(n)      | O(n²)     | O(n²)     | ja     |
| Mergesort      | O(n log n)| O(n log n)| O(n log n)| ja     |
| Quicksort      | O(n log n)| O(n log n)| O(n²)     | nein   |
| Linear Search  | O(1)      | O(n)      | O(n)      | —      |
| Binary Search  | O(1)      | O(log n)  | O(log n)  | —      |

---

## 6. Klassen (OOP)

```python
class MyClass:
    CLASS_VAR = "shared"       # Klassenvariable

    def __init__(self, x, y):
        self.x = x             # Instanzvariable
        self.y = y

    def method(self):
        return self.x + self.y

    def __repr__(self):        # Debug-Darstellung
        return f"MyClass({self.x}, {self.y})"

    def __str__(self):         # print()-Darstellung
        return f"({self.x}, {self.y})"

class Child(MyClass):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z

    def method(self):          # Override
        return super().method() + self.z

obj = MyClass(1, 2)
```

### Typisches Klassen-Pattern (wie FerNet)
```python
class Tool:
    def __init__(self, args):
        self.args = args
        # Ressourcen initialisieren (Socket, Datei, ...)

    def run(self):
        if self.args.mode_a:
            self.mode_a()
        else:
            self.mode_b()

    def mode_a(self): ...
    def mode_b(self): ...

if __name__ == "__main__":
    args = parse_args()
    t = Tool(args)
    t.run()
```

---

## 7. String-Manipulation

```python
s = "Hello World"
s.upper()   s.lower()   s.title()
s.strip()   s.lstrip()  s.rstrip()     # Whitespace entfernen
s.split()                              # ["Hello", "World"]
s.split(",")                           # An Komma trennen
",".join(["a","b","c"])                # "a,b,c"
s.replace("Hello", "Hi")
s.startswith("He")   s.endswith("ld")
s.find("World")                        # Index oder -1
s.count("l")
len(s)
s[1:5]                                 # Slice
s[::-1]                                # Umkehren

# f-Strings (Formatierung)
f"{val:.2f}"       # 2 Dezimalstellen
f"{val:>10}"       # Rechtsbündig, Breite 10
f"{val:03d}"       # Mit führenden Nullen
f"{i:3d}: {item}"  # Spalten-Format

# bytes <-> str
"text".encode("utf-8")          # -> bytes
b"bytes".decode("utf-8")        # -> str
b"bytes".decode(errors="replace")  # Fehler tolerant
```

---

## 8. Datei-I/O

```python
# Lesen
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()        # Alles auf einmal
    lines   = f.readlines()   # Liste von Zeilen

# Zeilenweise (Speicherschonend)
with open("file.txt") as f:
    for line in f:
        print(line.strip())

# Schreiben
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("Zeile 1\n")

# Binär (z.B. Dateiübertragung)
with open("file.bin", "rb") as f:
    data = f.read()

with open("out.bin", "wb") as f:
    f.write(data)
```

---

## 9. Fehlerbehandlung

```python
try:
    result = int("abc")
except ValueError as e:
    print(f"Fehler: {e}")
except (TypeError, KeyError):
    pass
except Exception as e:
    print(f"Unbekannter Fehler: {e}")
else:
    print("Kein Fehler")      # Wird nur ausgeführt wenn kein Fehler
finally:
    print("Immer ausgeführt") # Cleanup, Datei schließen etc.

# Eigene Exception
class MyError(Exception):
    pass

raise MyError("Etwas ist schiefgelaufen")
```

---

## 10. Standard-Bibliothek

### argparse — Kommandozeilen-Argumente
```python
import argparse, textwrap

parser = argparse.ArgumentParser(
    description="Mein Tool",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent('''
        Beispiele:
          python tool.py -t 127.0.0.1 -p 4444 -l
    ''')
)

parser.add_argument('-t', '--target', default='0.0.0.0', help='Ziel-IP')
parser.add_argument('-p', '--port',   type=int, default=4554)
parser.add_argument('-l', '--listen', action='store_true')   # Flag (True/False)
parser.add_argument('-e', '--execute', help='Befehl ausführen')

args = parser.parse_args()
# args.target  args.port  args.listen  args.execute
```

### subprocess — Shell-Befehle ausführen
```python
import subprocess, shlex

# Befehl ausführen und Output zurückbekommen
output = subprocess.check_output(
    shlex.split("ls -la"),      # String -> Liste: "ls -la" -> ["ls", "-la"]
    stderr=subprocess.STDOUT    # Fehler in stdout umleiten
)
text = output.decode(errors="replace")

# Mit shell=True (Windows-Fallback)
output = subprocess.check_output("cmd /c dir", shell=True, stderr=subprocess.STDOUT)

# CalledProcessError abfangen (exit code != 0)
try:
    out = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as e:
    out = e.output              # Fehlermeldung trotzdem verfügbar
except FileNotFoundError:
    pass                        # Befehl nicht gefunden
```

### threading — Multithreading
```python
import threading

def worker(arg):
    print(f"Thread arbeitet: {arg}")

t = threading.Thread(
    target=worker,
    args=(my_arg,)   # Komma! -> Tuple mit 1 Element
)
t.start()
t.join()             # Warten bis Thread fertig

# Lock für geteilte Ressourcen
lock = threading.Lock()
with lock:
    shared_variable += 1
```

### re — Reguläre Ausdrücke
```python
import re

re.findall(r"\w+", text)        # Alle Wörter
re.findall(r"\d+", text)        # Alle Zahlen
re.search(r"pattern", text)     # Erstes Match (oder None)
re.match(r"^start", text)       # Nur Anfang
re.sub(r"\s+", " ", text)       # Ersetzen

# Wichtige Muster
# \w  Buchstaben, Ziffern, _
# \d  Ziffern
# \s  Whitespace
# .   Beliebiges Zeichen (außer \n)
# +   Ein oder mehr
# *   Null oder mehr
# ?   Optional
# ^   Anfang  $  Ende
```

### operator & sorted
```python
import operator

# Nach zweitem Element sortieren (z.B. Dict-Items nach Wert)
sorted_items = sorted(d.items(), key=operator.itemgetter(1), reverse=True)

# Äquivalent mit lambda
sorted_items = sorted(d.items(), key=lambda x: x[1], reverse=True)
```

---

## 11. Netzwerk (socket / FerNet-Pattern)

### TCP Client
```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 4554))
client.send(b"Hallo\n")
response = client.recv(4096)     # Blockiert bis Daten kommen
print(response.decode())
client.close()
```

### TCP Server (mit Threading)
```python
import socket, threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Port sofort wiederverwendbar
server.bind(("0.0.0.0", 4554))
server.listen()

while True:
    client_sock, addr = server.accept()     # Blockiert -> (socket, (ip, port))
    t = threading.Thread(target=handle, args=(client_sock,))
    t.start()

def handle(sock):
    data = sock.recv(1024)
    sock.send(b"ACK")
    sock.close()
```

### UDP Client
```python
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # DGRAM statt STREAM
client.sendto(b"Nachricht", ("127.0.0.1", 4554))             # sendto statt send
response, addr = client.recvfrom(4096)                        # recvfrom statt recv
```

### Socket-Konstanten Übersicht
| Konstante | Bedeutung |
|---|---|
| `AF_INET` | IPv4 |
| `AF_INET6` | IPv6 |
| `SOCK_STREAM` | TCP |
| `SOCK_DGRAM` | UDP |
| `SO_REUSEADDR` | Port sofort wieder nutzbar nach Neustart |

### Daten senden/empfangen (Streams)
```python
# Problem: TCP ist ein Stream, kein Nachrichten-Protokoll.
# recv() gibt evtl. nur einen Teil zurück.

# Muster 1: Bis Newline warten
buffer = b""
while b"\n" not in buffer:
    buffer += sock.recv(64)
cmd = buffer.decode()

# Muster 2: Timeout für "Ende erkennen" (Reverse Shell Pattern)
sock.settimeout(1.0)
response = b""
try:
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
except TimeoutError:
    pass
sock.settimeout(None)   # Zurück zu Blocking

# Muster 3: Bekannte Länge (recv genau n Bytes)
def recv_exact(sock, n):
    data = b""
    while len(data) < n:
        data += sock.recv(n - len(data))
    return data
```

### Bind-Shell vs. Reverse-Shell
```
Bind-Shell:    Ziel (Bob) stellt Shell bereit  -l -c
               Angreifer (Alice) verbindet sich

Reverse-Shell: Ziel (Client) verbindet sich aktiv zum Angreifer
               Angreifer (Server) tippt Befehle  -l -r
```

---

## 12. Kryptoanalyse-Techniken

### Caesar-Verschlüsselung
```python
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def caesar(text, key):
    result = ""
    for c in text.upper():
        if c in ALPHABET:
            result += ALPHABET[(ALPHABET.index(c) + key) % 26]
        else:
            result += c
    return result

def de_caesar(text, key):
    return caesar(text, 26 - key)

def brute_force(text):
    for i in range(26):
        print(f"{i:2d}: {de_caesar(text, i)}")
```

### Vigenère-Verschlüsselung (polyalphabetisch)
```python
def vigenere(text, password):
    text, password = text.upper(), password.upper()
    result, key_i = "", 0
    for c in text:
        if c in ALPHABET:
            shift = ALPHABET.index(password[key_i % len(password)])
            result += caesar(c, shift)
            key_i += 1      # Schlüssel nur bei Buchstaben vorrücken
        else:
            result += c
    return result
```

### Häufigkeitsanalyse
```python
import operator

def freq(text):
    h = {}
    for c in text:
        h[c] = h.get(c, 0) + 1
    total = len(text)
    return {k: v / total * 100 for k, v in h.items()}

# Top-n sortiert ausgeben
sorted_freq = sorted(freq(text).items(), key=operator.itemgetter(1), reverse=True)
for rank, (char, pct) in enumerate(sorted_freq[:10]):
    print(f"{rank:3d}: {char}  {pct:.2f}%")
```

### n-Gramme (Bi-/Trigramme)
```python
def ngram(text, n):
    """Relative Häufigkeiten aller überlappenden n-Gramme."""
    ngrams = {}
    total = 0
    for delta in range(n):              # Versatz 0..n-1
        for i in range(0, len(text), n):
            teil = text[delta + i : delta + i + n]
            if len(teil) == n:
                total += 1
                ngrams[teil] = ngrams.get(teil, 0) + 1
    return {k: v / total * 100 for k, v in ngrams.items()} if total else {}

# Bigramme  = ngram(text, 2)
# Trigramme = ngram(text, 3)
```

### Koinzidenzindex (IC) — Sprachidentifikation
```python
def koinzidenz(text):
    """IC ~ 0.0385 Zufall | ~ 0.0667 Englisch | ~ 0.0762 Deutsch"""
    n = len(text)
    if n < 2: return 0.0
    h = {}
    for c in text:
        h[c] = h.get(c, 0) + 1
    zaehler = sum(ni * (ni - 1) for ni in h.values())
    return zaehler / (n * (n - 1))
```

### Referenz-Häufigkeiten
```
Deutsch (IC~0.076): E:16.93  N:10.53  I:8.02  R:6.89  S:6.42
Englisch (IC~0.067): E:11.0  T:9.1   A:7.8   O:7.4   I:6.9

Bigramme DE: ER  EN  CH  DE  EI  TE
Bigramme EN: TH  HE  IN  ER  AN  RE

Trigramme DE: DER  EIN  SCH  ICH  NDE
Trigramme EN: THE  AND  ING  HER  HAT
```

### Analyse-Workflow (monoalphabetische Substitution)
```
1. IC berechnen -> monoalphabetisch (>0.06) oder polyalphabetisch (<0.045)?
2. Häufigkeitsanalyse -> häufigsten Buchstaben = E/N/I/R in Deutsch
3. Bigramme/Trigramme -> Muster erkennen (ER, EIN, DER...)
4. Kurze Wörter: 2-buchst.=IN/AN, 4-buchst.=EINE/KEIN
5. Schrittweise substituieren (multirep): add A,E -> ersetzen -> text
   Hinweis: alle Paare erst definieren, dann einmal 'ersetzen' anwenden
```

---

## 13. Web: requests & BeautifulSoup

```python
import requests
from bs4 import BeautifulSoup
import re

# HTTP GET
resp = requests.get("https://example.com")
resp.status_code   # 200 = OK
resp.text          # HTML als String
resp.json()        # JSON-Response parsen

# POST mit Daten
resp = requests.post(url, data={"key": "value"})
resp = requests.post(url, json={"key": "value"})  # JSON-Body

# Header setzen
resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

# HTML -> Reintext
soup = BeautifulSoup(resp.text, "html.parser")
text = soup.get_text()

# Elemente suchen
links  = soup.find_all("a")
title  = soup.find("title").text
divs   = soup.find_all("div", class_="content")

# Wörter aus Text extrahieren
words = re.findall(r"\w+", text)

# Wörterhäufigkeit
freq = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1
top5 = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
```

---

## 14. Wichtige Idiome & Muster

### `if __name__ == "__main__":`
```python
# Code wird nur ausgeführt wenn Skript direkt gestartet wird,
# NICHT wenn es als Modul importiert wird.
if __name__ == "__main__":
    main()
```

### Context Manager (`with`)
```python
with open("file.txt") as f:    # Datei wird automatisch geschlossen
    data = f.read()

with socket.socket(...) as s:  # Socket wird geschlossen auch bei Exception
    s.connect(...)
```

### Sortieren nach Wert
```python
# Dict nach Wert sortiert (absteigend)
top = sorted(d.items(), key=lambda x: x[1], reverse=True)[:10]

# Objekte nach Attribut sortieren
sorted(objects, key=lambda o: o.score)
```

### `enumerate` & `zip`
```python
for i, val in enumerate(lst):        # Index + Wert
    print(f"{i}: {val}")

for a, b in zip(list1, list2):       # Zwei Listen parallel
    pass
```

### Bytes & Encoding
```python
# str -> bytes
data = "text".encode("utf-8")
data = cmd + "\n"
sock.send(data.encode("utf-8"))

# bytes -> str
text = data.decode("utf-8")
text = data.decode(errors="replace")  # Unbekannte Bytes -> '?'
```

### Dict-Tricks
```python
d.get(key, default)         # Sicherer Zugriff
d.setdefault(key, [])       # Key anlegen falls nicht vorhanden
{**d1, **d2}                # Dicts zusammenführen (Python 3.9+: d1 | d2)
d = {v: k for k, v in d.items()}  # Invertieren
```

### String-Formatierung auf einen Blick
```python
f"{n:2d}"      # Ganzzahl, Breite 2
f"{f:.2f}"     # Float, 2 Nachkommastellen
f"{s:<20}"     # Linksbündig, Breite 20
f"{s:>20}"     # Rechtsbündig
f"{n:03d}"     # Mit führenden Nullen (003)
```

### Typische Zähl-Pipeline
```python
text = "..."
words = re.findall(r"\w+", text.lower())
freq = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1
top = sorted(freq.items(), key=lambda x: x[1], reverse=True)
for word, count in top[:10]:
    print(f"{word:<20} {count}")
```

---

## Schnellreferenz: Häufige Module

| Modul | Import | Zweck |
|---|---|---|
| `argparse` | `import argparse` | CLI-Argumente parsen |
| `socket` | `import socket` | TCP/UDP Netzwerk |
| `threading` | `import threading` | Nebenläufigkeit |
| `subprocess` | `import subprocess` | Shell-Befehle ausführen |
| `shlex` | `import shlex` | Command-String -> Liste |
| `re` | `import re` | Reguläre Ausdrücke |
| `operator` | `import operator` | `itemgetter` für Sortierung |
| `textwrap` | `import textwrap` | `dedent()` für Multiline-Strings |
| `sys` | `import sys` | `sys.exit()`, `sys.argv` |
| `os` | `import os` | Pfade, Umgebungsvariablen |
| `requests` | `import requests` | HTTP-Requests |
| `bs4` | `from bs4 import BeautifulSoup` | HTML-Parsing |
