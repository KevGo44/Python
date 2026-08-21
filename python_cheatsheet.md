# Python CheatSheet

> Nachschlagewerk mit kommentierten Beispielen.
> Zwei Verzeichnisse: **Übersicht** (nur Kapitel) zum groben Orientieren,
> **Detail** (alle Unterpunkte) zum direkten Anspringen.

---

## Übersicht

- [1. Grundsyntax](#1-grundsyntax)
- [2. Datenstrukturen](#2-datenstrukturen)
- [3. Kontrollfluss & Schleifen](#3-kontrollfluss--schleifen)
- [4. Funktionen](#4-funktionen)
- [5. Algorithmen](#5-algorithmen)
- [6. Generatoren & `yield`](#6-generatoren--yield)
- [7. Klassen (OOP)](#7-klassen-oop)
- [8. String-Manipulation](#8-string-manipulation)
- [9. Datei-I/O](#9-datei-io)
- [10. Fehlerbehandlung](#10-fehlerbehandlung)
- [11. Standard-Bibliothek](#11-standard-bibliothek)
- [12. Netzwerk (`socket`)](#12-netzwerk-socket)
- [13. Kryptoanalyse-Techniken](#13-kryptoanalyse-techniken)
- [14. Web: `requests` & `BeautifulSoup`](#14-web-requests--beautifulsoup)
- [15. Idiome & Muster](#15-idiome--muster)
- [16. Schnellreferenz: Häufige Module](#16-schnellreferenz-häufige-module)

---

## Inhaltsverzeichnis (Detail)

- [1. Grundsyntax](#1-grundsyntax)
    - [1.1 Variablen & Zuweisung](#11-variablen--zuweisung)
    - [1.2 Typen prüfen & konvertieren](#12-typen-prüfen--konvertieren)
    - [1.3 Ausgabe & f-Strings](#13-ausgabe--f-strings)
- [2. Datenstrukturen](#2-datenstrukturen)
    - [2.1 Liste — mutable, geordnet](#21-liste--mutable-geordnet)
    - [2.2 Dictionary — Schlüssel-Wert-Paare](#22-dictionary--schlüssel-wert-paare)
    - [2.3 Tuple — immutable](#23-tuple--immutable)
    - [2.4 Set — Menge ohne Duplikate](#24-set--menge-ohne-duplikate)
    - [2.5 Stack & Queue](#25-stack--queue)
- [3. Kontrollfluss & Schleifen](#3-kontrollfluss--schleifen)
    - [3.1 Bedingungen](#31-bedingungen)
    - [3.2 for-Schleifen](#32-for-schleifen)
    - [3.3 while-Schleifen](#33-while-schleifen)
    - [3.4 Comprehensions](#34-comprehensions)
- [4. Funktionen](#4-funktionen)
    - [4.1 Definition & Default-Parameter](#41-definition--default-parameter)
    - [4.2 `*args` und `**kwargs`](#42-args-und-kwargs)
    - [4.3 Lambda](#43-lambda)
    - [4.4 Closures — verschachtelte Funktionen](#44-closures--verschachtelte-funktionen)
    - [4.5 Type Hints & Annotationen](#45-type-hints--annotationen)
- [5. Algorithmen](#5-algorithmen)
    - [5.1 Iteration vs. Rekursion — Fibonacci](#51-iteration-vs-rekursion--fibonacci)
    - [5.2 Suchalgorithmen](#52-suchalgorithmen)
    - [5.3 Sortieralgorithmen](#53-sortieralgorithmen)
    - [5.4 Komplexitäts-Übersicht](#54-komplexitäts-übersicht)
- [6. Generatoren & `yield`](#6-generatoren--yield)
    - [6.1 Generator-Funktion](#61-generator-funktion)
    - [6.2 `yield from`](#62-yield-from)
    - [6.3 Typischer Einsatz](#63-typischer-einsatz)
- [7. Klassen (OOP)](#7-klassen-oop)
    - [7.1 Grundgerüst](#71-grundgerüst)
    - [7.2 Dunder-Methoden](#72-dunder-methoden)
    - [7.3 Vererbung](#73-vererbung)
    - [7.4 Typisches Klassen-Pattern (Tool-Aufbau)](#74-typisches-klassen-pattern-tool-aufbau)
- [8. String-Manipulation](#8-string-manipulation)
    - [8.1 Wichtige String-Methoden](#81-wichtige-string-methoden)
    - [8.2 f-String-Formatierung](#82-f-string-formatierung)
    - [8.3 `bytes` ↔ `str`](#83-bytes--str)
- [9. Datei-I/O](#9-datei-io)
    - [9.1 Lesen](#91-lesen)
    - [9.2 Schreiben](#92-schreiben)
    - [9.3 Binärmodus](#93-binärmodus)
- [10. Fehlerbehandlung](#10-fehlerbehandlung)
    - [10.1 `try` / `except`](#101-try--except)
    - [10.2 Eigene Exceptions](#102-eigene-exceptions)
- [11. Standard-Bibliothek](#11-standard-bibliothek)
    - [11.1 `argparse` — Kommandozeilen-Argumente](#111-argparse--kommandozeilen-argumente)
    - [11.2 `subprocess` — Shell-Befehle ausführen](#112-subprocess--shell-befehle-ausführen)
    - [11.3 `subprocess.run` & Hintergrund-Prozesse](#113-subprocessrun--hintergrund-prozesse)
    - [11.4 `threading` — Nebenläufigkeit](#114-threading--nebenläufigkeit)
    - [11.5 `re` — Reguläre Ausdrücke](#115-re--reguläre-ausdrücke)
    - [11.6 `re` — Gruppen, `finditer`, Flags](#116-re--gruppen-finditer-flags)
    - [11.7 `os` — Pfade & Umgebung](#117-os--pfade--umgebung)
    - [11.8 `pathlib` — objektorientierte Pfade](#118-pathlib--objektorientierte-pfade)
    - [11.9 `datetime` — Zeitstempel](#119-datetime--zeitstempel)
    - [11.10 `json` — Serialisierung](#1110-json--serialisierung)
- [12. Netzwerk (`socket`)](#12-netzwerk-socket)
    - [12.1 TCP Client](#121-tcp-client)
    - [12.2 TCP Server (mit Threading)](#122-tcp-server-mit-threading)
    - [12.3 UDP Client](#123-udp-client)
    - [12.4 Socket-Konstanten](#124-socket-konstanten)
    - [12.5 Daten senden & empfangen (Stream-Muster)](#125-daten-senden--empfangen-stream-muster)
- [13. Kryptoanalyse-Techniken](#13-kryptoanalyse-techniken)
    - [13.1 Caesar-Verschlüsselung](#131-caesar-verschlüsselung)
    - [13.2 Vigenère-Verschlüsselung](#132-vigenère-verschlüsselung)
    - [13.3 Häufigkeitsanalyse](#133-häufigkeitsanalyse)
    - [13.4 n-Gramme (Bi-/Trigramme)](#134-n-gramme-bi-trigramme)
- [14. Web: `requests` & `BeautifulSoup`](#14-web-requests--beautifulsoup)
- [15. Idiome & Muster](#15-idiome--muster)
    - [15.1 `if __name__ == "__main__":`](#151-if-__name__--__main__)
    - [15.2 Context Manager (`with`)](#152-context-manager-with)
    - [15.3 Sortieren nach Wert](#153-sortieren-nach-wert)
    - [15.4 `enumerate` & `zip`](#154-enumerate--zip)
    - [15.5 `bytes` & Encoding](#155-bytes--encoding)
    - [15.6 Dict-Tricks](#156-dict-tricks)
    - [15.7 String-Formatierung auf einen Blick](#157-string-formatierung-auf-einen-blick)
- [16. Schnellreferenz: Häufige Module](#16-schnellreferenz-häufige-module)

---

## 1. Grundsyntax

### 1.1 Variablen & Zuweisung

```python
# Python ist dynamisch typisiert: der Typ ergibt sich aus dem Wert.
# Eine Typangabe wie in Java/C (int x = 42;) gibt es nicht.
x = 42              # int
name = "Alice"      # str
pi = 3.14           # float
flag = True         # bool  (Achtung: True/False groß geschrieben)

# Mehrfachzuweisung: rechts wird ein Tuple gebaut, links wieder entpackt
a, b, c = 1, 2, 3

# Tauschen ohne Hilfsvariable:
# die rechte Seite wird KOMPLETT ausgewertet, bevor zugewiesen wird
a, b = b, a
```

### 1.2 Typen prüfen & konvertieren

```python
type(x)                 # <class 'int'>   -> exakter Typ, gut zum Debuggen
isinstance(x, int)      # True            -> zum Abfragen in if (beachtet Vererbung)

# Konvertierung (jede Funktion baut ein NEUES Objekt, ändert nichts in-place)
int("42")               # 42        String -> Zahl (ValueError bei "abc")
str(42)                 # "42"      Zahl -> String
float("3.14")           # 3.14
list("abc")             # ['a','b','c']   String wird zeichenweise zerlegt
```

### 1.3 Ausgabe & f-Strings

```python
# f-String: alles in {} wird als Python-Ausdruck ausgewertet und eingesetzt
print(f"Name: {name}, Wert: {x:.2f}")   # :.2f  -> 2 Nachkommastellen
print(f"{x:3d}: {name}")                # :3d   -> Ganzzahl in Spalte der Breite 3

# print hängt automatisch \n an; das lässt sich abschalten:
print("kein Umbruch", end="")
print("a", "b", sep="-")                # 'a-b'  Trennzeichen zwischen Argumenten
```

---

## 2. Datenstrukturen

### 2.1 Liste — mutable, geordnet

```python
lst = [1, 2, 3, 4, 5]

lst.append(6)           # hängt EIN Element hinten an          -> O(1)
lst.insert(0, 0)        # fügt an Index ein, schiebt Rest nach rechts -> O(n)
lst.pop()               # entfernt letztes Element UND gibt es zurück
lst.pop(0)              # entfernt Element an Index 0 (langsam, alles rutscht)
lst.remove(3)           # entfernt den ERSTEN Treffer mit Wert 3 (ValueError wenn nicht da)

lst[1:3]                # Slice: ab Index 1 bis VOR Index 3 -> [2, 3]
lst[::-1]               # Schrittweite -1 -> umgekehrte KOPIE der Liste

lst.sort()              # sortiert die Liste selbst um, gibt None zurück (!)
sorted(lst)             # lässt das Original in Ruhe, gibt neue Liste zurück
len(lst)                # Anzahl der Elemente
```

### 2.2 Dictionary — Schlüssel-Wert-Paare

```python
d = {"a": 1, "b": 2}

d["c"] = 3              # legt Key an oder überschreibt ihn
d["x"]                  # KeyError, wenn "x" nicht existiert
d.get("x", 0)           # sicherer Zugriff: liefert 0 statt Fehler

d.keys()                # alle Schlüssel      (Sicht, kein echtes list)
d.values()              # alle Werte
d.items()               # Paare (key, value) -> ideal für for-Schleifen

del d["a"]              # Eintrag löschen
"b" in d                # True  -> 'in' prüft bei dicts die SCHLÜSSEL, nicht die Werte

# Häufigkeiten zählen (klassisches Muster, taucht überall wieder auf)
freq = {}
for item in collection:
    # beim ersten Sehen ist der Key noch nicht da -> get() liefert 0
    freq[item] = freq.get(item, 0) + 1
```

### 2.3 Tuple — immutable

```python
t = (1, 2, 3)           # wie eine Liste, aber nach dem Anlegen unveränderbar
a, b, c = t             # Unpacking: passt nur, wenn die Anzahl exakt stimmt
t[0]                    # Zugriff wie bei der Liste
# Einsatz: feste Wertepaare (x, y), Rückgabe mehrerer Werte, Dict-Keys
```

### 2.4 Set — Menge ohne Duplikate

```python
s = {1, 2, 3}           # Reihenfolge egal, jeder Wert nur EINMAL enthalten
s.add(4)                # hinzufügen (doppelte Werte werden still ignoriert)
s.discard(2)            # entfernen OHNE Fehler, falls nicht vorhanden
s.remove(2)             # entfernen MIT KeyError, falls nicht vorhanden

s1 & s2                 # Schnittmenge   (in beiden enthalten)
s1 | s2                 # Vereinigung    (in mindestens einem)
s1 - s2                 # Differenz      (nur in s1)
s1.intersection(s2)     # ausgeschriebene Varianten derselben Operationen
s1.union(s2)
s1.difference(s2)

set(lst)                # Trick: entfernt Duplikate aus einer Liste
```

### 2.5 Stack & Queue

```python
from collections import deque

# Stack (LIFO — Last In, First Out): normale Liste reicht,
# weil hinten anhängen und hinten entfernen beides O(1) ist
stack = []
stack.append("a")       # push
stack.pop()             # pop -> nimmt das ZULETZT eingefügte Element

# Queue (FIFO — First In, First Out): deque statt Liste verwenden!
# list.pop(0) müsste alle Elemente umkopieren -> O(n)
queue = deque()
queue.append("Erstes")      # hinten einreihen
queue.append("Zweites")
queue.popleft()             # 'Erstes' -> vorne entnehmen, O(1)
```

---

## 3. Kontrollfluss & Schleifen

### 3.1 Bedingungen

```python
# Blöcke werden über EINRÜCKUNG abgegrenzt (keine geschweiften Klammern)
if x > 10:
    pass                # 'pass' = Platzhalter, tut nichts
elif x == 10:           # beliebig viele elif möglich
    pass
else:
    pass

# Ternary: kurzes if/else in einer Zeile (Wert, kein Statement)
result = "ja" if x > 0 else "nein"
```

### 3.2 for-Schleifen

```python
# for läuft immer über ein iterierbares Objekt (Liste, String, dict, range ...)
for i in range(10):             # 0 bis 9 — die Obergrenze ist NICHT dabei
    pass
for i in range(2, 10, 2):       # start, stop, schritt -> 2, 4, 6, 8
    pass

for i, val in enumerate(lst):               # zählt automatisch mit, Start 0
    pass
for pos, val in enumerate(lst, start=1):    # Zähler beginnt bei 1 (für Ausgaben)
    pass

for k, v in d.items():                      # Dict: Key und Wert gleichzeitig
    pass
for i, (k, v) in enumerate(d.items(), start=1):
    # Klammern um (k, v) nötig: enumerate liefert (index, element),
    # das element ist hier selbst ein Tuple und wird nochmal entpackt
    pass
```

### 3.3 while-Schleifen

```python
while condition:        # läuft, solange die Bedingung wahr ist
    break               # verlässt die Schleife SOFORT komplett
    continue            # springt direkt zur nächsten Iteration
```

### 3.4 Comprehensions

```python
# List Comprehension: [ausdruck for element in quelle if bedingung]
# Kurzform für "leere Liste anlegen + Schleife + append"
squares  = [x**2 for x in range(10)]        # jedes Element umrechnen
filtered = [x for x in lst if x > 0]        # nur passende Elemente übernehmen

# Verschachtelt: die Schleifen stehen in derselben Reihenfolge wie ausgeschrieben
flat = [item for sub in matrix for item in sub]   # 2D-Liste -> flache Liste

# Dict Comprehension: {schlüssel: wert for ...}
inverted = {v: k for k, v in d.items()}                 # Key und Wert tauschen
rel_freq = {k: v / total * 100 for k, v in freq.items()}  # absolut -> Prozent
```

---

## 4. Funktionen

### 4.1 Definition & Default-Parameter

```python
def greet(name, greeting="Hallo"):
    # Parameter mit Default müssen HINTER den Pflichtparametern stehen
    return f"{greeting}, {name}!"

greet("Bob")                    # 'Hallo, Bob!'      Default greift
greet("Bob", greeting="Hi")     # Keyword-Argument: Reihenfolge egal, lesbarer

# Falle: veränderbare Defaults (Liste/Dict) werden nur EINMAL erzeugt
def bad(x, acc=[]):     # acc bleibt zwischen Aufrufen erhalten -> Bug
    acc.append(x)
def good(x, acc=None):  # richtig: None als Marker und drinnen neu anlegen
    acc = [] if acc is None else acc
```

### 4.2 `*args` und `**kwargs`

```python
def func(*args, **kwargs):
    # *args    sammelt alle unbenannten Argumente in einem Tuple
    # **kwargs sammelt alle benannten Argumente in einem Dict
    for a in args: ...
    for k, v in kwargs.items(): ...

func(1, 2, modus="schnell")     # args = (1, 2)   kwargs = {'modus': 'schnell'}

# Umgekehrt: eine vorhandene Liste/Dict beim Aufruf entpacken
werte = [1, 2]
func(*werte)                    # entspricht func(1, 2)
```

### 4.3 Lambda

```python
# Lambda = namenlose Funktion aus EINEM Ausdruck (return ist implizit)
square = lambda x: x ** 2

# Haupteinsatz: als key-Funktion, die bestimmt, WONACH sortiert wird
sorted_list = sorted(items, key=lambda item: item[1], reverse=True)
#                                            ^ sortiere nach dem 2. Element
items = [("Anna", 3), ("Bob", 7), ("Cem", 1)]
sorted(items)                        # ohne key: vergleicht die Tupel selbst,
# [('Anna', 3), ('Bob', 7), ('Cem', 1)]   -> also erst nach Name (Element 0)
sorted(items, key=lambda item: item[1])
# [('Cem', 1), ('Anna', 3), ('Bob', 7)]   -> nach der Zahl (Element 1)
```

### 4.4 Closures — verschachtelte Funktionen

```python
def outer(n):
    def inner(x):
        return x + n    # inner "merkt" sich n aus dem äußeren Aufruf
    return inner        # die Funktion selbst wird zurückgegeben (nicht aufgerufen!)

add5 = outer(5)         # n ist jetzt fest auf 5 eingefroren
add5(3)                 # 8
```

### 4.5 Type Hints & Annotationen

```python
# Type Hints sind DOKUMENTATION für Menschen und Werkzeuge (IDE, mypy).
# Python prüft sie zur Laufzeit NICHT — add("a", "b") läuft trotzdem durch
# und ergibt "ab". Der Nutzen: Autovervollständigung und Fehler VOR dem Start.

from __future__ import annotations   # Annotationen werden nicht sofort ausgewertet,
                                     # sondern als Text behandelt -> neue Schreibweisen
                                     # (list[int], X | None) gehen auch in älteren Versionen
                                     # Muss als ERSTE Anweisung der Datei stehen.

def add(a: int, b: int) -> int:      # Parametertypen nach dem ':', Rückgabetyp nach '->'
    return a + b

name: str = "Alice"                  # Variablen-Annotation (Typ vor der Zuweisung)
werte: list[int] = [1, 2, 3]         # ab 3.9: Liste VON int  (davor: List[int] aus typing)
mapping: dict[str, int] = {}         # dict[Key-Typ, Wert-Typ]
paare: tuple[str, int] = ("a", 1)    # Tuple: jeder Position ihr eigener Typ

# Union: mehrere erlaubte Typen, getrennt durch '|' (ab 3.10; davor Optional/Union aus typing)
def find(x) -> Service | None:       # gibt ein Service-Objekt ODER None zurück
    ...                              # -> beim Aufrufer ist ein 'if result is None' Pflicht

def run(cmd, timeout: int | None = None) -> None:
    ...                              # '-> None' = die Funktion gibt bewusst nichts zurück
                                     # 'int | None = None' = optionaler Parameter

# Ohne 'from __future__ import annotations' muss man Typen, die noch nicht
# definiert sind (z.B. die eigene Klasse), als STRING schreiben:
def helper(x) -> "list[Service] | None":
    ...

# Häufige Typen aus typing (für Fälle, die die Kurzschreibweise nicht abdeckt)
from typing import Any, Callable, Iterable
def apply(f: Callable[[int], str], daten: Iterable[int]) -> list[str]:
    #        ^ Funktion, die int nimmt und str liefert
    return [f(x) for x in daten]
# Any = "egal welcher Typ" -> schaltet die Prüfung für diese Stelle faktisch ab
```

---

## 5. Algorithmen

### 5.1 Iteration vs. Rekursion — Fibonacci

```python
# Iterativ: eine Schleife, konstanter Speicher -> die praxistaugliche Variante
def fib_iter(n):
    if n <= 1:
        return n                    # Abbruch für die ersten beiden Glieder
    a, b = 0, 1                     # a = fib(i-2), b = fib(i-1)
    for _ in range(2, n + 1):       # _ = Laufvariable wird nicht gebraucht
        a, b = b, a + b             # beide Werte gleichzeitig weiterschieben
    return b

# Rekursiv: die Funktion ruft sich selbst auf, bis der Basisfall greift
def fib_rek(n):
    if n <= 1:                      # BASISFALL — ohne ihn läuft es endlos
        return n
    # jeder Aufruf erzeugt zwei neue Aufrufe -> O(2^n), ab n≈35 unbrauchbar
    return fib_rek(n - 1) + fib_rek(n - 2)
```

### 5.2 Suchalgorithmen

```python
# Lineare Suche — O(n), funktioniert auf JEDER (auch unsortierter) Liste
def linear_search(liste, ziel):
    for i in range(len(liste)):     # jedes Element von vorne durchgehen
        if liste[i] == ziel:
            return i                # Index des Treffers zurückgeben
    return -1                       # Konvention: -1 = nicht gefunden
# Randfälle: leere Liste -> Schleife läuft nie -> -1
#            mehrere Treffer -> immer das ERSTE Vorkommen

# Binäre Suche — O(log n), setzt eine SORTIERTE Liste voraus
def binary_search(liste, ziel):
    links, rechts = 0, len(liste) - 1        # Grenzen des Suchbereichs
    while links <= rechts:                   # solange der Bereich nicht leer ist
        mid = (links + rechts) // 2          # // = Ganzzahldivision -> Mittelindex
        if liste[mid] == ziel:
            return mid                       # Treffer
        elif liste[mid] < ziel:
            links = mid + 1                  # Ziel liegt rechts -> linke Hälfte weg
        else:
            rechts = mid - 1                 # Ziel liegt links  -> rechte Hälfte weg
    return -1
# Randfälle: leere Liste -> links=0, rechts=-1 -> kein Schleifendurchlauf -> -1
#            mehrere Treffer -> IRGENDEIN Vorkommen, nicht zwingend das erste
```

### 5.3 Sortieralgorithmen

```python
# Bubble Sort — O(n²) | Idee: benachbarte Paare vergleichen und tauschen,
# dadurch "blubbert" das größte Element pro Durchlauf ganz nach hinten
def bubble_sort(liste):
    n = len(liste)
    for i in range(n):                      # n Durchläufe
        for j in range(0, n - i - 1):       # '- i': hinten stehen bereits i sortierte
            if liste[j] > liste[j + 1]:
                # Tausch in einer Zeile über Tuple-Zuweisung
                liste[j], liste[j + 1] = liste[j + 1], liste[j]

# Selection Sort — O(n²) | Idee: Minimum des Restes suchen und nach vorne tauschen
def selection_sort(liste):
    n = len(liste)
    for i in range(n):                      # i = Position, die gefüllt wird
        min_index = i                       # Annahme: aktuelles Element ist Minimum
        for j in range(i + 1, n):           # Rest der Liste durchsuchen
            if liste[j] < liste[min_index]:
                min_index = j               # neues Minimum merken
        liste[i], liste[min_index] = liste[min_index], liste[i]   # einmal tauschen

# Insertion Sort — O(n²) worst, O(n) bei fast sortierten Listen
# Idee: linke Teilliste ist sortiert, jedes neue Element wird eingefügt (wie Karten)
def insertion_sort(liste):
    for i in range(1, len(liste)):          # Element 0 gilt als sortiert
        key = liste[i]                      # Element, das eingeordnet wird
        j = i - 1                           # letzter Index der sortierten Teilliste
        while j >= 0 and liste[j] > key:    # alles Größere ...
            liste[j + 1] = liste[j]         # ... eine Position nach rechts schieben
            j -= 1
        liste[j + 1] = key                  # Lücke mit key füllen

# Mergesort — O(n log n) in allen Fällen | stabil | braucht Extra-Speicher
# Idee: halbieren -> rekursiv sortieren -> sortierte Hälften zusammenführen
def mergesort(liste):
    if len(liste) > 1:                      # Basisfall: 0 oder 1 Element ist sortiert
        mid   = len(liste) // 2
        left  = liste[:mid]                 # Slice erzeugt KOPIEN der Hälften
        right = liste[mid:]
        mergesort(left)                     # linke Hälfte sortieren
        mergesort(right)                    # rechte Hälfte sortieren

        i = j = k = 0                       # i=left, j=right, k=Zielposition
        while i < len(left) and j < len(right):     # solange beide Hälften Reste haben
            if left[i] < right[j]:                  # jeweils den kleineren Kopf nehmen
                liste[k] = left[i];  i += 1
            else:
                liste[k] = right[j]; j += 1
            k += 1
        while i < len(left):                # Rest der linken Hälfte anhängen
            liste[k] = left[i];  i += 1; k += 1
        while j < len(right):               # Rest der rechten Hälfte anhängen
            liste[k] = right[j]; j += 1; k += 1

# Quicksort — O(n log n) im Schnitt, O(n²) wenn das Pivot immer extrem liegt
# Idee: Pivot wählen -> kleinere nach links, größere nach rechts -> rekursiv
def quicksort(liste):
    if len(liste) <= 1:                     # Basisfall
        return liste
    pivot = liste[0]                        # einfachste Wahl: erstes Element
    left  = [x for x in liste[1:] if x <= pivot]   # alles <= Pivot
    right = [x for x in liste[1:] if x >  pivot]   # alles >  Pivot
    # rekursiv sortieren und mit dem Pivot in der Mitte zusammensetzen
    return quicksort(left) + [pivot] + quicksort(right)
```

### 5.4 Komplexitäts-Übersicht

Stabil = Elemente mit gleichem Schlüssel behalten ihre ursprüngliche Reihenfolge.

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

## 6. Generatoren & `yield`

### 6.1 Generator-Funktion

```python
# Eine Funktion mit yield liefert Werte EINZELN, statt eine ganze Liste
# im Speicher aufzubauen. Bei yield "pausiert" die Funktion und merkt sich
# ihren kompletten Zustand; beim nächsten next() läuft sie dort weiter.
def zaehle(n):
    i = 0
    while i < n:
        yield i            # Wert herausgeben und an dieser Stelle anhalten
        i += 1             # läuft erst beim nächsten Abruf weiter

for x in zaehle(3):        # for ruft intern next() auf -> 0, 1, 2
    print(x)

gen = zaehle(3)            # Aufruf startet NICHTS, erzeugt nur das Generator-Objekt
next(gen)                  # 0   — manuell einen Wert ziehen
next(gen)                  # 1
```

### 6.2 `yield from`

```python
def flach(listen):
    for teil in listen:
        yield from teil    # an einen Untergenerator delegieren
                           # Kurzform für: for x in teil: yield x

list(flach([[1, 2], [3, 4]]))   # [1, 2, 3, 4]  -> list() zieht alle Werte
```

### 6.3 Typischer Einsatz

```python
# Große Datei zeilenweise verarbeiten, ohne sie komplett zu laden
def nicht_leere_zeilen(pfad):
    with open(pfad, encoding="utf-8") as f:
        for zeile in f:                  # die Datei selbst ist schon iterierbar
            zeile = zeile.strip()
            if zeile:                    # leere Zeilen überspringen
                yield zeile
```

---

## 7. Klassen (OOP)

### 7.1 Grundgerüst

```python
class MyClass:
    CLASS_VAR = "shared"       # Klassenvariable: für ALLE Instanzen gemeinsam

    def __init__(self, x, y):  # Konstruktor: läuft beim Erzeugen automatisch
        self.x = x             # Instanzvariable: gehört nur zu diesem Objekt
        self.y = y

    def method(self):          # self = das Objekt selbst, immer 1. Parameter
        return self.x + self.y

obj = MyClass(1, 2)            # __init__ wird hier aufgerufen (self kommt automatisch)
obj.method()                   # 3
```

### 7.2 Dunder-Methoden

```python
class MyClass:
    def __repr__(self):        # Darstellung für Entwickler (Debugger, Konsole, Listen)
        return f"MyClass({self.x}, {self.y})"

    def __str__(self):         # Darstellung für Nutzer -> wird von print() genutzt
        return f"({self.x}, {self.y})"
# Fehlt __str__, greift print() auf __repr__ zurück -> im Zweifel __repr__ bauen
```

### 7.3 Vererbung

```python
class Child(MyClass):              # erbt alle Methoden von MyClass
    def __init__(self, x, y, z):
        super().__init__(x, y)     # Konstruktor der Elternklasse aufrufen (Pflicht!)
        self.z = z                 # eigene Erweiterung

    def method(self):              # Override: ersetzt die geerbte Methode
        return super().method() + self.z   # Original weiterverwenden statt kopieren
```

### 7.4 Typisches Klassen-Pattern (Tool-Aufbau)

```python
class Tool:
    def __init__(self, args):
        self.args = args
        # Ressourcen vorbereiten (Socket, Datei, Verbindung ...)

    def run(self):                 # zentrale Weiche: entscheidet den Modus
        if self.args.mode_a:
            self.mode_a()
        else:
            self.mode_b()

    def mode_a(self): ...          # jede Betriebsart in einer eigenen Methode
    def mode_b(self): ...

if __name__ == "__main__":         # nur beim direkten Start ausführen
    args = parse_args()
    t = Tool(args)
    t.run()
```

---

## 8. String-Manipulation

### 8.1 Wichtige String-Methoden

```python
s = "Hello World"
# WICHTIG: Strings sind immutable — jede Methode liefert einen NEUEN String,
# das Original bleibt unverändert (s = s.upper() nicht vergessen).

s.upper()   s.lower()   s.title()      # Groß / klein / Jedes Wort Groß
s.strip()                              # Whitespace an BEIDEN Enden weg (inkl. \n)
s.lstrip()  s.rstrip()                 # nur links / nur rechts

s.split()                              # ohne Argument: an beliebigem Whitespace
s.split(",")                           # an Komma trennen -> Liste
",".join(["a","b","c"])                # Liste -> String; Trenner steht VORNE

s.replace("Hello", "Hi")               # alle Vorkommen ersetzen
s.startswith("He")   s.endswith("ld")  # Prüfung am Anfang / Ende -> bool
s.find("World")                        # Index des ersten Treffers, sonst -1
s.count("l")                           # Anzahl der Vorkommen
len(s)                                 # Länge in Zeichen

s[1:5]                                 # Slice wie bei Listen
s[::-1]                                # String umkehren
```

### 8.2 f-String-Formatierung

```python
f"{val:.2f}"       # 2 Dezimalstellen (rundet)
f"{val:>10}"       # rechtsbündig in Breite 10 (mit Leerzeichen aufgefüllt)
f"{val:<10}"       # linksbündig
f"{val:03d}"       # Ganzzahl mit führenden Nullen -> '007'
f"{i:3d}: {item}"  # typisch für saubere Spalten in Ausgaben
```

### 8.3 `bytes` ↔ `str`

```python
# Netzwerk und Dateien im Binärmodus arbeiten mit bytes (b"..."),
# der Rest von Python mit str -> an den Grenzen umwandeln.
"text".encode("utf-8")             # str    -> bytes
b"bytes".decode("utf-8")           # bytes  -> str  (UnicodeDecodeError möglich)
b"bytes".decode(errors="replace")  # fehlertolerant: unbekannte Bytes werden ersetzt
```

---

## 9. Datei-I/O

### 9.1 Lesen

```python
# 'with' schließt die Datei automatisch — auch wenn eine Exception fliegt
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()        # gesamte Datei als EIN String
    lines   = f.readlines()   # Liste von Zeilen (inkl. \n am Ende)
# Achtung: nach read() ist der Lesezeiger am Ende -> readlines() liefert dann []

# Zeilenweise: speicherschonend, auch bei riesigen Dateien
with open("file.txt") as f:
    for line in f:
        print(line.strip())   # strip() entfernt das \n am Zeilenende
```

### 9.2 Schreiben

```python
with open("out.txt", "w", encoding="utf-8") as f:   # 'w' LEERT die Datei zuerst!
    f.write("Zeile 1\n")      # write() setzt KEIN \n automatisch

with open("out.txt", "a", encoding="utf-8") as f:   # 'a' = anhängen
    f.write("Zeile 2\n")
```

### 9.3 Binärmodus

```python
# 'b' im Modus -> es wird mit bytes gearbeitet, encoding entfällt
with open("file.bin", "rb") as f:      # lesen
    data = f.read()

with open("out.bin", "wb") as f:       # schreiben
    f.write(data)
```

| Modus | Bedeutung |
|---|---|
| `'r'` | Lesen (Standard), Fehler wenn Datei fehlt |
| `'w'` | Schreiben, legt neu an bzw. **überschreibt** |
| `'a'` | Anhängen ans Ende |
| `'rb'` / `'wb'` | dasselbe im Binärmodus (bytes) |

---

## 10. Fehlerbehandlung

### 10.1 `try` / `except`

```python
try:
    result = int("abc")           # hier kann es krachen
except ValueError as e:           # spezifische Fehler ZUERST abfangen
    print(f"Fehler: {e}")         # e enthält die Fehlermeldung
except (TypeError, KeyError):     # mehrere Typen gemeinsam behandeln
    pass
except Exception as e:            # Auffangnetz, immer als LETZTES
    print(f"Unbekannter Fehler: {e}")
else:
    print("Kein Fehler")          # läuft nur, wenn try komplett durchlief
finally:
    print("Immer ausgeführt")     # läuft IMMER -> Aufräumen, Schließen
```

### 10.2 Eigene Exceptions

```python
class MyError(Exception):         # von Exception erben reicht völlig
    pass                          # eigener Typ, damit man ihn gezielt fangen kann

raise MyError("Etwas ist schiefgelaufen")   # Fehler selbst auslösen
```

---

## 11. Standard-Bibliothek

### 11.1 `argparse` — Kommandozeilen-Argumente

```python
import argparse, textwrap

parser = argparse.ArgumentParser(
    description="Mein Tool",                                  # Kopfzeile bei -h
    formatter_class=argparse.RawDescriptionHelpFormatter,     # behält Zeilenumbrüche im epilog
    epilog=textwrap.dedent('''
        Beispiele:
          python tool.py -t 127.0.0.1 -p 4444 -l
    ''')                                                       # dedent entfernt die Einrückung
)

# Kurz- und Langform; der Attributname ergibt sich aus der Langform
parser.add_argument('-t', '--target', default='0.0.0.0', help='Ziel-IP')
parser.add_argument('-p', '--port',   type=int, default=4554)   # type= konvertiert automatisch
parser.add_argument('-l', '--listen', action='store_true')      # Flag: True wenn gesetzt, sonst False
parser.add_argument('-e', '--execute', help='Befehl ausführen')

args = parser.parse_args()      # liest sys.argv; bei Fehlern: Hilfe ausgeben + beenden
args.target, args.port, args.listen, args.execute
```

### 11.2 `subprocess` — Shell-Befehle ausführen

```python
import subprocess, shlex

# check_output: führt aus und liefert die Ausgabe als bytes zurück
output = subprocess.check_output(
    shlex.split("ls -la"),      # shlex.split: "ls -la" -> ["ls", "-la"] (beachtet Quotes)
    stderr=subprocess.STDOUT    # Fehlerkanal in die normale Ausgabe umleiten
)
text = output.decode(errors="replace")      # bytes -> str

# shell=True: der String geht an die Shell (nötig für Built-ins wie 'dir')
# Nur mit fest verdrahteten Befehlen nutzen, nie mit fremden Eingaben.
output = subprocess.check_output("cmd /c dir", shell=True, stderr=subprocess.STDOUT)

try:
    out = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as e:  # Exit-Code != 0
    out = e.output                          # Ausgabe ist trotzdem verfügbar
except FileNotFoundError:
    pass                                    # Befehl existiert gar nicht
```

### 11.3 `subprocess.run` & Hintergrund-Prozesse

```python
import subprocess, shlex, shutil

# Vorher prüfen, ob ein Programm überhaupt installiert ist (statt Exception abzuwarten)
if shutil.which("nmap"):        # liefert den Pfad oder None
    ...

# subprocess.run: der moderne Allrounder (empfohlen statt check_output)
proc = subprocess.run(
    ["nmap", "-sV", "10.0.0.1"],
    capture_output=True,      # stdout und stderr auffangen statt durchreichen
    text=True,                # Ergebnis als str statt bytes
    timeout=120,              # hartes Zeitlimit in Sekunden
    errors="replace",         # keine Abstürze bei kaputten Zeichen
)
proc.returncode               # 0 = ok, alles andere = Fehler
proc.stdout                   # Ausgabe als String
proc.stderr

# Timeout sauber behandeln
try:
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
except subprocess.TimeoutExpired as e:
    teil = e.stdout or ""     # die Teilausgabe bis zum Timeout bleibt erhalten

# Popen: startet den Prozess und läuft SOFORT weiter (blockiert nicht)
p = subprocess.Popen(
    ["nc", "-lvnp", "4444"],
    stdout=subprocess.DEVNULL,   # Ausgabe ins Leere leiten
    stderr=subprocess.DEVNULL,   # sonst füllt sich der Puffer und der Prozess hängt
    stdin=subprocess.DEVNULL,
)
p.pid                          # PID merken, um ihn später zu finden
p.terminate()                  # sanft beenden (SIGTERM)
p.kill()                       # hart beenden, falls terminate nicht wirkt
```

### 11.4 `threading` — Nebenläufigkeit

```python
import threading

def worker(arg):
    print(f"Thread arbeitet: {arg}")

t = threading.Thread(
    target=worker,       # Funktion OHNE Klammern übergeben (sonst wird sie sofort ausgeführt)
    args=(my_arg,)       # Komma nicht vergessen -> Tuple mit einem Element
)
t.start()                # startet den Thread, main läuft parallel weiter
t.join()                 # wartet, bis dieser Thread fertig ist

# Lock: schützt gemeinsam genutzte Daten vor gleichzeitigem Zugriff
lock = threading.Lock()
with lock:                       # betritt nur ein Thread gleichzeitig
    shared_variable += 1         # 'with' gibt das Lock auch bei Exception frei
```

### 11.5 `re` — Reguläre Ausdrücke

```python
import re
# r"..." = Raw-String: Backslashes bleiben stehen -> für Regex immer verwenden

re.findall(r"\w+", text)        # Liste ALLER Treffer (hier: alle Wörter)
re.findall(r"\d+", text)        # alle Zahlen
re.search(r"pattern", text)     # erster Treffer irgendwo -> Match-Objekt oder None
re.match(r"^start", text)       # sucht NUR am Stringanfang
re.sub(r"\s+", " ", text)       # Ersetzen: mehrere Leerzeichen -> eines
```

Wichtige Zeichenklassen:

| Muster | Bedeutung |
|---|---|
| `\w` | Buchstabe, Ziffer oder `_` |
| `\d` | Ziffer |
| `\s` | Whitespace (Leerzeichen, Tab, `\n`) |
| `.` | beliebiges Zeichen außer `\n` |
| `+` | ein oder mehr |
| `*` | null oder mehr |
| `?` | optional (null oder eins) |
| `^` / `$` | Anfang / Ende |

### 11.6 `re` — Gruppen, `finditer`, Flags

```python
import re

# Capture-Gruppe: Klammern markieren den Teil, den man wirklich haben will
m = re.search(r"DB_PASSWORD=(\S+)", text)
if m:                           # search kann None liefern -> IMMER prüfen
    passwort = m.group(1)       # nur der Klammerinhalt
    ganzes   = m.group(0)       # der komplette Treffer

# finditer: alle Treffer als Match-Objekte (mit Gruppen und Position)
for m in re.finditer(r"(\d+)/open/tcp", text):
    port = int(m.group(1))

# Benannte Gruppen -> Zugriff über den Namen statt über die Nummer
m = re.search(r"(?P<user>\w+):(?P<pw>\w+)", "root:toor")
m.group("user")                 # 'root'

# Flags
re.search(r"start.*ende", text, re.DOTALL)      # '.' matcht dann auch Zeilenumbrüche
re.findall(r"abc", text, re.IGNORECASE)         # Groß-/Kleinschreibung egal

re.escape("a.b*c")              # 'a\\.b\\*c' -> Sonderzeichen wörtlich suchen
```

### 11.7 `os` — Pfade & Umgebung

```python
import os
os.makedirs("out/payloads", exist_ok=True)   # legt auch Zwischenordner an;
                                             # exist_ok verhindert Fehler, falls schon da
os.path.join("out", "loot", "f.txt")         # plattformneutral (/ bzw. \)
os.path.isfile(pfad)                          # existiert und ist eine Datei?
os.path.isdir(pfad)                           # existiert und ist ein Ordner?
os.listdir(pfad)                              # Namen im Ordner (nur Namen, keine Pfade)
os.environ.get("HOME", "/tmp")                # Umgebungsvariable mit Default
os.chmod(pfad, 0o755)                         # Rechte setzen (0o = oktal)
```

### 11.8 `pathlib` — objektorientierte Pfade

```python
from pathlib import Path
p = Path("out") / "loot" / "f.txt"            # '/' verkettet Pfadteile
p.parent.mkdir(parents=True, exist_ok=True)   # Ordner des Files anlegen
p.write_text("inhalt", encoding="utf-8")      # schreiben ohne open()/with
text = p.read_text(encoding="utf-8")          # lesen in einer Zeile

p.exists()      # gibt es den Pfad?
p.suffix        # '.txt'      Endung
p.stem          # 'f'         Name ohne Endung
p.name          # 'f.txt'     Name mit Endung
```

### 11.9 `datetime` — Zeitstempel

```python
import datetime
# strftime formatiert ein Datum als String (%Y=Jahr, %m=Monat, %d=Tag, %H:%M:%S=Uhrzeit)
datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")   # '2026-08-07 16:30:00'
datetime.date.today().isoformat()                        # '2026-08-07' (Standardformat)
```

### 11.10 `json` — Serialisierung

```python
import json
# Merkhilfe: die Varianten MIT 's' arbeiten auf Strings,
# die OHNE 's' direkt auf einer Datei (file).

# --- Objekt -> JSON-String ---
d = {"target": "10.0.0.1", "ports": [22, 80], "up": True}
s = json.dumps(d)                                 # kompakt, eine Zeile
s = json.dumps(d, indent=2, ensure_ascii=False)   # indent = eingerückt und lesbar
                                                  # ensure_ascii=False -> Umlaute bleiben
                                                  #   Umlaute statt \u00e4-Escapes
s = json.dumps(d, sort_keys=True)                 # Keys alphabetisch -> gut zum Vergleichen

# --- JSON-String -> Objekt ---
obj = json.loads('{"a": 1, "b": [2, 3]}')  # {'a': 1, 'b': [2, 3]} -> ganz normales dict
obj["b"][0]                                # danach wie jedes andere dict/list benutzen

# --- Direkt in/aus Datei ---
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)   # schreibt in das Datei-Objekt f

with open("data.json", encoding="utf-8") as f:
    obj = json.load(f)                              # liest aus f und parst in einem Schritt

# --- Muster: dataclass <-> JSON ---
from dataclasses import asdict
json.dumps(asdict(service))                # asdict() macht aus dem Objekt erst ein dict,
                                           # denn json kennt eigene Klassen nicht

# Für Typen, die json nicht kann (datetime, Path, set ...):
json.dumps(d, default=str)                 # default = Notfall-Umwandlung in einen String

# --- Fehler abfangen ---
try:
    obj = json.loads(text)                 # kaputtes/leeres JSON knallt hier
except json.JSONDecodeError as e:
    print(f"Ungültiges JSON: {e}")         # e nennt Zeile und Spalte der Fehlerstelle
```

Typ-Zuordnung beim Umwandeln:

| Python | JSON |
|---|---|
| `dict` | object `{}` |
| `list`, `tuple` | array `[]` |
| `str` | string |
| `int`, `float` | number |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

> Achtung: `tuple` wird zu einem Array — beim Zurücklesen ist daraus eine `list` geworden.
> JSON-Keys sind immer Strings: `{1: "a"}` wird zu `{"1": "a"}`.

---

## 12. Netzwerk (`socket`)

### 12.1 TCP Client

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # IPv4 + TCP
client.connect(("127.0.0.1", 4554))      # Ziel als TUPLE (host, port)
client.send(b"Hallo\n")                  # nur bytes senden -> b"" oder .encode()
response = client.recv(4096)             # blockiert, bis Daten kommen; max. 4096 Bytes
print(response.decode())
client.close()                           # Verbindung schließen
```

### 12.2 TCP Server (mit Threading)

```python
import socket, threading

def handle(sock):                        # ein Handler pro Verbindung
    data = sock.recv(1024)
    sock.send(b"ACK")
    sock.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Port nach Neustart sofort frei
server.bind(("0.0.0.0", 4554))           # 0.0.0.0 = auf allen Interfaces lauschen
server.listen()                          # in den Lausch-Modus wechseln

while True:
    client_sock, addr = server.accept()  # blockiert -> (socket, (ip, port))
    # eigener Thread pro Client, damit accept() sofort wieder bereit ist
    t = threading.Thread(target=handle, args=(client_sock,))
    t.start()
```

### 12.3 UDP Client

```python
# UDP ist verbindungslos: kein connect, keine Garantie für Ankunft/Reihenfolge
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # DGRAM statt STREAM
client.sendto(b"Nachricht", ("127.0.0.1", 4554))             # Ziel bei JEDEM Senden angeben
response, addr = client.recvfrom(4096)                        # liefert auch den Absender mit
```

### 12.4 Socket-Konstanten

| Konstante | Bedeutung |
|---|---|
| `AF_INET` | IPv4 |
| `AF_INET6` | IPv6 |
| `SOCK_STREAM` | TCP (verbindungsorientiert, zuverlässig) |
| `SOCK_DGRAM` | UDP (verbindungslos) |
| `SO_REUSEADDR` | Port sofort wieder nutzbar nach Neustart |

### 12.5 Daten senden & empfangen (Stream-Muster)

```python
# Grundproblem: TCP ist ein Byte-STROM, kein Nachrichten-Protokoll.
# recv() liefert evtl. nur einen Teil — oder mehrere "Nachrichten" auf einmal.

# Muster 1: bis zum Trennzeichen sammeln
buffer = b""
while b"\n" not in buffer:          # solange die Endmarke fehlt ...
    buffer += sock.recv(64)         # ... weiter anhängen
cmd = buffer.decode()

# Muster 2: Timeout als "Ende erkannt"
sock.settimeout(1.0)                # ab jetzt wirft recv nach 1s eine Exception
response = b""
try:
    while True:
        chunk = sock.recv(4096)
        if not chunk:               # leere bytes = Gegenseite hat geschlossen
            break
        response += chunk
except TimeoutError:                # 1s nichts mehr gekommen -> fertig
    pass
sock.settimeout(None)               # zurück in den blockierenden Modus

# Muster 3: bekannte Länge — genau n Bytes lesen
def recv_exact(sock, n):
    data = b""
    while len(data) < n:            # so oft nachladen, bis n Bytes da sind
        data += sock.recv(n - len(data))
    return data
```

---

## 13. Kryptoanalyse-Techniken

### 13.1 Caesar-Verschlüsselung

```python
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def caesar(text, key):
    """Verschiebt jeden Buchstaben um 'key' Stellen im Alphabet."""
    result = ""
    for c in text.upper():                  # einheitlich in Großbuchstaben arbeiten
        if c in ALPHABET:                   # nur Buchstaben verschieben ...
            # index -> verschieben -> % 26 sorgt für den Umbruch Z -> A
            result += ALPHABET[(ALPHABET.index(c) + key) % 26]
        else:
            result += c                     # ... Ziffern/Satzzeichen unverändert lassen
    return result

def de_caesar(text, key):
    return caesar(text, 26 - key)           # Rückwärts = um den Rest vorwärts

def brute_force(text):
    """Alle 25 möglichen Schlüssel durchprobieren und ausgeben."""
    for i in range(26):
        print(f"{i:2d}: {de_caesar(text, i)}")   # per Auge den sinnvollen Klartext suchen
```

### 13.2 Vigenère-Verschlüsselung

```python
def vigenere(text, password):
    """Polyalphabetisch: jeder Buchstabe bekommt eine eigene Verschiebung
    aus dem Passwort, das zyklisch wiederholt wird."""
    text, password = text.upper(), password.upper()
    result, key_i = "", 0                   # key_i zählt NUR die Buchstaben
    for c in text:
        if c in ALPHABET:
            # % len(password) -> das Passwort beginnt am Ende wieder von vorne
            shift = ALPHABET.index(password[key_i % len(password)])
            result += caesar(c, shift)      # Einzelzeichen wie bei Caesar verschieben
            key_i += 1                      # Schlüssel nur bei Buchstaben vorrücken,
        else:                               # damit Leerzeichen ihn nicht verschieben
            result += c
    return result
```

### 13.3 Häufigkeitsanalyse

```python
import operator

def freq(text):
    """Relative Häufigkeit jedes Zeichens in Prozent."""
    h = {}
    for c in text:
        h[c] = h.get(c, 0) + 1              # Zähler-Muster (siehe 2.2)
    total = len(text)
    return {k: v / total * 100 for k, v in h.items()}   # absolut -> Prozent

# Top-n absteigend ausgeben — im Deutschen/Englischen ist 'E' meist Spitzenreiter
sorted_freq = sorted(freq(text).items(), key=operator.itemgetter(1), reverse=True)
for rank, (char, pct) in enumerate(sorted_freq[:10]):    # [:10] = nur die ersten 10
    print(f"{rank:3d}: {char}  {pct:.2f}%")
```

### 13.4 n-Gramme (Bi-/Trigramme)

```python
def ngram(text, n):
    """Relative Häufigkeiten aller überlappenden n-Gramme."""
    ngrams = {}
    total = 0
    for delta in range(n):                  # Versatz 0..n-1 -> alle Startpositionen
        for i in range(0, len(text), n):    # in Schritten von n durch den Text
            teil = text[delta + i : delta + i + n]
            if len(teil) == n:              # abgeschnittenes Reststück verwerfen
                total += 1
                ngrams[teil] = ngrams.get(teil, 0) + 1
    # Schutz vor Division durch 0, falls kein einziges n-Gramm gefunden wurde
    return {k: v / total * 100 for k, v in ngrams.items()} if total else {}

# Bigramme  = ngram(text, 2)      häufig: 'EN', 'ER', 'CH'
# Trigramme = ngram(text, 3)      häufig: 'DER', 'EIN', 'SCH'
```

---

## 14. Web: `requests` & `BeautifulSoup`

```python
import requests
from bs4 import BeautifulSoup
import re

# --- HTTP-Anfragen ---
resp = requests.get("https://example.com")
resp.status_code   # 200 = OK, 404 = nicht gefunden, 500 = Serverfehler
resp.text          # Antwort als String (HTML)
resp.json()        # Antwort als dict, falls JSON zurückkommt

resp = requests.post(url, data={"key": "value"})   # klassisches Formular
resp = requests.post(url, json={"key": "value"})   # JSON-Body + passender Header

resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})   # Header setzen
resp = requests.get(url, timeout=10)               # sonst kann es ewig hängen

# --- HTML auswerten ---
soup = BeautifulSoup(resp.text, "html.parser")     # HTML in einen Baum parsen
text = soup.get_text()                             # nur den Fließtext ohne Tags

links = soup.find_all("a")                         # ALLE Treffer als Liste
title = soup.find("title").text                    # ERSTER Treffer (None wenn nichts da)
divs  = soup.find_all("div", class_="content")     # class_ mit Unterstrich (class ist reserviert)

# --- Wörter zählen ---
words = re.findall(r"\w+", text)                   # Text in Wörter zerlegen
freq = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1
top5 = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
```

---

## 15. Idiome & Muster

### 15.1 `if __name__ == "__main__":`

```python
# __name__ ist "__main__", wenn die Datei DIREKT gestartet wird,
# beim Import dagegen der Modulname -> so läuft der Testcode nicht ungewollt mit.
if __name__ == "__main__":
    main()
```

### 15.2 Context Manager (`with`)

```python
with open("file.txt") as f:    # ruft am Blockende automatisch f.close() auf
    data = f.read()

with socket.socket(...) as s:  # gilt genauso für Sockets, Locks, DB-Verbindungen
    s.connect(...)             # geschlossen wird auch bei einer Exception
```

### 15.3 Sortieren nach Wert

```python
top = sorted(d.items(), key=lambda x: x[1], reverse=True)[:10]  # Dict nach Wert, Top 10
sorted(objects, key=lambda o: o.score)                          # Objekte nach Attribut
sorted(items, key=lambda x: (x[1], x[0]))                       # 2 Kriterien: erst [1], dann [0]
```

### 15.4 `enumerate` & `zip`

```python
for i, val in enumerate(lst):        # spart den manuellen Zähler i = i + 1
    print(f"{i}: {val}")

for a, b in zip(list1, list2):       # zwei Listen parallel durchlaufen;
    pass                             # stoppt bei der KÜRZEREN Liste
```

### 15.5 `bytes` & Encoding

```python
data = "text".encode("utf-8")         # str -> bytes (fürs Netzwerk/Binärdatei)
sock.send((cmd + "\n").encode("utf-8"))   # erst zusammenbauen, dann kodieren

text = data.decode("utf-8")           # bytes -> str
text = data.decode(errors="replace")  # unbekannte Bytes werden ersetzt statt Absturz
```

### 15.6 Dict-Tricks

```python
d.get(key, default)               # Zugriff ohne KeyError
d.setdefault(key, [])             # Key mit Startwert anlegen, falls er fehlt
                                  # typisch: d.setdefault(k, []).append(v)
{**d1, **d2}                      # zusammenführen (bei gleichem Key gewinnt d2)
d1 | d2                           # dasselbe ab Python 3.9
{v: k for k, v in d.items()}      # invertieren (Werte müssen eindeutig sein!)
```

### 15.7 String-Formatierung auf einen Blick

```python
f"{n:2d}"      # Ganzzahl, Breite 2 (rechtsbündig)
f"{f:.2f}"     # Float mit 2 Nachkommastellen
f"{s:<20}"     # linksbündig, Breite 20
f"{s:>20}"     # rechtsbündig
f"{n:03d}"     # führende Nullen -> '003'
```

---

## 16. Schnellreferenz: Häufige Module

| Modul | Import | Zweck |
|---|---|---|
| `argparse` | `import argparse` | CLI-Argumente parsen |
| `socket` | `import socket` | TCP/UDP Netzwerk |
| `threading` | `import threading` | Nebenläufigkeit, Threads |
| `subprocess` | `import subprocess` | Shell-Befehle ausführen |
| `shlex` | `import shlex` | Command-String → Liste |
| `re` | `import re` | Reguläre Ausdrücke |
| `operator` | `import operator` | `itemgetter()` zum Sortieren |
| `textwrap` | `import textwrap` | `dedent()` für Multiline-Strings |
| `sys` | `import sys` | `sys.exit()`, `sys.argv` |
| `os` | `import os` | Pfade, Umgebungsvariablen |
| `pathlib` | `from pathlib import Path` | objektorientierte Pfade |
| `shutil` | `import shutil` | `which()`, Dateien kopieren |
| `datetime` | `import datetime` | Zeitstempel |
| `json` | `import json` | Serialisierung dict ↔ String/Datei |
| `collections` | `from collections import deque` | `deque` für Queues |
| `requests` | `import requests` | HTTP-Requests |
| `bs4` | `from bs4 import BeautifulSoup` | HTML-Parsing |
