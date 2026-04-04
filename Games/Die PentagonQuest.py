# =============================================================================
# DIE PENTAGONQUEST
# =============================================================================
#
# Funktion: Textbasiertes RPG auf einer 5x5-Karte; Ziel ist es, den OrkKönig
#           auf dem letzten Feld (4,4) zu besiegen.
#
#   ┌─────────────────────────────────────────────────────────────────────┐
#   │                        Klassenstruktur                              │
#   │                                                                     │
#   │  Item          -> Basisklasse für alle aufsammelbare Gegenstände    │
#   │    Sword       -> Waffe mit Angriffswert (ad)                       │
#   │    HPPlus      -> Verbrauchsitem zum dauerhaften HP-erhöhen         │
#   │                                                                     │
#   │  Character     -> Basisklasse für alle kampffähigen Einheiten       │
#   │    Player      -> Spielerfigur mit Inventar und Ausrüstungsslot     │
#   │    MobWithDrop -> Mixin: Gegner der beim Tod Items droppen kann     │
#   │      Goblin    -> Schwacher Gegner (100 HP, 10 AD)                  │
#   │      Ork       -> Mittlerer Gegner (300 HP, 30 AD)                  │
#   │      Waechter  -> Starker Gegner (800 HP, 15 AD)                    │
#   │    OrkKoenig   -> Endboss (4000 HP, 60 AD), kein Drop               │
#   │                                                                     │
#   │  Field         -> Ein Feld der Karte mit Gegnern und Loot           │
#   │  Map           -> 5x5-Gitter aus Fields; verwaltet Spielerposition  │
#   └─────────────────────────────────────────────────────────────────────┘
#
# SPIELBEFEHLE:
#   forward / backwards / left / right  -> Bewegung auf der Karte
#   fight    -> Alle Gegner auf dem aktuellen Feld bekämpfen
#   pickup N -> Item N aus dem Loot des Feldes aufheben
#   drop N   -> Item N aus dem Inventar auf dem Feld ablegen
#   equip N  -> Item N aus dem Inventar ausrüsten
#   use N    -> Item N aus dem Inventar benutzen (z.B. HPPlus)
#   inventar -> Inventar anzeigen
#   stats    -> Spieler-Status anzeigen
#   map      -> Aktuellen Feldstatus anzeigen
#   rest     -> HP vollständig regenerieren
#   help     -> Alle verfügbaren Befehle anzeigen
#   quit     -> Spiel beenden

import random
import time

# =============================================================================
# ITEM-KLASSEN
# =============================================================================

class Item:
    """Basisklasse für alle aufsammelbaren Gegenstände."""

    def __init__(self, weight, worth):
        self.weight = weight      # Gewicht des Items (aktuell nicht spielmechanisch genutzt)
        self.worth = worth        # Wert des Items in Gold (aktuell nicht spielmechanisch genutzt)
        self.equipped = False     # Gibt an, ob das Item gerade ausgerüstet ist

    def set_equipped_true(self):
        self.equipped = True

    def set_equipped_false(self):
        self.equipped = False


class Sword(Item):
    """Waffe, die beim Ausrüsten den AD-Wert des Spielers überschreibt."""

    def __init__(self, weight, worth, ad, name):
        Item.__init__(self, weight, worth)
        self.ad = ad        # Angriffswert des Schwertes
        self.name = name    # Anzeigename im Inventar / Loot


class HPPlus(Item):
    """Verbrauchsitem, das beim Benutzen die maximalen HP dauerhaft erhöht."""

    def __init__(self, hpPlus, name):
        self.hpPlus = hpPlus    # Betrag, um den max_hp steigt
        self.name = name        # Anzeigename im Inventar / Loot
        # Kein Aufruf von Item.__init__, da HPPlus kein Gewicht/Wert hat

# =============================================================================
# CHARACTER-KLASSEN
# =============================================================================

class Character:
    """Basisklasse für alle kampffähigen Einheiten (Spieler und Gegner)."""

    def __init__(self, hp, ad, name):
        self.hp = hp        # Aktuelle Lebenspunkte
        self.ad = ad        # Angriffswert (attack damage)
        self.name = name    # Anzeigename

    def get_hit(self, ad):
        """Zieht `ad` Schadenspunkte ab; ruft die() auf, wenn HP <= 0."""
        self.hp = self.hp - ad
        if self.hp <= 0:
            self.die()

    def is_dead(self):
        """Gibt True zurück, wenn die Einheit keine HP mehr hat."""
        return self.hp <= 0

    def die(self):
        """Standardreaktion beim Tod: Meldung ausgeben."""
        print(self.name + " ist gestorben")


class MobWithDrop():
    """Mixin-Klasse für Gegner, die beim Tod eine Drop-Liste hinterlassen."""

    def __init__(self, drop):
        self.drop = drop    # Liste von Item-Objekten, die der Mob droppen soll

    def get_drop(self):
        return self.drop


# -----------------------------------------------------------------------------
# GEGNERTYPEN (erben von Character und MobWithDrop)
# -----------------------------------------------------------------------------

class Goblin(Character, MobWithDrop):
    """Schwacher Gegner: 100 HP, 10 AD."""

    def __init__(self, drop):
        MobWithDrop.__init__(self, drop)
        Character.__init__(self, 100, 10, "Goblin")


class Ork(Character, MobWithDrop):
    """Mittlerer Gegner: 300 HP, 30 AD."""

    def __init__(self, drop):
        MobWithDrop.__init__(self, drop)
        Character.__init__(self, 300, 30, "Ork")


class OrkKoenig(Character):
    """Endboss auf dem letzten Feld: 4000 HP, 60 AD, kein Drop."""

    def __init__(self):
        Character.__init__(self, 4000, 60, "OrkKoenig")


class Waechter(Character, MobWithDrop):
    """Starker Gegner: 800 HP, 15 AD (niedriger AD als Ork, aber mehr HP)."""

    def __init__(self, drop):
        MobWithDrop.__init__(self, drop)
        Character.__init__(self, 800, 15, "Waechter")


# =============================================================================
# SPIELER-KLASSE
# =============================================================================

class Player(Character):
    """
    Die vom Benutzer gesteuerte Spielfigur.

    Erweitert Character um:
      - Inventar (Liste von Items, begrenzt durch maxInv)
      - Ausrüstungs-Slot (ein Item gleichzeitig equipped)
      - Basis-AD-Wert der Hand (adHand), der beim Ablegen einer Waffe wiederhergestellt wird
      - max_hp: obere Grenze für die Regeneration via rest()
    """

    def __init__(self, name, hp, ad, maxInv):
        Character.__init__(self, hp, ad, name)
        self.adHand = ad        # Basis-AD ohne Waffe (wird bei drop() wiederhergestellt)
        self.ad = ad            # Aktueller AD (kann durch equip() erhöht werden)
        self.max_hp = hp        # Maximale HP (kann durch HPPlus-Items erhöht werden)
        self.inv = []           # Inventarliste (Item-Objekte)
        self.maxInv = maxInv    # Maximale Anzahl an Items im Inventar
        self.equippedItem = 0   # Index des ausgerüsteten Items (wird via eItem() ermittelt)

    def get_inv(self):
        """Gibt die Inventarliste zurück."""
        return self.inv

    def show_inv(self):
        """Gibt die aktuelle Inventarbelegung als 'belegt/max' aus."""
        print(str(len(self.inv)) + "/" + str(self.maxInv))

    def die(self):
        """Überschreibt Character.die(): Spielende statt Meldung."""
        exit("Du bist gestorben.")

    def rest(self):
        """Füllt HP vollständig auf max_hp auf."""
        self.hp = self.max_hp

    def eItem(self):
        """
        Gibt den Index des aktuell ausgerüsteten Items zurück.
        Gibt None zurück, wenn kein Item ausgerüstet ist.
        """
        for i in range(len(self.inv)):
            if self.inv[i].equipped == True:
                return i


# =============================================================================
# KARTEN-KLASSEN
# =============================================================================

class Field:
    """
    Ein einzelnes Feld auf der Karte.
    Enthält eine Liste von Gegnern und eine Liste von Loot-Items.
    """

    def __init__(self, enemies, loot):
        self.enemies = enemies  # Liste aktiver Gegner-Objekte auf diesem Feld
        self.loot = loot        # Liste von Item-Objekten, die aufgesammelt werden können

    def print_state(self):
        """Gibt Gegner (mit HP/AD) und Loot (mit Index) des Feldes aus."""
        print("Du guckst dich um und siehst ")
        print("\n" + "Feinde:")
        for i in self.enemies:
            print(i.name + " >  HP: " + str(i.hp) + " , " + "Atk: " + str(i.ad))
        print("\n" + "Loot:")
        x = 0
        for i in self.loot:
            print(str(x) + ". " + i.name)
            x = x + 1

    @staticmethod
    def gen_random():
        """
        Erzeugt zufällig eines von 5 vordefinierten Feldszenarien.
        Wird bei der Kartengenerierung für alle Felder außer Start und Ende genutzt.
        """
        rand = random.randint(0, 4)
        if rand == 0:
            return Field([Waechter([Sword(1, 100, 400, "Sword: 400ad")]), Waechter([Sword(1, 100, 400, "Sword: 400ad")])], [])
        if rand == 1:
            return Field([Ork([Sword(1, 100, 250, "Sword: 250ad"), HPPlus(50, "+50 Hp")])], [])
        if rand == 2:
            return Field([Goblin([]), Waechter([Sword(1, 100, 400, "Sword: 400ad")]), Ork([Sword(1, 100, 250, "Sword: 250ad"), HPPlus(50, "+50 Hp")])], [])
        if rand == 3:
            return Field([Goblin([Sword(1, 100, 100, "Sword: 100ad")]), Goblin([]), Goblin([])], [])
        if rand == 4:
            return Field([Goblin([]), Ork([Sword(1, 100, 250, "Sword: 250ad"), HPPlus(50, "+50 Hp")])], [])


class Map:
    """
    Zweidimensionales 5x5-Gitter aus Field-Objekten.

    Sonderfälle bei der Generierung:
      - (0,0): Startfeld mit drei Goblins (Tutorial-Gegner)
      - (width-1, height-1): Endfeld mit dem OrkKönig (Endboss)
      - alle anderen Felder: zufällig generiert via Field.gen_random()

    Die Spielerposition wird durch (self.x, self.y) verwaltet.
    Bewegungsmethoden (forward/backwards/left/right) prüfen die Grenzen
    und geben eine Meldung aus, falls die Karte verlassen werden würde.
    """

    def __init__(self, width, height):
        self.state = []         # 2D-Liste von Field-Objekten [x][y]
        self.width = width      # Breite der Karte (x-Achse)
        self.height = height    # Höhe der Karte (y-Achse)
        self.x = 0              # Aktuelle x-Position des Spielers
        self.y = 0              # Aktuelle y-Position des Spielers

        # Karte generieren: äußere Schleife = x (Spalten), innere = y (Zeilen)
        for i in range(width):
            fields = []
            for j in range(height):
                if i == 0 and j == 0:
                    # Startfeld: drei Goblins für das Tutorial
                    fields.append(Field([Goblin([Sword(1, 100, 100, "Sword: 100ad")]), Goblin([]), Goblin([])], []))
                elif i == width - 1 and j == height - 1:
                    # Endfeld: Endboss OrkKönig, kein initialer Loot
                    fields.append(Field([OrkKoenig()], []))
                else:
                    # Alle anderen Felder: zufälliges Szenario
                    fields.append(Field.gen_random())
            self.state.append(fields)

    def print_state(self):
        """Gibt aktuelle Koordinaten und den Zustand des aktuellen Feldes aus."""
        print("x: " + str(self.x), "y: " + str(self.y))
        self.state[self.x][self.y].print_state()

    def get_enemies(self):
        """Gibt die Gegnerliste des aktuellen Feldes zurück."""
        return self.state[self.x][self.y].enemies

    def get_loot(self):
        """Gibt die Lootliste des aktuellen Feldes zurück."""
        return self.state[self.x][self.y].loot

    # -------------------------------------------------------------------------
    # BEWEGUNGSMETHODEN: prüfen Grenzen, dann Koordinate anpassen
    # -------------------------------------------------------------------------

    def forward(self):
        """Bewegt den Spieler in positive x-Richtung (falls möglich)."""
        if self.x == len(self.state) - 1:
            print("Du siehst riesige Berge, welche du nicht überqueren kannst")
        else:
            self.x = self.x + 1

    def backwards(self):
        """Bewegt den Spieler in negative x-Richtung (falls möglich)."""
        if self.x == 0:
            print("Du siehst Klippen, kannst aber nicht sicher hinunterspringen")
        else:
            self.x = self.x - 1

    def right(self):
        """Bewegt den Spieler in positive y-Richtung (falls möglich)."""
        if self.y == len(self.state[self.x]) - 1:
            print("Du siehst riesige Berge, welche du nicht überqueren kannst")
        else:
            self.y = self.y + 1

    def left(self):
        """Bewegt den Spieler in negative y-Richtung (falls möglich)."""
        if self.y == 0:
            print("Du siehst Klippen, kannst aber nicht sicher hinunterspringen")
        else:
            self.y = self.y - 1


# =============================================================================
# BEFEHLSFUNKTIONEN
# =============================================================================
# Jede Funktion entspricht einem Spielerbefehl.
# Signatur: f(p: Player, m: Map) bzw. f(p, m, item) bei Item-Befehlen.
# Die Functions werden im Commands-Dict registriert und von der Spielschleife
# aufgerufen.
# -----------------------------------------------------------------------------

def forward(p, m):
    m.forward()
    m.print_state()

def right(p, m):
    m.right()
    m.print_state()

def left(p, m):
    m.left()
    m.print_state()

def backwards(p, m):
    m.backwards()
    m.print_state()

def quit_game(p, m):
    print("Du hast Selbstmord begangen und diese Welt verlassen.")
    exit(0)

def print_help(p, m):
    """Gibt alle registrierten Befehle aus."""
    print(Commands.keys())

def pickup(p, m, item):
    """
    Hebt Item mit Index `item` aus dem Loot des aktuellen Feldes auf
    und fügt es dem Inventar hinzu (sofern Platz vorhanden).
    """
    loot = m.get_loot()
    if len(p.inv) < p.maxInv:
        p.inv.append(loot[item])
        loot.remove(loot[item])
        m.print_state()
        print('\n')
    else:
        print("Dein Inventar ist voll")

def fight(p, m):
    """
    Kampfschleife: Spieler greift immer den ersten Gegner an.
    Alle lebenden Gegner greifen danach den Spieler an.
    Tote Gegner werden aus der Liste entfernt; ihr Loot landet auf dem Feld.
    """
    enemies = m.get_enemies()
    if len(enemies) != 0:
        while len(enemies) > 0:
            # Spieler greift den ersten Gegner in der Liste an
            enemies[0].get_hit(p.ad)
            if enemies[0].is_dead():
                # Drop des besiegten Gegners auf das Feld legen
                try:
                    drop = enemies[0].get_drop()
                    loot = m.get_loot()
                    for i in drop:
                        loot.append(i)
                except AttributeError:
                    pass    # OrkKoenig hat kein get_drop() -> ignorieren
                enemies.remove(enemies[0])
            # Alle noch lebenden Gegner greifen den Spieler an
            for i in enemies:
                p.get_hit(i.ad)
            print("Du bist verwundet und hast " + str(p.hp) + " hp übrig")
    else:
        print("Alle Feinde sind besiegt worden")
    print('\n')
    m.print_state()

def ende(p, m):
    """
    Prüft, ob das Spiel noch läuft.
    Gibt False zurück (Schleife endet), wenn der OrkKönig besiegt wurde.
    """
    if len(map.state[m.width - 1][m.height - 1].enemies) == 0:
        return False
    else:
        return True

def rest(p, m):
    """Regeneriert die HP des Spielers vollständig auf max_hp."""
    p.rest()

def inventar(p, m):
    """Gibt alle Items im Inventar mit ihrem Index aus."""
    itemsIninv = p.get_inv()
    x = 0
    for i in itemsIninv:
        print(str(x) + ". " + i.name)
        x = x + 1
    print("\n")

def equip(p, m, item):
    """
    Rüstet Item `item` aus dem Inventar aus.
    Zuerst wird das aktuell ausgerüstete Item (falls vorhanden) abgelegt.
    Nur Items mit einem `ad`-Attribut (Schwerter) können ausgerüstet werden.
    """
    try:
        # Aktuell ausgerüstetes Item ablegen
        p.inv[p.eItem()].set_equipped_false()
        try:
            p.ad = p.inv[item].ad       # AD des Spielers auf Schwert-AD setzen
            p.inv[item].set_equipped_true()
        except AttributeError:
            print("Du kannst dieses Item nicht ausrüsten")
    except TypeError:
        # TypeError: eItem() hat None zurückgegeben -> kein Item war ausgerüstet
        try:
            p.ad = p.inv[item].ad
            p.inv[item].set_equipped_true()
        except AttributeError:
            print("Du kannst dieses Item nicht ausrüsten")

def stats(p, m):
    """Gibt Name, HP, AD und Inventarbelegung des Spielers aus."""
    print("Name: " + p.name + '\n' + "Gesundheit: " + str(p.hp) + "/" + str(p.max_hp) + "\n" + "Angriff: " + str(p.ad) + "\n" + "Inventar: ")
    p.show_inv()

def map(p, m):
    """Zeigt den aktuellen Feldstatus (Gegner + Loot + Koordinaten) an."""
    m.print_state()

def drop(p, m, item):
    """
    Legt Item `item` aus dem Inventar auf dem aktuellen Feld ab.
    Falls das Item ausgerüstet war, wird der AD auf den Handwert zurückgesetzt.
    """
    item = p.inv[item]
    loot = m.get_loot()
    if item.equipped == True:
        p.ad = p.adHand     # Waffe abgelegt -> AD zurück auf Basiswert
    loot.append(item)
    p.inv.remove(item)

def use(p, m, item):
    """
    Benutzt Item `item` aus dem Inventar.
    Aktuell nur HPPlus-Items unterstützt: max_hp dauerhaft erhöhen und Item verbrauchen.
    """
    item = p.inv[item]
    try:
        p.max_hp = p.max_hp + item.hpPlus  # Maximale HP dauerhaft erhöhen
        p.inv.remove(item)                  # Item ist verbraucht
    except AttributeError:
        print("Du kannst dieses Item nicht benutzen")


# =============================================================================
# BEFEHLSREGISTER
# =============================================================================
# Ordnet Befehlsstrings den entsprechenden Funktionen zu.
# Befehle mit Item-Parameter (pickup, drop, equip, use) werden in der
# Spielschleife gesondert behandelt (Index-Parsing + Fehlerbehandlung).

Commands = {
    'help':      print_help,
    'quit':      quit_game,
    'pickup':    pickup,
    'forward':   forward,
    'right':     right,
    'left':      left,
    'backwards': backwards,
    'fight':     fight,
    'rest':      rest,
    'inventar':  inventar,
    'equip':     equip,
    'stats':     stats,
    'map':       map,
    'drop':      drop,
    'use':       use
}


# =============================================================================
# EINSTIEGSPUNKT: TUTORIAL + SPIELSCHLEIFE
# =============================================================================

if __name__ == '__main__':

    # -------------------------------------------------------------------------
    # TUTORIAL: Schritt-für-Schritt-Einführung in die Spielbefehle
    # Jeder Abschnitt wartet auf die korrekte Eingabe und wiederholt sonst die Anweisung.
    # -------------------------------------------------------------------------

    print("Willkommen im Ödland Fremder!")
    time.sleep(3)
    print('\n' + "Das Ödland wird schon seit langer Zeit von dem Ork-König unterdrückt...")
    time.sleep(2)
    print("Hilf uns ihn zu besiegen!")
    time.sleep(3)
    print("Du siehst aus, als könntest du kämpfen. Wie ist dein Name Fremder ?")
    time.sleep(3)
    name = input("Gib deinen Namen ein: ")
    time.sleep(2)

    # Spieler (200 HP, 50 AD, Inventar max. 5 Items) und 5x5-Karte erstellen
    p = Player(name, 200, 50, 5)
    map = Map(5, 5)

    # -- Tutorial: map --
    print('\n' + "Sehr gut " + name + ", beginnen wir mit den Grundlagen:")
    time.sleep(2)
    print("Mit 'map' kannst du dir den aktuellen Status deiner Umgebung anzeigen lassen. Dir werden Beute und Gegner auf dem aktuellen Feld angezeigt, sowie die Koordinaten des Feldes")
    while True:
        if input(">") == "map":
            map.print_state()
            break
        else:
            print("Mit 'map' kannst du dir den aktuellen Status deiner Umgebung anzeigen lassen. Dir werden Beute und Gegner auf dem aktuellen Feld angezeigt, sowie die Koordinaten des Feldes")

    # -- Tutorial: fight --
    print('\n' + "Oh nein, Goblins haben das Gebiet besetzt. Du kannst sie mit 'fight' bekämpfen")
    while True:
        if input(">") == "fight":
            fight(p, map)
            break
        else:
            print("Oh nein, Goblins haben das Gebiet besetzt. Du kannst sie mit 'fight' bekämpfen")

    # -- Tutorial: pickup --
    print('\n' + '\n' + "Während des Kampfes kannst du sehen, welchen Schaden du einstecken musstest. Fallen deine Lebenspunkte auf 0, stirbst du!" + '\n' + '\n' + "Die Goblins haben ein Schwert fallen lassen. Du kannst Items mit 'pickup' aufheben. Im Anschluss musst du auswählen, welches Item du von dem jeweiligen Bereich nehmen möchtest. Die Zahl vor dem Item bestimmt, welches Item du aufheben kannst. In diesem Fall: 'pickup 0'")
    while True:
        if input(">") == "pickup 0":
            pickup(p, map, 0)
            break
        else:
            print("Die Goblins haben ein Schwert fallen lassen. Du kannst Items mit 'pickup' aufheben. Im Anschluss musst du auswählen, welches Item du von dem jeweiligen Bereich nehmen möchtest. Die Zahl vor dem Item bestimmt, welches Item du aufheben kannst. In diesem Fall: 'pickup 0'")

    # -- Tutorial: inventar --
    print("Das Item wurde deinem Inventar hinzugefügt. Du kannst dir ein Inventar mit 'inventar' ausgeben lassen")
    while True:
        if input(">") == "inventar":
            inventar(p, map)
            break
        else:
            print("Das Item wurde deinem Inventar hinzugefügt. Du kannst dir ein Inventar mit 'inventar' ausgeben lassen")

    # -- Tutorial: stats --
    print("Mit 'stats' kannst du dir deinen aktuellen Status ausgeben lassen. Du kannst deinen Namen, deine aktuellen Lebenspunkte, den Schaden, den du verursachst, sowie deinen Platz in deinem Inventar sehen")
    while True:
        if input(">") == "stats":
            stats(p, map)
            break
        else:
            print("Mit 'stats' kannst du dir deinen aktuellen Status ausgeben lassen. Du kannst deinen Namen, deine aktuellen Lebenspunkte, den Schaden, den du verursachst, sowie deinen Platz in deinem Inventar sehen")

    # -- Tutorial: equip --
    print("Du kannst aufgesammelte Items, die sich in deinem Inventar befinden ausrüsten oder benutzen. Das Schwert, welches du von den Goblins bekommen, kannst du ausrüsten. Dadurch verursachst du erhöhten Schaden. Ausrüsten kannst du ein Item mit 'equip', benutzen kannst du ein Item mit 'use'. Auch hier musst du mit einem Index angeben, welches Item du ausrüsten bzw. benutzen möchtest. Rüste das Schwert aus deinem Inventar mit 'equip 0' aus")
    while True:
        if input(">") == "equip 0":
            equip(p, map, 0)
            break
        else:
            print("Du kannst aufgesammelte Items, die sich in deinem Inventar befinden ausrüsten oder benutzen. Das Schwert, welches du von den Goblins bekommen, kannst du ausrüsten. Dadurch verursachst du erhöhten Schaden. Ausrüsten kannst du ein Item mit 'equip', benutzen kannst du ein Item mit 'use'. Auch hier musst du mit einem Index angeben, welches Item du ausrüsten bzw. benutzen möchtest. Rüste das Schwert aus deinem Inventar mit 'equip 0' aus")

    # -- Tutorial: stats (nach equip) --
    print("Über eine erneute Ausgabe deines Status mit 'stats' siehst du, dass du nun Schaden in Höhe des Angriffswertes des Schwertes verursachst")
    while True:
        if input(">") == "stats":
            stats(p, map)
            break
        else:
            print("Über eine erneute Ausgabe deines Status mit 'stats' siehst du, dass du nun Schaden in Höhe des Angriffswertes des Schwertes verursachst")

    # -- Tutorial: rest --
    print("Deine Lebenspunkte sind zur Zeit auf 200 begrenzt, lassen sich aber z.B. durch HPPlus items erhöhen. Nach jedem Kampf kannst du deine Lebenspunkte mit 'rest' wieder auffüllen")
    while True:
        if input(">") == "rest":
            rest(p, map)
            break
        else:
            print("Deine Lebenspunkte sind zur Zeit auf 200 begrenzt, lassen sich aber z.B. durch HPPlus items erhöhen. Nach jedem Kampf kannst du deine Lebenspunkte mit 'rest' wieder auffüllen")

    # -- Tutorial: Abschluss --
    print("Sollte dein Inventar voll sein, kannst du Items die du nicht länger benötigst mit 'drop' ablegen. Diese findest du im Anschluss in dem Bereich, in dem du dich aktuell befindest." + '\n' + "Mit 'forward', 'backwards', 'left' und 'right' kannst du dich auf der Karte bewegen")
    print('\n' + "help zeigt dir alle verfügbaren Handlungsoptionen\n")
    map.print_state()

    # -------------------------------------------------------------------------
    # HAUPTSCHLEIFE: Läuft solange der OrkKönig lebt (ende() gibt True zurück)
    # -------------------------------------------------------------------------
    while ende(p, map):
        command = input(">").lower().split(" ")  # Eingabe in Befehl + Argumente aufteilen
        parameter = 0

        if command[0] in Commands:
            # Befehle mit Item-Index-Parameter: Parsing und Fehlerbehandlung
            if Commands[command[0]] in (Commands['pickup'], Commands['drop'], Commands['equip'], Commands['use']):
                try:
                    parameter = int(command[1])     # Index muss eine Ganzzahl sein
                    Commands[command[0]](p, map, parameter)
                except ValueError:
                    print("Du begibst dich auf einen Pfad, dem keiner folgen kann...")
                except IndexError:
                    print("Wähle ein Item")
            else:
                # Befehle ohne Item-Parameter
                Commands[command[0]](p, map)
        else:
            print("Du begibst dich auf einen Pfad, dem keiner folgen kann...")

    # -------------------------------------------------------------------------
    # SPIELENDE: OrkKönig besiegt
    # -------------------------------------------------------------------------
    print('\n' + '\n' + "Der Ork-König wurde besiegt..." + '\n' + "Du hast es geschafft " + name + "!" + '\n' + "Danke deiner Hilfe konnte das Ödland befreit werden." + '\n' + '\n' + "Wir werden dir für immer dankbar sein..." + '\n' + '\n' + '\n' + "ENDE ~progammed by Kevin Küster")
    time.sleep(15)
