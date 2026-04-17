# =============================================================================
# KRYPTOANALYSE V2 (KryptoanalyseV2.py)
# =============================================================================
#
# Interaktives Werkzeug zur Analyse und Entschlüsselung klassischer Chiffren.
#
#   ┌─────────────────────────────────────────────────────────────────────┐
#   │                        Programmstruktur                             │
#   │                                                                     │
#   │  VERSCHLÜSSELUNG                                                    │
#   │    caesar()            -> Cäsar-Verschlüsselung (Verschiebechiffre) │
#   │    de_caesar()         -> Cäsar-Entschlüsselung                     │
#   │    caesarbruteforce()  -> Alle 26 Verschiebungen ausgeben           │
#   │    vigenere()          -> Vigenère-Verschlüsselung                  │
#   │    de_vigenere()       -> Vigenère-Entschlüsselung                  │
#   │                                                                     │
#   │  ANALYSE                                                            │
#   │    absoluteHaeufigkeiten() -> Buchstaben-Zählungen                  │
#   │    relativeHaeufigkeiten() -> Buchstaben-Häufigkeiten in %          │
#   │    ngram()             -> n-Gramm-Häufigkeiten in %                 │
#   │    analyse()           -> Relative + Bi-/Trigramm-Ausgabe           │
#   │    sprache()           -> Koinzidenzindex berechnen                 │
#   │    info()              -> Referenzwerte Englisch / Deutsch          │
#   │                                                                     │
#   │  SUBSTITUTION                                                       │
#   │    multirep()          -> Mehrfachersetzung auf Text anwenden       │
#   │    ersetze_menu()      -> Interaktives Substitutionsmenü            │
#   └─────────────────────────────────────────────────────────────────────┘
#
# BEFEHLE (Hauptmenü):
#   neu          -> Neue Chiffre eingeben
#   chiffre      -> Aktuelle Chiffre anzeigen
#   analyse [n]  -> Häufigkeitsanalyse (optional: Top-n-Einträge)
#   sprache      -> Koinzidenzindex berechnen
#   info         -> Referenztabellen Englisch/Deutsch anzeigen
#   multirep     -> Substitutionsmenü öffnen
#   caesar       -> Cäsar-Brute-Force (alle 26 Schlüssel)
#   help         -> Hilfe anzeigen
#   exit         -> Programm beenden
# =============================================================================

import operator

# Unveränderliches Referenz-Alphabet (nur Großbuchstaben A–Z)
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# =============================================================================
# VERSCHLÜSSELUNG
# =============================================================================

def caesar(klartext, key):
    """
    Cäsar-Verschlüsselung: Verschiebt jeden Buchstaben um 'key' Positionen.

    key: Verschiebung 0–25 (modulo 26 → bleibt automatisch im gültigen Bereich)
    Nicht-Buchstaben (Leerzeichen, Zahlen, Satzzeichen) werden unverändert übernommen.
    """
    klartext = klartext.upper()
    chiffre = ""
    for buchstabe in klartext:
        if buchstabe in ALPHABET:
            index = ALPHABET.index(buchstabe)
            chiffre += ALPHABET[(index + key) % 26]
        else:
            chiffre += buchstabe  # Sonderzeichen/Leerzeichen beibehalten, nicht abbrechen
    return chiffre

def de_caesar(chiffre, key):
    """Cäsar-Entschlüsselung: Umkehrung durch Verschiebung um (26 - key)."""
    return caesar(chiffre, 26 - key)

def caesarbruteforce(text):
    """Gibt alle 26 möglichen Cäsar-Entschlüsselungen nummeriert aus."""
    for i in range(len(ALPHABET)):
        print(f"  {i:2d}: {de_caesar(text, i)}")

def vigenere(klartext, password):
    """
    Vigenère-Verschlüsselung: Polyalphabetische Substitution mit Schlüsselwort.

    Der Schlüssel wird zyklisch wiederholt. Der Schlüsselindex rückt nur
    bei Alphabet-Zeichen vor, damit Sonder-/Leerzeichen die Schlüsselposition
    nicht verschieben.
    """
    klartext = klartext.upper()
    password = password.upper()
    if not password:
        return klartext
    chiffre = ""
    key_index = 0  # separater Zähler – Nicht-Buchstaben verschieben den Schlüssel nicht
    for buchstabe in klartext:
        if buchstabe in ALPHABET:
            key_shift = ALPHABET.index(password[key_index % len(password)])
            chiffre += caesar(buchstabe, key_shift)
            key_index += 1
        else:
            chiffre += buchstabe
    return chiffre

def de_vigenere(chiffre, password):
    """Vigenère-Entschlüsselung: Umkehrung durch negative Schlüsselverschiebung."""
    chiffre = chiffre.upper()
    password = password.upper()
    if not password:
        return chiffre
    klartext = ""
    key_index = 0
    for buchstabe in chiffre:
        if buchstabe in ALPHABET:
            key_shift = ALPHABET.index(password[key_index % len(password)])
            klartext += de_caesar(buchstabe, key_shift)
            key_index += 1
        else:
            klartext += buchstabe
    return klartext


# =============================================================================
# HÄUFIGKEITSANALYSE
# =============================================================================

def absoluteHaeufigkeiten(text):
    """Zählt absolute Häufigkeiten jedes Zeichens im Text."""
    h = {}
    for b in text:
        h[b] = h.get(b, 0) + 1
    return h

def relativeHaeufigkeiten(text):
    """Berechnet relative Häufigkeiten (%) jedes Zeichens im Text."""
    if not text:
        return {}
    h = absoluteHaeufigkeiten(text)
    return {k: v / len(text) * 100 for k, v in h.items()}

def ngram(text, n):
    """
    Berechnet relative Häufigkeiten (%) aller überlappenden n-Gramme im Text.

    Für jeden Startversatz delta (0..n-1) werden nicht-überlappende Fenster
    der Breite n extrahiert. Alle Versätze zusammen erfassen jeden überlappenden
    n-Gramm-Kandidaten genau einmal.
    """
    ngrams = {}
    total = 0
    for delta in range(n):
        for i in range(0, len(text), n):
            teil = text[delta + i : delta + i + n]
            if len(teil) == n:
                total += 1
                ngrams[teil] = ngrams.get(teil, 0) + 1
    if total == 0:
        return {}
    return {k: v / total * 100 for k, v in ngrams.items()}

def analyse(chiffre, anzahl):
    """
    Gibt sortierte Häufigkeitstabellen aus: Einzelzeichen, Bigramme, Trigramme.

    anzahl: Anzahl der auszugebenden Top-Einträge (0 = alle ausgeben)
    """
    def _print_top(label, freq_dict, n):
        """Sortiert absteigend und gibt die ersten n Einträge formatiert aus."""
        sorted_items = sorted(freq_dict.items(), key=operator.itemgetter(1), reverse=True)
        limit = n if n > 0 else len(sorted_items)
        print(f"\n{label}:")
        for i, item in enumerate(sorted_items[:limit]):
            print(f"  {i:3d}: {item[0]}  {item[1]:.2f}%")

    _print_top("Relative Häufigkeiten", relativeHaeufigkeiten(chiffre), anzahl)
    _print_top("Bigramme", ngram(chiffre, 2), anzahl)
    _print_top("Trigramme", ngram(chiffre, 3), anzahl)

def sprache(chiffre):
    """
    Berechnet den Koinzidenzindex (IC / Index of Coincidence) des Textes.

    IC = Σ(ni * (ni-1)) / (n * (n-1))

    Richtwerte:
      Zufällig (gleichverteilt): IC ≈ 0.0385
      Englisch:                  IC ≈ 0.0667
      Deutsch:                   IC ≈ 0.0762
    """
    n = len(chiffre)
    if n < 2:
        return 0.0
    h = absoluteHaeufigkeiten(chiffre)
    zaehler = sum(ni * (ni - 1) for ni in h.values())  # Summe zuerst, dann einmalig dividieren
    return zaehler / (n * (n - 1))


# =============================================================================
# SUBSTITUTION (manuelle Zeichenersetzung)
# =============================================================================

def multirep(text, remove, new):
    """
    Wendet mehrere Zeichenersetzungen sequenziell auf den Text an.

    remove[i] wird durch new[i] ersetzt. Reihenfolge beachten: spätere
    Ersetzungen können frühere Ergebnisse überschreiben.
    """
    ergebnis = text
    for i in range(len(remove)):
        ergebnis = ergebnis.replace(remove[i], new[i])
    return ergebnis

def ersetze_menu(chiffre):
    """
    Interaktives Substitutionsmenü zur manuellen Häufigkeitsanalyse.

    Befehle:
      add A,B   -> Ersetzung hinzufügen: A wird durch B ersetzt
      remove n  -> Ersetzung Nr. n aus der Liste entfernen
      liste     -> Alle definierten Ersetzungen anzeigen
      ersetzen  -> Alle Ersetzungen auf die Chiffre anwenden
      text      -> Aktuellen (ersetzten) Text anzeigen
      clear     -> Alle Ersetzungen löschen
      back      -> Menü verlassen
    """
    remove = []  # Original-Zeichen (werden ersetzt)
    new = []     # Ziel-Zeichen (ersetzen durch)
    text = chiffre

    print("  Substitutionsmenü | 'help' für Befehle")

    while True:
        command = input("  ersetzungen>>> ").strip().lower().split()
        if not command:
            continue

        cmd = command[0]

        if cmd == "back":
            break

        elif cmd == "help":
            print("  add A,B | remove n | liste | ersetzen | text | clear | back")

        elif cmd == "text":
            print(f"  {text}")

        elif cmd == "add":
            # Syntax: add A,B [C,D ...]  (mehrere Paare pro Befehl möglich)
            try:
                for token in command[1:]:
                    parts = token.split(",")
                    if len(parts) != 2:
                        raise ValueError("Kein Komma-Trennzeichen gefunden")
                    remove.append(parts[0].upper())
                    new.append(parts[1])
                    print(f"  Hinzugefügt: {parts[0].upper()} -> {parts[1]}")
            except (ValueError, IndexError):
                print("  Syntax-Fehler. Beispiel: add A,E")

        elif cmd == "remove":
            try:
                idx = int(command[1])
                print(f"  Entfernt: {remove[idx]} -> {new[idx]}")
                remove.pop(idx)  # pop(index) statt remove(value) – verhindert falsches Löschen bei Duplikaten
                new.pop(idx)
            except (IndexError, ValueError):
                print("  Ungültiger Index.")

        elif cmd == "liste":
            if not remove:
                print("  (keine Ersetzungen definiert)")
            else:
                for i in range(len(remove)):
                    print(f"  {i}: {remove[i]} --> {new[i]}")

        elif cmd == "ersetzen":
            text = multirep(chiffre, remove, new)
            print("  Ersetzungen angewendet.")

        elif cmd == "clear":
            remove.clear()
            new.clear()
            text = chiffre
            print("  Liste geleert.")

        else:
            print(f"  Unbekannter Befehl: '{cmd}'. 'help' für Hilfe.")


# =============================================================================
# REFERENZTABELLEN (Englisch / Deutsch)
# =============================================================================

def info():
    """Zeigt statistische Referenzwerte für englische und deutsche Texte."""
    print(
        "=" * 67 + "\n"
        "REFERENZWERTE\n"
        "=" * 67 + "\n"
        "Alphabet: A-B-C-D-E-F-G-H-I-J-K-L-M-N-O-P-Q-R-S-T-U-V-W-X-Y-Z\n"
        "IC (Zufall / gleichverteilt): 0.0385\n"
        "\n"
        "ENGLISCH  (IC ~ 0.0667)\n"
        "-" * 67 + "\n"
        "E:11.0  I:8.6  A:7.8  O:6.1  U:3.3  Y:1.6\n"
        "\n"
        "Bigramme:\n"
        "  th:3.56  he:3.07  in:2.43  er:2.05  an:1.99  re:1.85\n"
        "  on:1.76  at:1.49  en:1.45  nd:1.35  ti:1.34  es:1.34\n"
        "  or:1.28  te:1.20  of:1.17  ed:1.17  is:1.13  it:1.12\n"
        "  al:1.09  ar:1.07  st:1.05  to:1.05  nt:1.04  ng:0.95\n"
        "\n"
        "Trigramme:\n"
        "  the:3.508  and:1.594  ing:1.147  her:0.822  hat:0.651\n"
        "  his:0.597  tha:0.594  ere:0.561  for:0.555  ent:0.531\n"
        "  ion:0.506  ter:0.461  was:0.460  you:0.437  ith:0.431\n"
        "\n"
        "DEUTSCH  (IC ~ 0.0762)\n"
        "-" * 67 + "\n"
        "E:16.93  N:10.53  I:8.02  R:6.89  S:6.42  T:5.79\n"
        "A:5.58   D:4.98   H:4.98  U:3.83  L:3.60\n"
        "\n"
        "Bigramme:\n"
        "  ER:3.90  EN:3.61  CH:2.36  DE:2.31  EI:1.98  TE:1.98\n"
        "  IN:1.71  ND:1.68  IE:1.48  GE:1.45  ST:1.21  NE:1.19\n"
        "  BE:1.17  ES:1.17  UN:1.13  RE:1.11  AN:1.07  HE:0.89\n"
        "\n"
        "Trigramme:\n"
        "  DER:1.04  EIN:0.83  SCH:0.76  ICH:0.75  NDE:0.72\n"
        "  DIE:0.62  CHE:0.58  DEN:0.56  TEN:0.51  UND:0.48\n"
        "  INE:0.48  TER:0.44  GEN:0.44  END:0.44  ERS:0.42\n"
        + "=" * 67
    )


# =============================================================================
# DEMO-DURCHLAUF
# =============================================================================

def demo():
    """
    Simuliert einen Analyse-Durchlauf fuer eine monoalphabetische Substitutionschiffre.
    Im Gegensatz zu Caesar ist Brute-Force ausgeschlossen (26! ~ 4e26 Schlussel).
    Ansatz: IC -> Haeufigkeitsanalyse -> Mustererkennung -> schrittweise Substitution.
    Jeder Schritt zeigt den Befehl und die Ausgabe; der Ablauf ist manuell reproduzierbar.
    """
    SEP  = "-" * 67
    SEP2 = "=" * 67

    # Konsistente monoalphabetische Substitution (plain -> cipher).
    # Alle 26 Buchstaben sind eindeutig zugeordnet (Permutation des Alphabets).
    _ENC = {
        'A':'C','B':'D','C':'H','D':'F','E':'L','F':'V','G':'G','H':'J',
        'I':'K','J':'R','K':'I','L':'O','M':'X','N':'Q','O':'A','P':'P',
        'Q':'E','R':'B','S':'U','T':'Z','U':'S','V':'T','W':'W','X':'Y',
        'Y':'N','Z':'M'
    }
    _DEC = {v: k for k, v in _ENC.items()}  # cipher -> plain (fuer direkte Entschluesselung)

    demo_plain  = "DIESES PROGRAMM DEMONSTRIERT WIE EINE MONOALPHABETISCHE SUBSTITUTION IN PYTHON GEBROCHEN WERDEN KANN"
    demo_cipher = ''.join(_ENC.get(c, c) for c in demo_plain)
    cipher_clean = ''.join(c for c in demo_cipher if c.isalpha())

    def _partial(text, mapping):
        """Single-pass Substitution: jedes Zeichen wird genau einmal ersetzt."""
        return ''.join(mapping.get(c, c) for c in text)

    def _partial_vis(text, mapping):
        """Wie _partial, aber ersetzte Zeichen erscheinen klein (noch unbekannte gross).
        Entspricht der multirep-Konvention: add L,e -> ersetzte Zeichen sichtbar markiert."""
        result = []
        for c in text:
            if c in mapping:
                result.append(mapping[c].lower())
            else:
                result.append(c)
        return ''.join(result)

    print(f"\n{SEP2}")
    print("  DEMO - Monoalphabetische Substitution: Analyse-Durchlauf")
    print(SEP2)
    print("\n  Ausgangssituation: Folgender Text wurde abgefangen:\n")
    print(f"    {demo_cipher}\n")
    print("  Ziel: Klartext ohne Kenntnis des Geheimalphabets wiederherstellen.")
    print("  Wichtig: 26! ~ 4 x 10^26 Schluessel -> Brute-Force nicht moeglich.")
    print("  Ansatz: IC + Haeufigkeitsanalyse + Mustererkennung\n")

    # -------------------------------------------------------------------------
    # SCHRITT 1: Koinzidenzindex
    # -------------------------------------------------------------------------
    print(SEP)
    print("  SCHRITT 1 - Chiffrentyp bestimmen          Befehl: sprache")
    print(SEP)
    ic = sprache(cipher_clean)
    print(f"\n  >>> sprache")
    print(f"  Koinzidenzindex: {ic:.6f}\n")
    print("  Richtwerte:")
    print("    ~0.0385  Zufall / Vigenere mit sehr langem Schluessel")
    print("    ~0.0667  Englischer Klartext  (monoalphabetisch)")
    print("    ~0.0762  Deutscher Klartext   (monoalphabetisch)")
    if ic > 0.060:
        print(f"\n  -> IC = {ic:.4f} liegt nahe am Sprachtext-Wert.")
        print("     Fazit: monoalphabetische Substitution (Caesar oder Geheimalphabet).")
        print("     Naechster Schritt: Haeufigkeitsanalyse, da Brute-Force nicht praktikabel.")

    # -------------------------------------------------------------------------
    # SCHRITT 2: Haeufigkeitsanalyse
    # -------------------------------------------------------------------------
    print(f"\n{SEP}")
    print("  SCHRITT 2 - Haeufigkeitsanalyse            Befehl: analyse 8")
    print(SEP)
    print("\n  >>> analyse 8\n")
    rel = relativeHaeufigkeiten(cipher_clean)
    sorted_rel = sorted(rel.items(), key=operator.itemgetter(1), reverse=True)
    print("  Relative Haeufigkeiten (Top 8):")
    for i, (char, pct) in enumerate(sorted_rel[:8]):
        print(f"    {i:2d}: {char}   {pct:.2f}%")
    top = sorted_rel[0]
    print(f"\n  Vergleich mit deutschem Referenztext (Befehl: info):")
    print(f"    E:16.93%  N:10.53%  I:8.02%  R:6.89%  S:6.42%")
    print(f"\n  -> '{top[0]}' ist haeufigster Buchstabe ({top[1]:.1f}%) -> Kandidat fuer 'E'")
    print(f"     Hinweis: Einzelne Zuordnung noch unsicher, wird durch Mustererkennung bestaetigt.")

    # -------------------------------------------------------------------------
    # SCHRITT 3: Mustererkennung in kurzen Woertern
    # -------------------------------------------------------------------------
    print(f"\n{SEP}")
    print("  SCHRITT 3 - Mustererkennung (kurze Woerter)")
    print(SEP)
    words = demo_cipher.split()
    w2 = [w for w in words if len(w) == 2][0]
    w3 = [w for w in words if len(w) == 3][0]
    w4_sym = [w for w in words if len(w) == 4 and w[0] == w[3]][0]

    print(f"\n  Auffaellige kurze Woerter im Chiffretext:")
    print(f"    '{w2}'     (2 Zeichen)  -> Deutsche 2-Buchstaben-Woerter: IN, IM, AN, AM, ...")
    print(f"    '{w3}'    (3 Zeichen)  -> beginnt mit letztem Zeichen aus '{w2}': WIE, WIR, ...")
    print(f"    '{w4_sym}'  (4 Zeichen)  -> 1. und 4. Zeichen identisch ({w4_sym[0]}..{w4_sym[3]}): EINE, EBEN, ...")
    print(f"\n  Hypothese aufstellen:")
    print(f"    '{w4_sym}' = EINE  ->  {w4_sym[0]}=E, {w4_sym[1]}=I, {w4_sym[2]}=N")
    print(f"    '{w2}'   = IN    ->  {w2[0]}=I, {w2[1]}=N  (bestaetigt: passt zu EINE)")
    print(f"    '{w3}'  = WIE   ->  {w3[0]}=W, {w3[1]}=I, {w3[2]}=E  (bestaetigt)")
    print(f"\n  Erkannte Zuordnungen bisher: {w4_sym[0]}=E  {w4_sym[1]}=I  {w4_sym[2]}=N  {w3[0]}=W")

    # -------------------------------------------------------------------------
    # SCHRITT 4: Erste Ersetzungen
    # -------------------------------------------------------------------------
    print(f"\n{SEP}")
    print("  SCHRITT 4 - Erste Ersetzungen anwenden      Befehl: multirep")
    print(SEP)
    map4 = {w4_sym[0]: 'E', w4_sym[1]: 'I', w4_sym[2]: 'N', w3[0]: 'W'}
    print(f"\n  Im Substitutionsmenue (multirep) eingeben:")
    for c, p in map4.items():
        print(f"    >>> add {c},{p}")
    print(f"    >>> ersetzen")
    print(f"    >>> text\n")
    text4 = _partial_vis(demo_cipher, map4)
    print(f"  Ergebnis nach Schritt 4:")
    print(f"    {text4}\n")
    # Deduce F=D, U=S from first word
    w0_after4 = _partial_vis(words[0], map4)
    print(f"  Analyse des ersten Wortes '{words[0]}' -> '{w0_after4}':")
    print(f"    Muster _IE_E_ mit Pos 1=I, 3=E -> DIESES: {words[0][0]}=D, {words[0][3]}=S")
    w1_after4 = _partial_vis(words[1], map4)
    print(f"\n  Analyse von '{words[1]}' -> '{w1_after4}':")
    print(f"    8 Zeichen, Pos 6=7 (Doppelbuchstabe) -> PROGRAMM: {words[1][1]}=R, {words[1][2]}=O, {words[1][5]}=A, {words[1][6]}=M")

    # -------------------------------------------------------------------------
    # SCHRITT 5: Erweitertes Mapping (die 11 vom Benutzer vorgegebenen)
    # -------------------------------------------------------------------------
    print(f"\n{SEP}")
    print("  SCHRITT 5 - Mapping erweitern               Befehl: multirep")
    print(SEP)
    map5 = {'L':'E','K':'I','Q':'N','W':'W','F':'D','U':'S','A':'O','B':'R','C':'A','X':'M','Z':'T','J':'H'}
    new5 = {k: v for k, v in map5.items() if k not in map4}
    print(f"\n  Weitere Ersetzungen hinzufuegen:")
    for c, p in new5.items():
        print(f"    >>> add {c},{p}")
    print(f"    >>> ersetzen\n")
    text5 = _partial_vis(demo_cipher, map5)
    print(f"  Ergebnis nach Schritt 5:")
    print(f"    {text5}\n")
    print(f"  Erkennbare Restluecken: G, P, O, S, N, D, H, I")
    print(f"  Aus Kontext:")
    python_word = next(w for w in words if w[0] == 'P' and len(w) == 6)
    print(f"    '{_partial_vis(python_word, map5)}' -> PYTHON: P=P, O->L (aus MONO...LPHABETISCHE ableitbar)")
    w_kann_after5 = _partial_vis(words[-1], map5)
    print(f"    '{words[-1]}' -> '{w_kann_after5}' -> KANN: {words[-1][0]}=K")
    print(f"    'GEBROCHEN': G=G erkennbar, O->L, D->B, H->C")

    # -------------------------------------------------------------------------
    # SCHRITT 6: Vollstaendige Entschluesselung
    # -------------------------------------------------------------------------
    print(f"\n{SEP}")
    print("  SCHRITT 6 - Vollstaendige Entschluesselung")
    print(SEP)
    final = _partial(demo_cipher, _DEC)
    print(f"\n  Klartext: {final}")
    print(f"\n  Vollstaendiges Mapping (Chiffre -> Klartext):")
    pairs = sorted(_DEC.items())
    row = "    "
    for i, (c, p) in enumerate(pairs):
        row += f"{c}={p}  "
        if (i + 1) % 9 == 0:
            print(row.rstrip())
            row = "    "
    if row.strip():
        print(row.rstrip())

    # -------------------------------------------------------------------------
    # REPRODUZIEREN
    # -------------------------------------------------------------------------
    print(f"\n  -- Zum manuellen Reproduzieren ----------------------------------")
    print(f"  >>> neu")
    print(f"       {demo_cipher}")
    print(f"  >>> sprache        IC pruefen -> monoalphabetisch (~0.07)")
    print(f"  >>> analyse 8      Haeufigkeiten mit 'info' vergleichen")
    print(f"  >>> multirep       Schrittweise: add L,E  add K,I  add Q,N  ...")
    print(f"  Hinweis: Bei multirep koennen sich Ersetzungen gegenseitig beeinflussen.")
    print(f"           Sicherer: alle add-Befehle erst eingeben, dann einmal 'ersetzen'.")
    print(f"{SEP2}\n")


# =============================================================================
# HILFE / HAUPTMENÜ
# =============================================================================

def show_help():
    """Zeigt eine strukturierte Befehlsuebersicht im klassischen Format."""
    W = 67
    print(f"\n{'=' * W}")
    print("  KRYPTOANALYSE v2  -  Befehlsuebersicht")
    print(f"{'=' * W}")
    print(f"  {'Befehl':<22} {'Argumente':<14} Beschreibung")
    print(f"  {'-' * 21} {'-' * 13} {'-' * 27}")
    rows = [
        ("CHIFFRE", "", ""),
        ("  neu",        "",             "Neue Chiffre eingeben (ueberschreibt aktuelle)"),
        ("  chiffre",    "",             "Aktuelle Chiffre anzeigen (oder neu einlesen)"),
        ("", "", ""),
        ("ANALYSE", "", ""),
        ("  analyse",    "[n]",          "Haeufigkeiten: Zeichen, Bigramme, Trigramme"),
        ("",             "",             "  n = Top-n-Eintraege (Standard: alle)"),
        ("  sprache",    "",             "Koinzidenzindex (IC) berechnen"),
        ("  info",       "",             "Statistische Referenzwerte EN/DE anzeigen"),
        ("", "", ""),
        ("KRYPTOGRAPHIE", "", ""),
        ("  caesar",     "",             "Caesar Brute-Force: alle 26 Schluessel testen"),
        ("  vigenere",   "<schluessel>", "Vigenere-Verschluesselung mit Schluesselwort"),
        ("  devigenere", "<schluessel>", "Vigenere-Entschluesselung mit Schluesselwort"),
        ("", "", ""),
        ("SUBSTITUTION", "", ""),
        ("  multirep",   "",             "Manuelles Substitutionsmenue oeffnen"),
        ("", "", ""),
        ("SONSTIGES", "", ""),
        ("  demo",       "",             "Kompletten Analyse-Durchlauf demonstrieren"),
        ("  help",       "",             "Diese Hilfe anzeigen"),
        ("  exit",       "",             "Programm beenden"),
    ]
    for cmd, args, desc in rows:
        if cmd == "" and args == "" and desc == "":
            continue  # Leerzeilen-Trenner überspringen (der \n in der Abschnittsüberschrift reicht)
        elif desc == "" and args == "":
            print(f"\n  {cmd}")
        else:
            print(f"  {cmd:<22} {args:<14} {desc}")
    print(f"\n{'=' * W}\n")


if __name__ == "__main__":
    print("Kryptoanalyse v2  -  Programmiert von Kevin Kuester")
    print("  --> 'help' für Befehlsübersicht\n")

    chiffre = ""  # aktive Chiffre; leer bis 'neu' oder 'chiffre' gesetzt wird

    while True:
        raw = input(">>> ").strip()
        if not raw:
            continue

        parts = raw.lower().split()
        cmd = parts[0]

        # ── Chiffre verwalten ────────────────────────────────────────────────
        if cmd == "neu":
            chiffre = input("  Neue Chiffre: ").upper()
            print(f"  Chiffre gesetzt ({len(chiffre)} Zeichen).")

        elif cmd == "chiffre":
            if chiffre:
                print(f"  {chiffre}")
            else:
                chiffre = input("  Chiffre eingeben: ").upper()

        elif cmd == "exit":
            break

        # ── Analyse ──────────────────────────────────────────────────────────
        elif cmd == "analyse":
            if not chiffre:
                chiffre = input("  Chiffre eingeben: ").upper()
            try:
                anzahl = int(parts[1]) if len(parts) > 1 else 0
            except ValueError:
                anzahl = 0
            analyse(chiffre, anzahl)

        elif cmd == "sprache":
            if not chiffre:
                chiffre = input("  Chiffre eingeben: ").upper()
            print(f"  Koinzidenzindex: {sprache(chiffre):.6f}")

        elif cmd == "info":
            info()

        # ── Substitution ─────────────────────────────────────────────────────
        elif cmd == "multirep":
            if not chiffre:
                chiffre = input("  Chiffre eingeben: ").upper()
            ersetze_menu(chiffre)

        # ── Kryptographie ────────────────────────────────────────────────────
        elif cmd == "caesar":
            if not chiffre:
                chiffre = input("  Chiffre eingeben: ").upper()
            caesarbruteforce(chiffre)

        elif cmd == "vigenere":
            if len(parts) < 2:
                print("  Syntax: vigenere <schlüssel>")
            else:
                key = parts[1].upper()
                if not chiffre:
                    chiffre = input("  Chiffre eingeben: ").upper()
                result = vigenere(chiffre, key)
                print(f"  Verschlüsselt: {result}")

        elif cmd == "devigenere":
            if len(parts) < 2:
                print("  Syntax: devigenere <schlüssel>")
            else:
                key = parts[1].upper()
                if not chiffre:
                    chiffre = input("  Chiffre eingeben: ").upper()
                result = de_vigenere(chiffre, key)
                print(f"  Entschlüsselt: {result}")

        # ── Sonstiges ────────────────────────────────────────────────────────
        elif cmd == "demo":
            demo()

        elif cmd == "help":
            show_help()

        else:
            print(f"  Unbekannter Befehl: '{cmd}'. 'help' für Hilfe.")
