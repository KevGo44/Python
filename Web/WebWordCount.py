# =============================================================================
# WEB WORD COUNT (WebWordCount.py)
# =============================================================================
#
# Funktion: Eine Webseite abrufen, den sichtbaren Text extrahieren und die
#           häufigsten Wörter zählen und ausgeben.
#
#   ┌───────────────────────────────────────────────────────────────┐
#   │                    Programmablauf                             │
#   │                                                               │
#   │  get_html_of()          -> HTML-Quelltext per HTTP laden      │
#   │  get_text_of_html()     -> HTML in Reintext umwandeln         │
#   │  list_of_words()        -> Text in Wortliste zerlegen         │
#   │  dict_word_count()      -> Häufigkeit jedes Wortes zählen     │
#   │  get_sorted_tupel_list()-> Nach Häufigkeit sortieren          │
#   │  count_words()          -> Alles orchestrieren, Top-5 ausgeben│
#   └───────────────────────────────────────────────────────────────┘
#
# VERWENDETE BIBLIOTHEKEN:
#   re          - Reguläre Ausdrücke (Standard-Lib): Wörter aus Text extrahieren
#   requests    - HTTP-Client (Drittanbieter): Webseiten abrufen
#   BeautifulSoup - HTML-Parser (Drittanbieter): HTML -> lesbarer Text
#
# BEISPIEL-AUSGABE für PAGE_URL = 'https://google.com':
#   Google -> 5
#   Search -> 3
#   ...

import re          # Standardbibliothek: Reguläre Ausdrücke für Textmuster-Suche
import requests    # Drittanbieter: HTTP-Requests senden (pip install requests)
from bs4 import BeautifulSoup  # Drittanbieter: HTML/XML parsen (pip install beautifulsoup4)

# Ziel-URL der zu analysierenden Webseite (hier leicht anpassbar als Konstante)
PAGE_URL = 'https://google.com'


def get_html_of(url):
    """
    Ruft den HTML-Quelltext einer URL per HTTP-GET ab.

    requests.get():
      - Sendet einen HTTP-GET-Request an die URL
      - Gibt ein Response-Objekt zurück
      - resp.status_code: HTTP-Statuscode (200=OK, 404=Not Found, 500=Server Error, ...)
      - resp.text: Antwort-Body als dekodierter String (HTML-Quelltext)

    Warum exit(1) bei Fehler?
      Alle folgenden Funktionen erwarten validen HTML-Text.
      Bei einem Fehler-Statuscode wäre der zurückgegebene Text eine Fehlerseite,
      was die Wortzählung verfälschen würde.
    """
    resp = requests.get(url)

    # Nur HTTP 200 (OK) ist ein erfolgreicher Seitenaufruf
    if resp.status_code != 200:
        print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')
        exit(1)  # exit(1) = Fehlercode: Programm mit Fehler beendet (exit(0) = Erfolg)

    return resp.text  # HTML-Quelltext als String zurückgeben


def get_text_of_html(html):
    """
    Extrahiert den sichtbaren Reintext aus einem HTML-Dokument.

    Warum BeautifulSoup statt einfachem String-Split?
      HTML enthält Tags (<div>, <script>, <style>, ...) die kein lesbarer Text sind.
      Ein einfaches Split würde "div" oder "class" als Wörter zählen.
      BeautifulSoup versteht die HTML-Struktur und gibt nur den sichtbaren Text zurück.

    BeautifulSoup(html, 'html.parser'):
      - html: Der rohe HTML-Quelltext als String
      - 'html.parser': Der eingebaute Python-HTML-Parser (kein Zusatzpaket nötig)
        Alternative: 'lxml' (schneller, aber extra Abhängigkeit)

    soup.get_text():
      - Gibt alle Text-Knoten des HTML-Baums als einen einzigen String zurück
      - Entfernt automatisch alle HTML-Tags
      - Ergebnis: "Google Suche Ich fühle mich heute glücklich ..."
    """
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()  # Nur den sichtbaren Text ohne HTML-Tags zurückgeben


def list_of_words(text):
    """
    Zerlegt einen Text in eine Liste einzelner Wörter.

    re.findall(r"\\w+", text):
      - \\w  = Wortzeichen: Buchstaben (a-z, A-Z), Ziffern (0-9) und Unterstrich (_)
      - +   = ein oder mehr solcher Zeichen hintereinander
      - Findet alle nicht-leeren Wortgruppen im Text
      - Gibt eine Liste aller Treffer zurück: ["Google", "Suche", "123", ...]

    Warum nicht text.split()?
      split() trennt nur an Leerzeichen. Satzzeichen wie "Wort," oder "Wort."
      würden als Bestandteil des Wortes gezählt. \\w+ ignoriert Satzzeichen automatisch.
    """
    return re.findall(r"\w+", text)  # Alle Wörter (alphanumerisch) aus dem Text extrahieren


def dict_word_count(wordlist):
    """
    Zählt, wie oft jedes Wort in der Liste vorkommt.

    Datenstruktur: Dictionary { Wort -> Anzahl }
      Beispiel: {"Google": 5, "Search": 3, "the": 12, ...}

    Ablauf für jedes Wort:
      1. Ist das Wort noch NICHT im Dict? -> Eintrag mit Zähler 1 anlegen
      2. Ist das Wort schon drin?         -> Zähler um 1 erhöhen

    Warum kein collections.Counter()?
      Counter(wordlist) würde dasselbe kürzer tun, aber diese manuelle Implementierung
      zeigt explizit die Logik hinter der Häufigkeitszählung.
    """
    worddict = {}  # Leeres Dictionary: wird mit {Wort: Anzahl} befüllt

    for word in wordlist:
        if word not in worddict:
            worddict[word] = 1         # Erstes Vorkommen: Zähler auf 1 setzen
        else:
            count = worddict.get(word) # Aktuellen Zählerstand abrufen
            worddict[word] = count + 1 # Zähler um 1 erhöhen

    return worddict


def get_sorted_tupel_list(worddict):
    """
    Sortiert das Wort-Häufigkeits-Dictionary nach Häufigkeit (absteigend).

    worddict.items():
      - Gibt alle Schlüssel-Wert-Paare als Liste von Tupeln zurück
      - Beispiel: [("Google", 5), ("the", 12), ("Search", 3)]

    sorted(..., key=lambda item: item[1], reverse=True):
      - key=lambda item: item[1]  -> Sortierkriterium: das zweite Element jedes Tupels (die Häufigkeit)
      - reverse=True              -> Absteigend: höchste Häufigkeit zuerst
      - Ergebnis: [("the", 12), ("Google", 5), ("Search", 3)]

    Rückgabe: Sortierte Liste von (Wort, Anzahl)-Tupeln
    """
    return sorted(worddict.items(), key=lambda item: item[1], reverse=True)


def count_words():
    """
    Orchestriert den gesamten Ablauf: URL abrufen -> Text extrahieren ->
    Wörter zählen -> Top-5 ausgeben.

    Ablauf:
      1. HTML-Quelltext der Ziel-URL laden
      2. Sichtbaren Text aus HTML extrahieren
      3. Text in Wortliste umwandeln
      4. Häufigkeit jedes Wortes zählen
      5. Nach Häufigkeit sortieren
      6. Die 5 häufigsten Wörter ausgeben

    min(5, len(sortedfinallist)):
      Verhindert einen IndexError, falls die Seite weniger als 5 Wörter enthält.
      Normalerweise liefert jede echte Webseite deutlich mehr als 5 Wörter.
    """
    html = get_html_of(PAGE_URL)                    # Schritt 1: HTML laden
    text = get_text_of_html(html)                   # Schritt 2: Text extrahieren
    wordlist = list_of_words(text)                  # Schritt 3: In Wörter zerlegen
    worddict = dict_word_count(wordlist)            # Schritt 4: Häufigkeit zählen
    sortedfinallist = get_sorted_tupel_list(worddict)  # Schritt 5: Sortieren

    # Schritt 6: Top-5 ausgeben
    # enumerate() gibt Index + Wert zurück: (0, ("the", 12)), (1, ("Google", 5)), ...
    for index, word in enumerate(sortedfinallist):
        if index >= min(5, len(sortedfinallist)):  # Nach 5 Einträgen abbrechen
            break
        # word[0] = Wortstring, word[1] = Häufigkeit
        print(word[0], "->", word[1])


# Einstiegspunkt: Wird nur ausgeführt wenn Skript direkt gestartet wird,
# nicht wenn es als Modul importiert wird (import WebWordCount)
count_words()