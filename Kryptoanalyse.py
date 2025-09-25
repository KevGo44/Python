#Imports
import operator



#Ersetzngen
def ersetzungen_liste_remove(new, remove, tmp):
    b = new[tmp]
    new.remove(b)
    b = remove[tmp]
    remove.remove(b)

def ersetzungen_liste_clear(new, remove):
    new.clear()
    remove.clear()

def ersetze_print_list(new, remove):
    for i in range(len(new)):
        print(str(i) + ": " + str(remove[i]) + " --> " + str(new[i]))

def multirep(text, new, remove):
    ersetzt = text
    for i in range(len(new)):
        ersetzt = ersetzt.replace(remove[i], new[i])
    return ersetzt

def ersetzungen_help():
    print("\'help\'", "\'back\'", "\'liste\'", "\'clear\'", "\'add charI,charII\'", "\'remove int\'", "\'ersetzen\'", "\'text\'")

Commands_Ersetzungen = {
    'help': ersetzungen_help,
    'remove': ersetzungen_liste_remove,
    'clear': ersetzungen_liste_clear,
    'liste': ersetze_print_list,
    'ersetzen': multirep
}

def ersetze_menu(chiffre):
    remove = []
    new = []
    text = ""
    while True:
        command = input("ersetzungen>>>").lower().split(" ")
        
        if command[0] == "back":
            break
        if command[0] == "text":
            print(text)
        if command[0] == "add":
            try:
                for i in range(1, len(command)):
                    replace = command[i].split(",")
                    remove.append(replace[0].upper())
                    new.append(replace[1])
                    print("Aenderung hinzugefuegt")
            except IndexError:
                print("Snytax: \'add charI,charII\'")

        if command[0] in Commands_Ersetzungen:
            if Commands_Ersetzungen[command[0]] == Commands_Ersetzungen['help']:
               ersetzungen_help()
            elif Commands_Ersetzungen[command[0]] == Commands_Ersetzungen['remove']:
                try:
                    tmp = int(command[1])
                except IndexError:
                    print("error")
                try:
                    ersetzungen_liste_remove(new, remove, tmp)
                    print(str(tmp) + " entfernt")
                except IndexError:
                    print("error")
            elif Commands_Ersetzungen[command[0]] == Commands_Ersetzungen['clear']:
                ersetzungen_liste_clear(new, remove)
                print("liste geleert")
            elif Commands_Ersetzungen[command[0]] == Commands_Ersetzungen['liste']:
                ersetze_print_list(new, remove)
            elif Commands_Ersetzungen[command[0]] == Commands_Ersetzungen['ersetzen']:
                text = multirep(chiffre, new, remove)
                print("Ersetungen durchgeführt")



#Verschlüsselung
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#Cäsar
def caesar(klartext, key):
    klartext = klartext.upper()
    chiffre = ""
    for buchstabe in klartext:
        indexInAlphabet = alphabet.index(buchstabe)
        zielIndex = (indexInAlphabet + key) % 26
        chiffreZeichen = alphabet[zielIndex]
        chiffre = chiffre + chiffreZeichen
    return chiffre
    
def de_caesar(chiffre, key):
    return caesar(chiffre, 26 - key)

def caesarbruteforce(text):
    for i in range(len(alphabet)):
        print(str(i) + " : " + caesar(text, i))

#Vigenere
def vigenere(klartext, password):
    klartext = klartext.upper()
    password = password.upper()
    chiffre = ""
    for index, b in enumerate(klartext):
        tmp = index % len(password)
        keyASCII = password[tmp]
        keyInt = ord(keyASCII) - ord('A')
        chiffre += caesar(b, keyInt)
    return chiffre

def de_vigenere(klartext, password):
    klartext = klartext.upper()
    password = password.upper()
    chiffre = ""
    for index, b in enumerate(klartext):
        tmp = index % len(password)
        keyASCII = password[tmp]
        keyInt = ord(keyASCII) - ord('A')
        chiffre += de_caesar(b, keyInt)
    return chiffre



#Anaylse
def absoluteHaeufigkeiten(text):
    h = dict()
    for b in text:
        if b in h:
            h[b] += 1
        else:
            h[b] = 1
    return h

def relativeHaeufigkeiten(text):
    h = absoluteHaeufigkeiten(text)
    r = dict()
    for k in h.keys():
        r[k] = h[k] / len(text) * 100
    return r

def ngram(text, n):
    ntuplesTotal = 0
    ngrams = dict()
    for delta in range(n):
        for i in range(0, len(text), n):
            teil = text[delta+i : delta+i+n]
            if len(teil) == n:
                ntuplesTotal += 1
                if teil in ngrams:
                    ngrams[teil] += 1
                else:
                    ngrams[teil] = 1
    for key in ngrams:
        ngrams[key] = ngrams[key] / ntuplesTotal * 100
    return ngrams

def analyse(chiffre, anzahl):
    #relativ
    r = relativeHaeufigkeiten(chiffre)
    s = sorted(r.items(), key=operator.itemgetter(1), reverse=True)
    print("relative Haeufigkeiten:")
    tmp = list(s)
    for i, b in enumerate(s):
        print(str(i) +": "+ str(tmp[i]))
    #bigram
    r = ngram(chiffre, 2)
    s = sorted(r.items(), key=operator.itemgetter(1), reverse=True)
    print("\n" + "bigrams:")
    tmp = list(s)
    if anzahl == 0:
        anzahl = len(tmp)
    try:
        for i in range(int(anzahl)):
            print(str(i) +": "+ str(tmp[i]))
    except IndexError:
        pass
    #trigram
    r = ngram(chiffre, 3)
    s = sorted(r.items(), key=operator.itemgetter(1), reverse=True)
    print("\n" + "trigrams:")
    tmp = list(s)
    if anzahl == 0:
        anzahl = len(tmp)
    try:
        for i in range(int(anzahl)):
            print(str(i) +": "+ str(tmp[i]))
    except IndexError:
        pass

def info():
    print("----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----" + "\n" +
        "Info" + "\n" +
        "----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----" + "\n" +
        "Alphabet:" + "\n" +
        "A-B-C-D-E-F-G-H-I-J-K-L-M-N-O-P-Q-R-S-T-U-V-W-X-Y-Z" + "\n" +
        "Ic = 0.0385" + "\n"
        "----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----" + "\n" +
        "English, id: 0.067" + "\n" +
        "E : 11" + "\n" +
        "I : 8.6" + "\n" +
        "A : 7.8" + "\n" +
        "O : 6.1" + "\n" +
        "U : 3.3" + "\n" +
        "Y : 1.6" + "\n" +
        "\n" +
        "th : 3.56    of : 1.17    io : 0.83" + "\n" +
        "he : 3.07    ed : 1.17    le : 0.83" + "\n" +
        "in : 2.43    is : 1.13    ve : 0.83" + "\n" +
        "er : 2.05    it : 1.12    co : 0.79" + "\n" +
        "an : 1.99    al : 1.09    me : 0.79" + "\n" +
        "re : 1.85    ar : 1.07    de : 0.76" + "\n" +
        "on : 1.76    st : 1.05    hi : 0.76" + "\n" +
        "at : 1.49    to : 1.05    ri : 0.73" + "\n" +
        "en : 1.45    nt : 1.04    ro : 0.73" + "\n" +
        "nd : 1.35    ng : 0.95    ic : 0.70" + "\n" +
        "ti : 1.34    se : 0.93    ne : 0.69" + "\n" +
        "es : 1.34    ha : 0.93    ea : 0.69" + "\n" +
        "or : 1.28    as : 0.87    ra : 0.69" + "\n" +
        "te : 1.20    ou : 0.87    ce : 0.65" + "\n" +
        "\n" +
        "the : 3.508232    ere : 0.560594    ith : 0.431250" + "\n" +
        "and : 1.593878    for : 0.555372    ver : 0.430732" + "\n" +
        "ing : 1.147042    ent : 0.530771    all : 0.422758" + "\n" +
        "her : 0.822444    ion : 0.506454    wit : 0.397290" + "\n" +
        "hat : 0.650715    ter : 0.461099    thi : 0.394796" + "\n" +
        "his : 0.596748    was : 0.460487    tio :0.378058" + "\n" +
        "tha : 0.593593    you : 0.437213" + "\n" +
        "----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----" + "\n" +
        "German, Id: 0.0762" + "\n" +
        "E : 16.93" + "\n" +
        "N : 10.53" + "\n" +
        "I : 8.02" + "\n" +
        "R : 6.89" + "\n" +
        "S : 6.42" + "\n" +
        "T : 5.79" + "\n" +
        "A : 5.58" + "\n" +
        "D : 4.98" + "\n" +
        "H : 4.98" + "\n" +
        "U : 3.83" + "\n" +
        "L : 3.60" + "\n" +
        "\n" +
        "ER :  3.90    ST :  1.21    SE :  0.83" + "\n" +
        "EN :  3.61    NE :  1.19    IT :  0.81" + "\n" +
        "CH :  2.36    BE :  1.17    DI :  0.81" + "\n" +
        "DE :  2.31    ES :  1.17    IC :  0.80" + "\n" +
        "EI :  1.98    UN :  1.13    SC :  0.77" + "\n" +
        "TE :  1.98    RE :  1.11    LE :  0.73" + "\n" +
        "IN :  1.71    AN :  1.07    DA :  0.72" + "\n" +
        "ND :  1.68    HE :  0.89    NS :  0.71" + "\n" +
        "IE :  1.48    AU :  0.89    IS :  0.70" + "\n" +
        "GE :  1.45    NG :  0.87    RA :  0.69" + "\n" +
        "\n" +
        "DER :  1.04    INE :  0.48    BER :  0.36" + "\n" +
        "EIN :  0.83    TER :  0.44    ENS :  0.36" + "\n" +
        "SCH :  0.76    GEN :  0.44    NGE :  0.35" + "\n" +
        "ICH :  0.75    END :  0.44    RDE :  0.35" + "\n" +
        "NDE :  0.72    ERS :  0.42    VER :  0.34" + "\n" +
        "DIE :  0.62    STE :  0.42    EIT :  0.33" + "\n" +
        "CHE :  0.58    CHT :  0.41    HEN :  0.31" + "\n" +
        "DEN :  0.56    UNG :  0.39    ERD :  0.30" + "\n" +
        "TEN :  0.51    DAS :  0.38    REI :  0.30" + "\n" +
        "UND :  0.48    ERE :  0.38    IND :  0.29" + "\n" +
        "----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----")

def sprache(chiffre):
    x = 0
    itext = 0
    h = dict()
    for b in chiffre:
        if b in h:
            h[b] += 1
        else:
            h[b] = 1
    for keys in h.keys():
        n = len(chiffre)
        if n > 1:
            ni = h[keys]
            x += ni*(ni-1)
            itext = x/(n*(n-1))
    return itext

def help():
    print("\'help\'", "\'neu\'", "\'chiffre\'", "\'analyse (int)\'", "\'info\'", "\'sprache\'", "\'multirep\'", "\'caesar\'", "\'exit\'")

Commands = {
    'help': help,
    'analyse': analyse,
    'info': info,
    'sprache': sprache,
    'multirep': ersetze_menu,
    'caesar': caesarbruteforce
}

if __name__ == "__main__":
    print("Programmed by Kevin Küster" + "\n" + "--> 'help'"+ "\n")
    while True:
        command = input(">>>").lower().split(" ")
        if command[0] == "neu":
            chiffre = input("neue chiffre: ").upper()
       
        if command[0] == "chiffre":
            try:
                print(chiffre)
            except NameError:
                chiffre = input("chiffre: ").upper()
        if command[0] == "exit":
            break
        
        if command[0] in Commands:
            if Commands[command[0]] == Commands['help']:
                Commands[command[0]]()
            elif Commands[command[0]] == Commands['analyse']:
                try:
                    anzahl = int(command[1])
                    try:
                        Commands[command[0]](chiffre, anzahl)
                    except NameError:
                        chiffre = input("chiffre: ")
                    except TypeError:
                        Commands[command[0]](chiffre, 0)
                except IndexError or ValueError:   
                    try:
                        Commands[command[0]](chiffre, 0)
                    except NameError:
                        chiffre = input("chiffre: ")              
            elif Commands[command[0]] == Commands['info']:
                Commands[command[0]]()
            elif Commands[command[0]] == Commands['sprache']:
                try:
                    print("Koinzidenzindex: " + str(Commands[command[0]](chiffre)))
                except NameError:
                    chiffre = input("chiffre: ").upper()
            elif Commands[command[0]] == Commands['multirep']:
                try:
                    Commands[command[0]](chiffre)
                except NameError:
                    chiffre = input("chiffre: ").upper()
            elif Commands[command[0]] == Commands['caesar']:
                try:
                    Commands[command[0]](chiffre)
                except NameError:
                    chiffre = input("chiffre: ").upper()