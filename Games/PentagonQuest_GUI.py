#!/usr/bin/env python3
"""
Die PentagonQuest – Grafische Version
Original-Konsolenspiel: Kevin Küster
Grafische Umsetzung: Claude
"""
import pygame, sys, math, random

# ════════════════════════════════════════════════════════════
# Konstanten & Layout
# ════════════════════════════════════════════════════════════
SW, SH = 1280, 720

BLACK      = (0, 0, 0)
WHITE      = (255, 255, 255)
GRAY       = (128, 128, 128)
DARK_GRAY  = (40, 40, 40)
LIGHT_GRAY = (180, 180, 180)
RED        = (200, 40, 40)
DARK_RED   = (120, 20, 20)
GREEN      = (40, 180, 40)
DARK_GREEN = (20, 80, 20)
BLUE       = (40, 80, 200)
YELLOW     = (220, 200, 40)
ORANGE     = (220, 120, 40)
BROWN      = (100, 60, 20)
DARK_BROWN = (60, 30, 10)
STONE      = (90, 80, 70)
DARK_STONE = (50, 45, 40)
LIGHT_STONE= (130, 120, 110)
GOLD       = (200, 170, 40)
SILVER     = (160, 170, 180)

HUD_RECT     = pygame.Rect(0,   0,   870,  50)
DUNGEON_RECT = pygame.Rect(0,   50,  870,  495)
DIALOG_RECT  = pygame.Rect(0,   545, SW,   175)
MINIMAP_RECT = pygame.Rect(875, 5,   280,  280)
NAV_RECT     = pygame.Rect(875, 330, 280,  175)

# Inventar-Layout (absolute Bildschirmkoordinaten)
INV_COLS = 4
INV_SS   = 108   # Slot-Größe
INV_GAP  = 8
INV_OX   = 30    # Panel x(10) + padding(20)
INV_OY   = 118   # Panel y(60) + Titel(58)

# ════════════════════════════════════════════════════════════
# Spiellogik
# ════════════════════════════════════════════════════════════

class Item:
    item_type = "generic"
    def __init__(self, weight, worth, name):
        self.weight   = weight
        self.worth    = worth
        self.name     = name
        self.equipped = False

class Sword(Item):
    item_type = "weapon"
    def __init__(self, weight, worth, ad, name):
        super().__init__(weight, worth, name)
        self.ad = ad

class HPPlus(Item):
    item_type = "potion"
    def __init__(self, hp_plus, name):
        super().__init__(0, 50, name)
        self.hp_plus = hp_plus

class Armor(Item):
    item_type = "armor"
    def __init__(self, weight, worth, defense, name):
        super().__init__(weight, worth, name)
        self.defense = defense

class Character:
    def __init__(self, hp, ad, name):
        self.hp     = hp
        self.max_hp = hp
        self.ad     = ad
        self.name   = name

    def get_hit(self, dmg):
        self.hp = max(0, self.hp - dmg)

    def is_dead(self):
        return self.hp <= 0

class Monster(Character):
    def __init__(self, hp, ad, name, sprite, xp, drop):
        super().__init__(hp, ad, name)
        self.sprite = sprite
        self.xp     = xp
        self.drop   = drop

    def get_drop(self):
        return self.drop

def make_goblin():
    # Kleiner Trank oder rostiges Schwert als Drop
    if random.random() < 0.55:
        drop = [HPPlus(40, "Kleiner Heiltrank")]
    else:
        drop = [Sword(1, 25, 18, "Rostiges Schwert")]
    return Monster(40, 9, "Goblin", "goblin", 30, drop)

def make_ork():
    drop = [HPPlus(75, "Heiltrank")]
    if random.random() < 0.50:
        drop.append(Sword(2, 80, 52, "Kurzschwert"))
    return Monster(200, 26, "Ork", "ork", 85, drop)

def make_waechter():
    drop = [Sword(3, 150, 88, "Langschwert")]
    r = random.random()
    if r < 0.30:
        drop.append(Armor(4, 220, 18, "Lederrüstung"))
    elif r < 0.55:
        drop.append(HPPlus(120, "Großer Heiltrank"))
    return Monster(480, 20, "Wächter", "waechter", 160, drop)

def make_ork_koenig():
    return Monster(1800, 50, "Ork-König", "ork_koenig", 800, [])

# Statische Beschreibungen für Monsterinfo-Seite
MONSTER_INFO = [
    {
        "name":   "Goblin",
        "sprite": "goblin",
        "hp":     40,
        "atk":    9,
        "xp":     30,
        "drops":  "Kleiner Heiltrank (55%) oder Rostiges Schwert (45%)",
        "desc":   "Schwaches, aber flinkes Wesen. Gefährlich in Gruppen.",
        "rating": "★☆☆☆",
    },
    {
        "name":   "Ork",
        "sprite": "ork",
        "hp":     200,
        "atk":    26,
        "xp":     85,
        "drops":  "Heiltrank (immer) + Kurzschwert (50%)",
        "desc":   "Massiver Krieger. Hoher Schaden – Rüstung empfohlen!",
        "rating": "★★☆☆",
    },
    {
        "name":   "Wächter",
        "sprite": "waechter",
        "hp":     480,
        "atk":    20,
        "xp":     160,
        "drops":  "Langschwert (immer) + Lederrüstung (30%) / Gr. Trank (25%)",
        "desc":   "Schwer gepanzerter Soldat. Viel Ausdauer nötig, gute Beute.",
        "rating": "★★★☆",
    },
    {
        "name":   "Ork-König",
        "sprite": "ork_koenig",
        "hp":     1800,
        "atk":    50,
        "xp":     800,
        "drops":  "Kein Drop – der Sieg selbst ist die Belohnung.",
        "desc":   "Der Endboss. Benötigt mindestens Langschwert + Rüstung.",
        "rating": "★★★★",
    },
]

class Player(Character):
    XP_PER_LEVEL = 120   # XP für Level 1→2; Level n→n+1 kostet n * XP_PER_LEVEL
    HP_PER_LEVEL = 30
    ATK_PER_LEVEL = 8

    def __init__(self, name):
        super().__init__(120, 22, name)
        self.ad_base   = 22
        self.defense   = 0
        self.inv       = []
        self.max_inv   = 8
        self.eq_weapon = None
        self.eq_armor  = None
        self.xp        = 0
        self.level     = 1

    def equip(self, item):
        if isinstance(item, Sword):
            if self.eq_weapon:
                self.eq_weapon.equipped = False
            self.eq_weapon = item
            item.equipped  = True
            self.ad = self.ad_base + item.ad
            return f"'{item.name}' ausgerüstet! ATK: {self.ad}"
        elif isinstance(item, Armor):
            if self.eq_armor:
                self.eq_armor.equipped = False
            self.eq_armor  = item
            item.equipped  = True
            self.defense   = item.defense
            return f"'{item.name}' ausgerüstet! DEF: {self.defense}"
        return "Kann nicht ausgerüstet werden."

    def use_item(self, item):
        if isinstance(item, HPPlus):
            if self.hp >= self.max_hp:
                return f"HP bereits voll! ({self.hp}/{self.max_hp})"
            restored = min(item.hp_plus, self.max_hp - self.hp)
            self.hp += restored
            self.inv.remove(item)
            return f"'{item.name}' benutzt! +{restored} HP ({self.hp}/{self.max_hp})"
        return "Kann nicht benutzt werden."

    def drop_item(self, item):
        if item is self.eq_weapon:
            self.eq_weapon = None
            self.ad = self.ad_base
        elif item is self.eq_armor:
            self.eq_armor = None
            self.defense  = 0
        item.equipped = False
        self.inv.remove(item)

    def get_hit(self, dmg):
        actual = max(1, dmg - self.defense)
        self.hp = max(0, self.hp - actual)
        return actual

    def rest(self):
        self.hp = self.max_hp

    def xp_needed(self):
        """XP für nächstes Level."""
        return self.level * self.XP_PER_LEVEL

    def gain_xp(self, amount):
        self.xp += amount
        msgs = []
        while self.xp >= self.xp_needed():
            self.xp     -= self.xp_needed()
            self.level  += 1
            self.max_hp += self.HP_PER_LEVEL
            self.hp      = self.max_hp           # HP vollständig aufgefüllt
            self.ad_base += self.ATK_PER_LEVEL
            self.ad = self.ad_base + (self.eq_weapon.ad if self.eq_weapon else 0)
            msgs.append(
                f"★ Level Up! Du bist jetzt Level {self.level}!  "
                f"+{self.HP_PER_LEVEL} Max-HP  +{self.ATK_PER_LEVEL} ATK  HP aufgefüllt!")
        return msgs


class Field:
    def __init__(self, enemies, loot=None):
        self.enemies        = enemies
        self.loot           = loot or []
        self.visited        = False
        self.combat_started = False

    @staticmethod
    def random():
        t = random.randint(0, 7)
        if t == 0:   # Schatz-Raum – keine Feinde, gute Beute
            return Field([], loot=[HPPlus(120, "Großer Heiltrank"),
                                   Armor(5, 280, 28, "Kettenhemd")])
        elif t == 1: return Field([make_goblin(), make_goblin()])
        elif t == 2: return Field([make_goblin(), make_goblin(), make_goblin()])
        elif t == 3: return Field([make_ork()])
        elif t == 4: return Field([make_goblin(), make_ork()])
        elif t == 5: return Field([make_waechter()])
        elif t == 6: return Field([make_goblin(), make_waechter()])
        else:        return Field([make_waechter(), make_waechter()])


class GameMap:
    SIZE = 5

    def __init__(self):
        self.x    = 0
        self.y    = 0
        self.grid = []
        for i in range(self.SIZE):
            row = []
            for j in range(self.SIZE):
                if i == 0 and j == 0:
                    row.append(Field([make_goblin(), make_goblin()]))
                elif i == self.SIZE - 1 and j == self.SIZE - 1:
                    row.append(Field([make_ork_koenig()]))
                else:
                    row.append(Field.random())
            self.grid.append(row)
        self.grid[0][0].visited = True

    @property
    def field(self):
        return self.grid[self.x][self.y]

    def can_move(self, dx, dy):
        return 0 <= self.x + dx < self.SIZE and 0 <= self.y + dy < self.SIZE

    def move(self, dx, dy):
        if self.can_move(dx, dy):
            self.x += dx
            self.y += dy
            self.field.visited = True
            return True
        return False

    def boss_dead(self):
        return not self.grid[self.SIZE - 1][self.SIZE - 1].enemies


# ════════════════════════════════════════════════════════════
# Monster-Zeichenfunktionen (pixel-art-ähnliche Figuren)
# ════════════════════════════════════════════════════════════

def _p(cx, cy, s, x, y):
    """Skalierter Punkt"""
    return (int(cx + x * s), int(cy + y * s))

def _r(cx, cy, s, x, y, w, h):
    """Skaliertes Rechteck als Tuple"""
    return (int(cx + x * s), int(cy + y * s), int(w * s), int(h * s))


def draw_goblin(surf, cx, cy, s=1.0):
    # Schatten
    pygame.draw.ellipse(surf, (20, 35, 20), _r(cx, cy, s, -28, -4, 56, 12))
    # Beine
    pygame.draw.rect(surf, (20, 90, 20), _r(cx, cy, s, -18, -42, 13, 42))
    pygame.draw.rect(surf, (20, 90, 20), _r(cx, cy, s, 5, -42, 13, 42))
    # Körper
    pygame.draw.ellipse(surf, (70, 160, 55), _r(cx, cy, s, -25, -124, 50, 86))
    # Arme
    pygame.draw.line(surf, (70, 160, 55), _p(cx, cy, s, -25, -104), _p(cx, cy, s, -43, -76), max(1, int(7 * s)))
    pygame.draw.line(surf, (70, 160, 55), _p(cx, cy, s, 25, -104), _p(cx, cy, s, 43, -76), max(1, int(7 * s)))
    # Keule in rechter Hand
    pygame.draw.line(surf, DARK_BROWN, _p(cx, cy, s, 43, -76), _p(cx, cy, s, 57, -52), max(1, int(4 * s)))
    pygame.draw.circle(surf, BROWN, _p(cx, cy, s, 59, -48), max(1, int(9 * s)))
    # Lederweste
    pygame.draw.rect(surf, DARK_BROWN, _r(cx, cy, s, -18, -112, 36, 18))
    # Kopf
    pygame.draw.circle(surf, (70, 160, 55), _p(cx, cy, s, 0, -151), max(1, int(30 * s)))
    # Ohren (spitz)
    pygame.draw.polygon(surf, (58, 128, 43), [
        _p(cx, cy, s, -27, -161), _p(cx, cy, s, -50, -184), _p(cx, cy, s, -19, -146)])
    pygame.draw.polygon(surf, (58, 128, 43), [
        _p(cx, cy, s, 27, -161), _p(cx, cy, s, 50, -184), _p(cx, cy, s, 19, -146)])
    # Augen
    for ex in (-10, 10):
        pygame.draw.circle(surf, YELLOW, _p(cx, cy, s, ex, -156), max(1, int(7 * s)))
        pygame.draw.circle(surf, BLACK, _p(cx, cy, s, ex, -156), max(1, int(3 * s)))
    # Mund & Zähne
    pygame.draw.rect(surf, WHITE, _r(cx, cy, s, -7, -141, 5, 6))
    pygame.draw.rect(surf, WHITE, _r(cx, cy, s, 2, -141, 5, 6))


def draw_ork(surf, cx, cy, s=1.0):
    # Schatten
    pygame.draw.ellipse(surf, (20, 35, 20), _r(cx, cy, s, -44, -5, 88, 16))
    # Beine (massig)
    pygame.draw.rect(surf, (25, 85, 25), _r(cx, cy, s, -30, -64, 24, 64))
    pygame.draw.rect(surf, (25, 85, 25), _r(cx, cy, s, 6, -64, 24, 64))
    # Knie-Platten
    pygame.draw.rect(surf, LIGHT_GRAY, _r(cx, cy, s, -32, -46, 28, 12))
    pygame.draw.rect(surf, LIGHT_GRAY, _r(cx, cy, s, 4, -46, 28, 12))
    # Körper
    pygame.draw.ellipse(surf, (45, 115, 45), _r(cx, cy, s, -48, -192, 96, 132))
    # Gürtel
    pygame.draw.rect(surf, DARK_BROWN, _r(cx, cy, s, -42, -82, 84, 14))
    # Arme (massig)
    pygame.draw.line(surf, (45, 115, 45), _p(cx, cy, s, -48, -158), _p(cx, cy, s, -68, -108), max(1, int(18 * s)))
    pygame.draw.line(surf, (45, 115, 45), _p(cx, cy, s, 48, -158), _p(cx, cy, s, 68, -108), max(1, int(18 * s)))
    # Axt
    pygame.draw.line(surf, DARK_BROWN, _p(cx, cy, s, 68, -108), _p(cx, cy, s, 82, -68), max(1, int(6 * s)))
    pygame.draw.polygon(surf, SILVER, [
        _p(cx, cy, s, 74, -78), _p(cx, cy, s, 102, -92), _p(cx, cy, s, 98, -58)])
    pygame.draw.polygon(surf, GRAY, [
        _p(cx, cy, s, 74, -78), _p(cx, cy, s, 102, -92), _p(cx, cy, s, 98, -58)], 1)
    # Schild
    pygame.draw.rect(surf, DARK_RED, _r(cx, cy, s, -82, -140, 28, 55))
    pygame.draw.rect(surf, RED, _r(cx, cy, s, -82, -140, 28, 55), 2)
    pygame.draw.line(surf, GOLD, _p(cx, cy, s, -68, -140), _p(cx, cy, s, -68, -85), max(1, int(2 * s)))
    # Kopf
    pygame.draw.ellipse(surf, (45, 115, 45), _r(cx, cy, s, -38, -250, 76, 70))
    # Stirnrunzeln
    pygame.draw.line(surf, (25, 75, 25), _p(cx, cy, s, -28, -228), _p(cx, cy, s, -8, -222), max(1, int(3 * s)))
    pygame.draw.line(surf, (25, 75, 25), _p(cx, cy, s, 28, -228), _p(cx, cy, s, 8, -222), max(1, int(3 * s)))
    # Augen
    for ex in (-14, 14):
        pygame.draw.circle(surf, RED, _p(cx, cy, s, ex, -222), max(1, int(9 * s)))
        pygame.draw.circle(surf, DARK_RED, _p(cx, cy, s, ex, -222), max(1, int(4 * s)))
    # Stoßzähne
    pygame.draw.polygon(surf, WHITE, [
        _p(cx, cy, s, -14, -200), _p(cx, cy, s, -8, -200), _p(cx, cy, s, -11, -184)])
    pygame.draw.polygon(surf, WHITE, [
        _p(cx, cy, s, 8, -200), _p(cx, cy, s, 14, -200), _p(cx, cy, s, 11, -184)])
    # Hörner
    pygame.draw.polygon(surf, (35, 10, 10), [
        _p(cx, cy, s, -20, -246), _p(cx, cy, s, -32, -274), _p(cx, cy, s, -8, -243)])
    pygame.draw.polygon(surf, (35, 10, 10), [
        _p(cx, cy, s, 20, -246), _p(cx, cy, s, 32, -274), _p(cx, cy, s, 8, -243)])


def draw_waechter(surf, cx, cy, s=1.0):
    # Schatten
    pygame.draw.ellipse(surf, (30, 30, 40), _r(cx, cy, s, -40, -5, 80, 14))
    # Beine mit Rüstung
    pygame.draw.rect(surf, SILVER, _r(cx, cy, s, -22, -72, 18, 72))
    pygame.draw.rect(surf, SILVER, _r(cx, cy, s, 4, -72, 18, 72))
    pygame.draw.rect(surf, LIGHT_GRAY, _r(cx, cy, s, -24, -52, 22, 12))
    pygame.draw.rect(surf, LIGHT_GRAY, _r(cx, cy, s, 2, -52, 22, 12))
    pygame.draw.rect(surf, DARK_GRAY, _r(cx, cy, s, -25, -22, 22, 22))
    pygame.draw.rect(surf, DARK_GRAY, _r(cx, cy, s, 3, -22, 22, 22))
    # Umhang
    pygame.draw.polygon(surf, DARK_RED, [
        _p(cx, cy, s, -35, -178), _p(cx, cy, s, -52, -42),
        _p(cx, cy, s, -30, -42), _p(cx, cy, s, -18, -182)])
    # Körper (Plattenrüstung)
    pygame.draw.rect(surf, SILVER, _r(cx, cy, s, -36, -186, 72, 116))
    pygame.draw.line(surf, GRAY, _p(cx, cy, s, 0, -186), _p(cx, cy, s, 0, -72), max(1, int(2 * s)))
    pygame.draw.ellipse(surf, LIGHT_GRAY, _r(cx, cy, s, -20, -168, 40, 30))
    # Arme
    pygame.draw.rect(surf, SILVER, _r(cx, cy, s, -56, -182, 20, 80))
    pygame.draw.rect(surf, SILVER, _r(cx, cy, s, 36, -182, 20, 80))
    # Speer
    pygame.draw.line(surf, BROWN, _p(cx, cy, s, 56, -205), _p(cx, cy, s, 56, 20), max(1, int(5 * s)))
    pygame.draw.polygon(surf, SILVER, [
        _p(cx, cy, s, 49, -225), _p(cx, cy, s, 56, -245), _p(cx, cy, s, 63, -225)])
    # Schild
    pygame.draw.rect(surf, BLUE, _r(cx, cy, s, -84, -175, 30, 56))
    pygame.draw.rect(surf, SILVER, _r(cx, cy, s, -84, -175, 30, 56), 2)
    pygame.draw.line(surf, GOLD, _p(cx, cy, s, -69, -175), _p(cx, cy, s, -69, -119), max(1, int(2 * s)))
    pygame.draw.line(surf, GOLD, _p(cx, cy, s, -84, -147), _p(cx, cy, s, -54, -147), max(1, int(2 * s)))
    # Helm
    pygame.draw.ellipse(surf, SILVER, _r(cx, cy, s, -28, -256, 56, 56))
    pygame.draw.rect(surf, DARK_GRAY, _r(cx, cy, s, -18, -234, 36, 18))
    pygame.draw.rect(surf, RED, _r(cx, cy, s, -5, -266, 10, 20))
    pygame.draw.rect(surf, (200, 200, 50), _r(cx, cy, s, -15, -228, 12, 5))
    pygame.draw.rect(surf, (200, 200, 50), _r(cx, cy, s, 3, -228, 12, 5))


def draw_ork_koenig(surf, cx, cy, s=1.0):
    # Beine (massive dunkle Rüstung)
    pygame.draw.rect(surf, (55, 14, 14), _r(cx, cy, s, -36, -94, 28, 94))
    pygame.draw.rect(surf, (55, 14, 14), _r(cx, cy, s, 8, -94, 28, 94))
    # Knie-Spikes
    pygame.draw.polygon(surf, DARK_RED, [
        _p(cx, cy, s, -22, -68), _p(cx, cy, s, -14, -86), _p(cx, cy, s, -6, -68)])
    pygame.draw.polygon(surf, DARK_RED, [
        _p(cx, cy, s, 6, -68), _p(cx, cy, s, 14, -86), _p(cx, cy, s, 22, -68)])
    pygame.draw.rect(surf, BLACK, _r(cx, cy, s, -40, -24, 34, 24))
    pygame.draw.rect(surf, BLACK, _r(cx, cy, s, 6, -24, 34, 24))
    # Körper
    pygame.draw.ellipse(surf, (50, 14, 14), _r(cx, cy, s, -62, -250, 124, 160))
    pygame.draw.rect(surf, (38, 10, 10), _r(cx, cy, s, -52, -240, 104, 18))
    pygame.draw.rect(surf, (38, 10, 10), _r(cx, cy, s, -52, -210, 104, 18))
    # Schulter-Spikes
    pygame.draw.polygon(surf, RED, [
        _p(cx, cy, s, -62, -228), _p(cx, cy, s, -86, -260), _p(cx, cy, s, -40, -222)])
    pygame.draw.polygon(surf, RED, [
        _p(cx, cy, s, 62, -228), _p(cx, cy, s, 86, -260), _p(cx, cy, s, 40, -222)])
    # Arme
    pygame.draw.line(surf, (50, 14, 14), _p(cx, cy, s, -62, -218), _p(cx, cy, s, -96, -148), max(1, int(26 * s)))
    pygame.draw.line(surf, (50, 14, 14), _p(cx, cy, s, 62, -218), _p(cx, cy, s, 96, -148), max(1, int(26 * s)))
    pygame.draw.circle(surf, (38, 10, 10), _p(cx, cy, s, -96, -145), max(1, int(18 * s)))
    pygame.draw.circle(surf, (38, 10, 10), _p(cx, cy, s, 96, -145), max(1, int(18 * s)))
    # Riesenschwert (rechts)
    pygame.draw.rect(surf, DARK_GRAY, _r(cx, cy, s, 83, -220, 8, 164))
    pygame.draw.polygon(surf, SILVER, [
        _p(cx, cy, s, 78, -280), _p(cx, cy, s, 98, -280),
        _p(cx, cy, s, 93, -220), _p(cx, cy, s, 81, -220)])
    pygame.draw.line(surf, WHITE, _p(cx, cy, s, 87, -275), _p(cx, cy, s, 87, -225), max(1, int(2 * s)))
    pygame.draw.rect(surf, GOLD, _r(cx, cy, s, 67, -230, 40, 8))
    # Streitkolben (links)
    pygame.draw.line(surf, DARK_BROWN, _p(cx, cy, s, -96, -145), _p(cx, cy, s, -108, -74), max(1, int(7 * s)))
    pygame.draw.circle(surf, GRAY, _p(cx, cy, s, -110, -68), max(1, int(18 * s)))
    for a in range(0, 360, 60):
        spx = int(-110 + 18 * math.cos(math.radians(a)))
        spy = int(-68  + 18 * math.sin(math.radians(a)))
        pygame.draw.circle(surf, DARK_RED, _p(cx, cy, s, spx, spy), max(1, int(5 * s)))
    # Kopf
    pygame.draw.ellipse(surf, (58, 18, 18), _r(cx, cy, s, -52, -342, 104, 104))
    # Krone
    crown = [
        _p(cx, cy, s, -57, -334), _p(cx, cy, s, -57, -372),
        _p(cx, cy, s, -36, -354), _p(cx, cy, s, -15, -386),
        _p(cx, cy, s,  0,  -360), _p(cx, cy, s,  15, -386),
        _p(cx, cy, s,  36, -354), _p(cx, cy, s,  57, -372),
        _p(cx, cy, s,  57, -334),
    ]
    pygame.draw.polygon(surf, GOLD, crown)
    pygame.draw.polygon(surf, (170, 130, 0), crown, 2)
    for gx in (-40, 0, 40):
        pygame.draw.circle(surf, RED, _p(cx, cy, s, gx, -360), max(1, int(5 * s)))
    # Glühende Augen
    for ex in (-18, 18):
        pygame.draw.circle(surf, (150, 0, 0), _p(cx, cy, s, ex, -304), max(1, int(14 * s)))
        pygame.draw.circle(surf, (255, 60, 0), _p(cx, cy, s, ex, -304), max(1, int(9 * s)))
        pygame.draw.circle(surf, (255, 200, 0), _p(cx, cy, s, ex, -304), max(1, int(4 * s)))
    # Stirnrunzeln
    pygame.draw.line(surf, (30, 5, 5), _p(cx, cy, s, -36, -312), _p(cx, cy, s, -10, -304), max(1, int(4 * s)))
    pygame.draw.line(surf, (30, 5, 5), _p(cx, cy, s,  36, -312), _p(cx, cy, s,  10, -304), max(1, int(4 * s)))
    # Hauer
    pygame.draw.polygon(surf, WHITE, [
        _p(cx, cy, s, -20, -260), _p(cx, cy, s, -10, -260), _p(cx, cy, s, -14, -238)])
    pygame.draw.polygon(surf, WHITE, [
        _p(cx, cy, s,  10, -260), _p(cx, cy, s,  20, -260), _p(cx, cy, s,  14, -238)])
    # Hörner
    pygame.draw.polygon(surf, (38, 10, 10), [
        _p(cx, cy, s, -38, -334), _p(cx, cy, s, -60, -392), _p(cx, cy, s, -16, -327)])
    pygame.draw.polygon(surf, (38, 10, 10), [
        _p(cx, cy, s,  38, -334), _p(cx, cy, s,  60, -392), _p(cx, cy, s,  16, -327)])


DRAW_FUNCS = {
    "goblin":     draw_goblin,
    "ork":        draw_ork,
    "waechter":   draw_waechter,
    "ork_koenig": draw_ork_koenig,
}

# Höhe vom Boden bis zur Sprite-Spitze (für HP-Bar-Positionierung)
SPRITE_HEIGHTS = {
    "goblin":     186,
    "ork":        274,
    "waechter":   266,
    "ork_koenig": 392,
}


# ════════════════════════════════════════════════════════════
# UI-Klassen
# ════════════════════════════════════════════════════════════

class Button:
    def __init__(self, x, y, w, h, text, bg=DARK_GRAY, fg=WHITE,
                 hover=None, border=GRAY, fsize=19):
        self.rect    = pygame.Rect(x, y, w, h)
        self.text    = text
        self.bg      = bg
        self.fg      = fg
        self.hover_c = hover or tuple(min(c + 45, 255) for c in bg)
        self.border  = border
        self.font    = pygame.font.SysFont("Arial", fsize, bold=True)
        self.hovered = False
        self.enabled = True

    def update(self, mp):
        self.hovered = self.rect.collidepoint(mp)

    def draw(self, surf):
        if not self.enabled:
            col = tuple(c // 2 for c in self.bg)
        elif self.hovered:
            col = self.hover_c
        else:
            col = self.bg
        pygame.draw.rect(surf, col, self.rect, border_radius=6)
        pygame.draw.rect(surf, self.border, self.rect, 2, border_radius=6)
        label = self.font.render(self.text, True, self.fg if self.enabled else GRAY)
        surf.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, ev):
        return (self.enabled
                and ev.type == pygame.MOUSEBUTTONDOWN
                and ev.button == 1
                and self.rect.collidepoint(ev.pos))


class DialogBox:
    def __init__(self):
        self.msgs    = []          # list of (text, color)
        self.offset  = 0
        self.visible = 6
        self.font    = pygame.font.SysFont("Arial", 17)
        self.tfont   = pygame.font.SysFont("Arial", 19, bold=True)

    def add(self, text, color=LIGHT_GRAY):
        self.msgs.append((str(text), color))
        if len(self.msgs) > 300:
            self.msgs.pop(0)
        self.offset = max(0, len(self.msgs) - self.visible)

    def scroll(self, d):
        self.offset = max(0, min(max(0, len(self.msgs) - self.visible), self.offset + d))

    def draw(self, surf):
        r = DIALOG_RECT
        pygame.draw.rect(surf, (13, 8, 3), r)
        pygame.draw.rect(surf, (80, 55, 12), r, 2)
        # Titelleiste
        pygame.draw.rect(surf, (34, 22, 6), (r.x, r.y, r.width, 23))
        surf.blit(self.tfont.render("Ereignisse", True, GOLD), (r.x + 8, r.y + 3))
        # Nachrichten
        y = r.y + 26
        for text, color in self.msgs[self.offset:self.offset + self.visible]:
            surf.blit(self.font.render(text[:115], True, color), (r.x + 10, y))
            y += 24
        # Scrollleiste
        if len(self.msgs) > self.visible:
            bh = r.height - 23
            th = max(16, bh * self.visible // len(self.msgs))
            ty = r.y + 23 + int((bh - th) * self.offset / max(1, len(self.msgs) - self.visible))
            pygame.draw.rect(surf, DARK_GRAY, (r.right - 7, r.y + 23, 5, bh))
            pygame.draw.rect(surf, GOLD, (r.right - 7, ty, 5, th))


# ════════════════════════════════════════════════════════════
# Haupt-Spielklasse
# ════════════════════════════════════════════════════════════

class Game:
    S_START = "start"
    S_TUTOR = "tutorial"
    S_PLAY  = "play"
    S_INV   = "inventory"
    S_HELP  = "help"
    S_INFO  = "info"
    S_DEAD  = "dead"
    S_WIN   = "win"

    TUTORS = [
        ("Willkommen im Ödland, {}!",
         "Das Ödland leidet unter der Herrschaft des grausamen Ork-Königs.\n"
         "Deine Aufgabe: Kämpfe dich auf der 5×5-Karte bis zu ihm vor und besiege ihn!"),
        ("Bewegung & Kampf",
         "WASD oder Pfeiltasten bewegen dich durch den Dungeon.\n"
         "Du kannst Räume jederzeit verlassen – auch mitten im Kampf.\n"
         "[F] angreifen  |  [R] rasten (nur ohne Feinde)  |  [P] Beute aufheben"),
        ("Inventar & Ausrüstung",
         "[E] öffnet das Inventar – hier rüstest du Waffen und Rüstungen aus.\n"
         "Heiltränke stellen verlorene HP wieder her (bis zu deinem Maximum).\n"
         "Besiegte Feinde lassen Beute fallen – heb sie mit [P] auf."),
        ("Levelsystem",
         "Jeder besiegte Feind bringt Erfahrungspunkte (XP).\n"
         "Level 1→2 kostet 120 XP, Level 2→3 kostet 240 XP, usw.\n"
         "Pro Level: +30 Max-HP, +8 ATK-Basis – HP wird dabei vollständig aufgefüllt!"),
        ("Viel Erfolg, {}!",
         "[H] zeigt die Hilfe, [I] zeigt alle Monster mit ihren Werten.\n"
         "Die Minimap: Gold = du, Grün = gesäubert, Rot = Feinde.\n"
         "Klick oder [Leertaste] zum Beginnen!"),
    ]

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Die PentagonQuest")
        self.screen = pygame.display.set_mode((SW, SH))
        self.clock  = pygame.time.Clock()
        self.tick   = 0

        self.fnt_sm  = pygame.font.SysFont("Arial", 16)
        self.fnt_md  = pygame.font.SysFont("Arial", 20)
        self.fnt_lg  = pygame.font.SysFont("Arial", 30, bold=True)
        self.fnt_xl  = pygame.font.SysFont("Arial", 52, bold=True)
        self.fnt_hud = pygame.font.SysFont("Arial", 18, bold=True)

        self.state    = self.S_START
        self.player   = None
        self.gmap     = None
        self.dialog   = DialogBox()
        self.t_step   = 0
        self.name_str = ""
        self.inv_sel  = None
        self.inv_msg  = ""

        self._build_buttons()

    def _build_buttons(self):
        # Startbildschirm
        self.btn_start = Button(SW // 2 - 105, 490, 210, 52, "Spiel starten",
                                (65, 32, 8), WHITE, border=GOLD, fsize=22)

        # Navigation (NAV_RECT: 875,330,280,175 → Mitte: 1015,417)
        nc = (1015, 412)
        bs = 48
        self.btn_up  = Button(nc[0]-bs//2, nc[1]-85, bs, bs, "↑", DARK_STONE, WHITE, border=LIGHT_STONE, fsize=22)
        self.btn_dn  = Button(nc[0]-bs//2, nc[1]+10, bs, bs, "↓", DARK_STONE, WHITE, border=LIGHT_STONE, fsize=22)
        self.btn_lt  = Button(nc[0]-bs-12, nc[1]-37, bs, bs, "←", DARK_STONE, WHITE, border=LIGHT_STONE, fsize=22)
        self.btn_rt  = Button(nc[0]+12,   nc[1]-37, bs, bs, "→", DARK_STONE, WHITE, border=LIGHT_STONE, fsize=22)
        self.nav_btns = [self.btn_up, self.btn_dn, self.btn_lt, self.btn_rt]

        # Aktionen (y=510)
        self.btn_fight = Button(875,  510, 118, 32, "⚔ Kämpfen",     (100, 18, 18), WHITE, border=RED)
        self.btn_rest  = Button(997,  510, 118, 32, "💤 Rasten",       (18, 60, 18),  WHITE, border=GREEN)
        self.btn_inv   = Button(1119, 510, 100, 32, "🎒 Inv [E]",      (25, 25, 90),  WHITE, border=BLUE, fsize=15)
        self.btn_help  = Button(1223, 510, 60,  32, "? [H]",           (50, 35, 10),  WHITE, border=GOLD, fsize=14)
        self.btn_info  = Button(1226, 546, 54,  28, "I [I]",           (20, 40, 75),  WHITE, border=BLUE, fsize=14)
        self.act_btns  = [self.btn_fight, self.btn_rest, self.btn_inv, self.btn_help, self.btn_info]

        # Beute aufheben
        self.btn_pick = Button(875, 510, 260, 32, "⬆ Gegenstand aufheben  [P]",
                               (55, 45, 10), WHITE, border=GOLD, fsize=16)

        # Inventar-Buttons (Positionen werden in _draw_inv gesetzt)
        self.btn_equip = Button(0, 0, 155, 42, "Ausrüsten",  (55, 38, 10), WHITE)
        self.btn_use   = Button(0, 0, 155, 42, "Benutzen",   (10, 55, 10), WHITE)
        self.btn_drop  = Button(0, 0, 155, 42, "Ablegen",    (75, 10, 10), WHITE)
        self.btn_close = Button(0, 0, 130, 36, "✕ Schließen", (65, 10, 10), WHITE)
        self.inv_btns  = [self.btn_equip, self.btn_use, self.btn_drop, self.btn_close]

    # ── Haupt-Loop ───────────────────────────────────────────

    def run(self):
        while True:
            self.clock.tick(60)
            self.tick += 1
            events = pygame.event.get()
            mp     = pygame.mouse.get_pos()

            for ev in events:
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEWHEEL and self.state == self.S_PLAY:
                    self.dialog.scroll(-ev.y)

            handlers = {
                self.S_START: (self._handle_start, self._draw_start),
                self.S_TUTOR: (self._handle_tutor, self._draw_tutor),
                self.S_PLAY:  (self._handle_play,  self._draw_play),
                self.S_INV:   (self._handle_inv,   self._draw_inv),
                self.S_HELP:  (self._handle_help,  self._draw_help),
                self.S_INFO:  (self._handle_info,  self._draw_info),
                self.S_DEAD:  (self._handle_end,   self._draw_dead),
                self.S_WIN:   (self._handle_end,   self._draw_win),
            }
            handle, draw = handlers[self.state]
            handle(events, mp)
            draw()
            pygame.display.flip()

    # ── Startbildschirm ──────────────────────────────────────

    def _handle_start(self, events, mp):
        self.btn_start.update(mp)
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN and self.name_str.strip():
                    self._begin()
                elif ev.key == pygame.K_BACKSPACE:
                    self.name_str = self.name_str[:-1]
                elif len(self.name_str) < 20 and ev.unicode.isprintable() and ev.unicode != "":
                    self.name_str += ev.unicode
            if self.btn_start.clicked(ev) and self.name_str.strip():
                self._begin()

    def _begin(self):
        self.player = Player(self.name_str.strip())
        self.gmap   = GameMap()
        self.t_step = 0
        self.state  = self.S_TUTOR

    def _draw_start(self):
        s = self.screen
        s.fill((4, 2, 8))
        fl = int(math.sin(self.tick * 0.05) * 18)
        # Atmosphärische Hintergrundstreifen
        for xi in range(0, SW, 80):
            dark = abs(xi - SW // 2) / (SW // 2)
            c = int(28 * (1 - dark))
            pygame.draw.rect(s, (c, c // 2, c // 3), (xi, 0, 80, SH))

        title_font = pygame.font.SysFont("Arial", 74, bold=True)
        t = title_font.render("DIE PENTAGON QUEST", True, (208 + fl, 165 + fl // 2, 32))
        s.blit(t, t.get_rect(centerx=SW // 2, y=100))
        sub = self.fnt_lg.render("Ein Dungeon-Abenteuer", True, LIGHT_GRAY)
        s.blit(sub, sub.get_rect(centerx=SW // 2, y=190))

        pygame.draw.line(s, GOLD, (SW // 2 - 210, 368), (SW // 2 + 210, 368), 1)
        pr = self.fnt_md.render("Dein Name, Fremder:", True, LIGHT_GRAY)
        s.blit(pr, pr.get_rect(centerx=SW // 2, y=322))
        cursor = "|" if self.tick % 60 < 30 else ""
        ns = self.fnt_lg.render(self.name_str + cursor, True, WHITE)
        s.blit(ns, ns.get_rect(centerx=SW // 2, y=380))
        hint = self.fnt_sm.render("Name eingeben und Enter drücken oder Button klicken", True, GRAY)
        s.blit(hint, hint.get_rect(centerx=SW // 2, y=448))
        self.btn_start.draw(s)
        cr = self.fnt_sm.render("Original: Kevin Küster  |  Grafische Version: Claude", True, DARK_GRAY)
        s.blit(cr, cr.get_rect(centerx=SW // 2, y=SH - 26))

    # ── Tutorial ─────────────────────────────────────────────

    def _handle_tutor(self, events, mp):
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_SPACE, pygame.K_RETURN):
                self._next_tutor()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self._next_tutor()

    def _next_tutor(self):
        self.t_step += 1
        if self.t_step >= len(self.TUTORS):
            self.state = self.S_PLAY
            self._enter_room()

    def _draw_tutor(self):
        s = self.screen
        s.fill((6, 3, 10))
        pygame.draw.rect(s, DARK_STONE, (70, 65, SW - 140, SH - 130))
        pygame.draw.rect(s, STONE, (70, 65, SW - 140, SH - 130), 4)

        step = min(self.t_step, len(self.TUTORS) - 1)
        title_raw, body = self.TUTORS[step]
        title = title_raw.format(self.player.name)

        t = self.fnt_xl.render(title, True, GOLD)
        s.blit(t, t.get_rect(centerx=SW // 2, y=118))

        y = 218
        for line in body.split('\n'):
            ls = self.fnt_md.render(line, True, WHITE)
            s.blit(ls, ls.get_rect(centerx=SW // 2, y=y))
            y += 50

        # Fortschritts-Dots
        n = len(self.TUTORS)
        for i in range(n):
            col = GOLD if i == step else GRAY
            pygame.draw.circle(s, col, (SW // 2 - (n - 1) * 16 + i * 32, SH - 118), 9)

        cont = "Starten! (Klick oder Leertaste)" if step == n - 1 else "Weiter  (Klick oder Leertaste)"
        hs = self.fnt_md.render(cont, True, LIGHT_GRAY)
        s.blit(hs, hs.get_rect(centerx=SW // 2, y=SH - 88))

    # ── Spiellogik ───────────────────────────────────────────

    def _enter_room(self):
        f    = self.gmap.field
        x, y = self.gmap.x, self.gmap.y
        if f.enemies:
            names = ", ".join(e.name for e in f.enemies)
            self.dialog.add(f"Raum ({x},{y}) – Feinde: {names}!", RED)
        else:
            self.dialog.add(f"Raum ({x},{y}) – kein Feind in Sicht.", GREEN)
        if f.loot:
            self.dialog.add(f"Beute liegt herum: {', '.join(i.name for i in f.loot)}", YELLOW)

    def _handle_play(self, events, mp):
        f            = self.gmap.field
        has_enemies  = bool(f.enemies)
        has_loot     = bool(f.loot)

        for btn in self.nav_btns + self.act_btns + [self.btn_pick]:
            btn.update(mp)

        self.btn_fight.enabled = has_enemies
        self.btn_rest.enabled  = not has_enemies
        in_combat = f.combat_started and bool(f.enemies)
        self.btn_up.enabled    = not in_combat and self.gmap.can_move(1, 0)
        self.btn_dn.enabled    = not in_combat and self.gmap.can_move(-1, 0)
        self.btn_lt.enabled    = not in_combat and self.gmap.can_move(0, -1)
        self.btn_rt.enabled    = not in_combat and self.gmap.can_move(0, 1)

        for ev in events:
            if ev.type == pygame.KEYDOWN:
                k = ev.key
                if   k in (pygame.K_w, pygame.K_UP):    self._move(1, 0)
                elif k in (pygame.K_s, pygame.K_DOWN):  self._move(-1, 0)
                elif k in (pygame.K_a, pygame.K_LEFT):  self._move(0, -1)
                elif k in (pygame.K_d, pygame.K_RIGHT): self._move(0, 1)
                elif k == pygame.K_f:                   self._fight()
                elif k == pygame.K_r and not has_enemies: self._rest()
                elif k == pygame.K_e:                   self.state = self.S_INV
                elif k == pygame.K_p and has_loot:      self._pickup()
                elif k == pygame.K_h:                   self.state = self.S_HELP
                elif k == pygame.K_i:                   self.state = self.S_INFO

            if self.btn_up.clicked(ev):    self._move(1, 0)
            if self.btn_dn.clicked(ev):    self._move(-1, 0)
            if self.btn_lt.clicked(ev):    self._move(0, -1)
            if self.btn_rt.clicked(ev):    self._move(0, 1)
            if self.btn_fight.clicked(ev): self._fight()
            if self.btn_rest.clicked(ev):  self._rest()
            if self.btn_inv.clicked(ev):   self.state = self.S_INV
            if self.btn_help.clicked(ev):  self.state = self.S_HELP
            if self.btn_info.clicked(ev):  self.state = self.S_INFO
            if self.btn_pick.clicked(ev) and has_loot: self._pickup()

        if self.player.is_dead():  self.state = self.S_DEAD
        if self.gmap.boss_dead():  self.state = self.S_WIN

    def _move(self, dx, dy):
        f = self.gmap.field
        if f.combat_started and f.enemies:
            self.dialog.add("Kampf gestartet – besiege alle Feinde bevor du fliehst!", RED)
            return
        wall_msgs = {
            ( 1,  0): "Massive Felswände versperren den Weg vorwärts.",
            (-1,  0): "Tiefe Klippen versperren den Rückweg.",
            ( 0, -1): "Unüberquerbares Gebirge zu deiner Linken.",
            ( 0,  1): "Unüberquerbares Gebirge zu deiner Rechten.",
        }
        if not self.gmap.move(dx, dy):
            self.dialog.add(wall_msgs.get((dx, dy), "Kein Durchkommen."), GRAY)
        else:
            self._enter_room()

    def _fight(self):
        field   = self.gmap.field
        enemies = field.enemies
        if not enemies:
            return
        field.combat_started = True
        t = enemies[0]
        t.get_hit(self.player.ad)
        self.dialog.add(
            f"Du triffst {t.name} für {self.player.ad} Schaden!  ({t.hp}/{t.max_hp} HP)",
            (255, 190, 80))
        if t.is_dead():
            drop = t.get_drop()
            for item in drop:
                self.gmap.field.loot.append(item)
            enemies.remove(t)
            lvl_msgs = self.player.gain_xp(t.xp)
            self.dialog.add(f"{t.name} besiegt! +{t.xp} XP", GREEN)
            if drop:
                self.dialog.add(f"Beute: {', '.join(i.name for i in drop)}", YELLOW)
            for m in lvl_msgs:
                self.dialog.add(m, GOLD)
        for e in list(enemies):
            dmg = self.player.get_hit(e.ad)
            self.dialog.add(
                f"{e.name} trifft dich für {dmg}!  ({self.player.hp}/{self.player.max_hp} HP)",
                (255, 90, 90))
            if self.player.is_dead():
                self.dialog.add("Du bist gestorben!", RED)
                break
        if not enemies:
            self.dialog.add("Alle Feinde besiegt! Du kannst dich jetzt ausruhen.", (100, 255, 100))

    def _rest(self):
        self.player.rest()
        self.dialog.add(f"Du rastest aus. HP vollständig aufgefüllt: {self.player.max_hp}", GREEN)

    def _pickup(self):
        loot = self.gmap.field.loot
        if not loot:
            return
        if len(self.player.inv) >= self.player.max_inv:
            self.dialog.add("Inventar voll! Lege zuerst etwas ab.", RED)
            return
        item = loot.pop(0)
        self.player.inv.append(item)
        self.dialog.add(f"'{item.name}' aufgehoben und ins Inventar gelegt.", YELLOW)

    # ── Zeichnen: Hauptspiel ──────────────────────────────────

    def _draw_play(self):
        self.screen.fill(BLACK)
        self._draw_hud()
        self._draw_dungeon()
        self._draw_minimap()
        self._draw_nav()
        self._draw_actions()
        self.dialog.draw(self.screen)

    def _draw_hud(self):
        s = self.screen
        p = self.player
        pygame.draw.rect(s, (18, 9, 3), HUD_RECT)
        pygame.draw.rect(s, (62, 40, 10), HUD_RECT, 2)

        nm = self.fnt_hud.render(p.name, True, GOLD)
        s.blit(nm, (8, 15))

        bx, by, bw, bh = 160, 12, 340, 26
        ratio = p.hp / p.max_hp if p.max_hp > 0 else 0
        pygame.draw.rect(s, DARK_RED, (bx, by, bw, bh), border_radius=4)
        if ratio > 0:
            pygame.draw.rect(s, RED, (bx, by, int(bw * ratio), bh), border_radius=4)
        pygame.draw.rect(s, WHITE, (bx, by, bw, bh), 1, border_radius=4)
        ht = self.fnt_hud.render(f"HP  {p.hp} / {p.max_hp}", True, WHITE)
        s.blit(ht, ht.get_rect(centerx=bx + bw // 2, centery=by + bh // 2))

        # XP-Balken
        xp_needed = p.xp_needed()
        xp_ratio  = min(1.0, p.xp / xp_needed)
        xbx, xby, xbw, xbh = 512, 6, 200, 10
        pygame.draw.rect(s, (30, 20, 5), (xbx, xby, xbw, xbh), border_radius=3)
        if xp_ratio > 0:
            pygame.draw.rect(s, GOLD, (xbx, xby, int(xbw * xp_ratio), xbh), border_radius=3)
        pygame.draw.rect(s, (80, 65, 20), (xbx, xby, xbw, xbh), 1, border_radius=3)

        stats = (f"ATK {p.ad}   DEF {p.defense}   Lv {p.level}"
                 f"   XP {p.xp}/{xp_needed}")
        s.blit(self.fnt_sm.render(stats, True, LIGHT_GRAY), (512, 20))
        if p.eq_weapon:
            ws = self.fnt_sm.render(f"⚔ {p.eq_weapon.name}", True, YELLOW)
            s.blit(ws, (752, 30))

    def _draw_dungeon(self):
        s = self.screen
        r = DUNGEON_RECT

        # Decke (Farbverlauf)
        ch = r.height * 2 // 5
        for i in range(ch):
            t = i / ch
            c = (int(26 + 20 * t), int(20 + 14 * t), int(16 + 10 * t))
            pygame.draw.line(s, c, (r.x, r.y + i), (r.right, r.y + i))

        # Boden (Farbverlauf)
        fy = r.y + r.height * 3 // 5
        fh = r.height - r.height * 3 // 5
        for i in range(fh):
            t = 1 - i / fh
            c = (int(16 + 34 * t), int(13 + 28 * t), int(10 + 22 * t))
            pygame.draw.line(s, c, (r.x, fy + i), (r.right, fy + i))

        hor = r.y + ch
        vx  = r.x + r.width // 2

        # Seitenwände (Trapeze)
        lw = [(r.x, r.y), (r.x + r.width // 4, hor),
              (r.x + r.width // 4, r.y + r.height * 3 // 5), (r.x, r.bottom)]
        rw = [(r.right, r.y), (r.x + r.width * 3 // 4, hor),
              (r.x + r.width * 3 // 4, r.y + r.height * 3 // 5), (r.right, r.bottom)]
        for wall in (lw, rw):
            pygame.draw.polygon(s, (30, 26, 22), wall)
            pygame.draw.polygon(s, STONE, wall, 2)

        # Rückwand
        bk = pygame.Rect(r.x + r.width // 4, r.y, r.width // 2, r.height * 3 // 5)
        pygame.draw.rect(s, DARK_STONE, bk)
        # Steinquader-Textur
        for bx2 in range(bk.x, bk.right, 68):
            for by2 in range(bk.y, bk.bottom, 34):
                row = (by2 - bk.y) // 34
                ox  = 34 if row % 2 else 0
                pygame.draw.rect(s, STONE, (bx2 + ox, by2, 65, 31), 1)

        # Ausgänge (Türen/Durchgänge)
        door_bg = (3, 2, 7)
        if self.gmap.can_move(1, 0):  # vorwärts
            dw, dh = 80, 130
            pygame.draw.rect(s, door_bg, (vx - dw // 2, bk.bottom - dh, dw, dh))
            pygame.draw.rect(s, (52, 44, 34), (vx - dw // 2, bk.bottom - dh, dw, dh), 2)
            lbl = self.fnt_sm.render("W↑", True, GOLD)
            s.blit(lbl, lbl.get_rect(centerx=vx, y=bk.bottom - dh + 4))
        if self.gmap.can_move(0, -1):  # links
            pts = [(r.x, r.y + r.height // 3), (r.x + r.width // 4 + 8, hor + 20),
                   (r.x + r.width // 4 + 8, r.y + r.height * 3 // 5 - 18), (r.x, r.y + r.height * 2 // 3)]
            pygame.draw.polygon(s, door_bg, pts)
            lbl = self.fnt_sm.render("←A", True, GOLD)
            s.blit(lbl, (r.x + 14, r.y + r.height // 2 - 8))
        if self.gmap.can_move(0, 1):   # rechts
            pts = [(r.right, r.y + r.height // 3), (r.x + r.width * 3 // 4 - 8, hor + 20),
                   (r.x + r.width * 3 // 4 - 8, r.y + r.height * 3 // 5 - 18), (r.right, r.y + r.height * 2 // 3)]
            pygame.draw.polygon(s, door_bg, pts)
            lbl = self.fnt_sm.render("D→", True, GOLD)
            s.blit(lbl, (r.right - 32, r.y + r.height // 2 - 8))

        # Fackeln
        for tx in (r.x + r.width // 4 + 14, r.x + r.width * 3 // 4 - 34):
            ty = hor - 30
            fl = int(math.sin(self.tick * 0.09) * 9)
            tc = (212 + fl, 108 + fl // 2, 16)
            pygame.draw.rect(s, DARK_BROWN, (tx, ty, 7, 28))
            for fi in range(5, 0, -1):
                fc = (min(255, tc[0]), min(255, tc[1] + fi * 5), 0)
                pygame.draw.circle(s, fc, (tx + 3, ty - fi * 3 + fl // 2), fi * 3)
            # Lichtschein
            glow = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(glow, (220, 110, 20, 28), (25, 25), 25)
            s.blit(glow, (tx - 22, ty - 28))

        # Monster zeichnen
        enemies = self.gmap.field.enemies
        if enemies:
            n  = len(enemies)
            sp = min(190, bk.width // (n + 1))
            sx = vx - (n - 1) * sp // 2
            for i, e in enumerate(enemies):
                ex  = sx + i * sp
                ey  = bk.bottom - 2
                scl_map = {"goblin": 0.44, "ork": 0.54, "waechter": 0.50, "ork_koenig": 0.62}
                sc  = scl_map.get(e.sprite, 0.50) * (0.74 if n > 2 else 1.0)
                fn  = DRAW_FUNCS.get(e.sprite)
                if fn:
                    fn(s, ex, ey, sc)
                # HP-Balken über dem Monster
                h_total = SPRITE_HEIGHTS.get(e.sprite, 200)
                bar_y   = ey - int(h_total * sc) - 16
                bw2     = int(78 * sc / 0.5)
                bx2     = ex - bw2 // 2
                ratio2  = e.hp / e.max_hp if e.max_hp > 0 else 0
                pygame.draw.rect(s, DARK_RED, (bx2, bar_y, bw2, 9), border_radius=2)
                if ratio2 > 0:
                    pygame.draw.rect(s, RED, (bx2, bar_y, int(bw2 * ratio2), 9), border_radius=2)
                pygame.draw.rect(s, WHITE, (bx2, bar_y, bw2, 9), 1, border_radius=2)
                lbl_txt = f"{e.name}  {e.hp}/{e.max_hp}"
                lbl     = self.fnt_sm.render(lbl_txt, True, WHITE)
                lr      = lbl.get_rect(centerx=ex, bottom=bar_y - 2)
                sh_lbl  = self.fnt_sm.render(lbl_txt, True, BLACK)
                s.blit(sh_lbl, (lr.x + 1, lr.y + 1))
                s.blit(lbl, lr)
        else:
            cs = self.fnt_lg.render("Raum gesäubert", True, (52, 74, 52))
            s.blit(cs, cs.get_rect(centerx=r.centerx, centery=r.centery - 18))

        # Beute am Boden
        loot = self.gmap.field.loot
        if loot:
            ly = r.bottom - 90
            pygame.draw.circle(s, (72, 62, 0), (vx, ly + 14), 20)
            pygame.draw.circle(s, GOLD, (vx, ly + 14), 10)
            lt = self.fnt_md.render(f"Beute: {', '.join(i.name for i in loot)}", True, GOLD)
            s.blit(lt, lt.get_rect(centerx=r.centerx, y=ly + 36))
            ph = self.fnt_sm.render("[P] aufheben", True, LIGHT_GRAY)
            s.blit(ph, ph.get_rect(centerx=r.centerx, y=ly + 58))

        # Rand des Dungeonbereichs
        pygame.draw.rect(s, STONE, r, 3)

    def _draw_minimap(self):
        s  = self.screen
        mr = MINIMAP_RECT
        pygame.draw.rect(s, (8, 6, 4), mr)
        pygame.draw.rect(s, GOLD, mr, 2)

        s.blit(self.fnt_sm.render("Karte", True, GOLD), (mr.x + 6, mr.y + 5))

        m  = self.gmap
        cw = (mr.width - 22) // m.SIZE
        ch = (mr.height - 36) // m.SIZE
        ox = mr.x + 10
        oy = mr.y + 30

        for ix in range(m.SIZE):
            for iy in range(m.SIZE):
                cx2 = ox + iy * cw
                cy2 = oy + ix * ch
                f   = m.grid[ix][iy]
                cell_r = pygame.Rect(cx2 + 2, cy2 + 2, cw - 4, ch - 4)

                if not f.visited:
                    pygame.draw.rect(s, (16, 16, 16), cell_r)
                else:
                    if ix == m.x and iy == m.y:
                        col = GOLD
                    elif ix == m.SIZE - 1 and iy == m.SIZE - 1:
                        col = (130, 0, 0) if f.enemies else DARK_GREEN
                    elif not f.enemies:
                        col = DARK_GREEN
                    else:
                        col = DARK_RED
                    pygame.draw.rect(s, col, cell_r)
                    pygame.draw.rect(s, STONE, cell_r, 1)
                    if ix == m.x and iy == m.y:
                        pygame.draw.circle(s, WHITE, (cx2 + cw // 2, cy2 + ch // 2),
                                           min(cw, ch) // 3)
                    if ix == m.SIZE - 1 and iy == m.SIZE - 1 and f.enemies:
                        pygame.draw.polygon(s, RED, [
                            (cx2 + cw // 2, cy2 + 2),
                            (cx2 + cw - 2, cy2 + ch - 2),
                            (cx2 + 2, cy2 + ch - 2)])

        coord = self.fnt_sm.render(f"Position: ({m.x}, {m.y})   Ziel: (4, 4)", True, LIGHT_GRAY)
        s.blit(coord, (mr.x + 4, mr.bottom + 7))

    def _draw_nav(self):
        s  = self.screen
        nr = NAV_RECT
        pygame.draw.rect(s, (10, 8, 5), nr)
        pygame.draw.rect(s, DARK_STONE, nr, 2)
        nt = self.fnt_sm.render("Bewegung  –  WASD / Pfeiltasten", True, LIGHT_GRAY)
        s.blit(nt, (nr.x + 6, nr.y + 5))
        for btn in self.nav_btns:
            btn.draw(s)

    def _draw_actions(self):
        s  = self.screen
        ar = pygame.Rect(875, 504, 405, 40)
        pygame.draw.rect(s, (10, 8, 5), ar)
        for btn in self.act_btns:
            btn.draw(s)
        if self.gmap.field.loot:
            ph = self.fnt_sm.render("Beute im Raum!  [P] aufheben", True, YELLOW)
            s.blit(ph, (878, 546))
        kh = self.fnt_sm.render(
            "F: Kämpfen   R: Rasten   E: Inventar   P: Aufheben   H: Hilfe   I: Monsterinfo   WASD/↑↓←→: Bewegen",
            True, (68, 68, 68))
        s.blit(kh, (4, SH - 19))

    # ── Inventar ─────────────────────────────────────────────

    def _inv_slot_rect(self, idx):
        row = idx // INV_COLS
        col = idx % INV_COLS
        return pygame.Rect(INV_OX + col * (INV_SS + INV_GAP),
                           INV_OY + row * (INV_SS + INV_GAP),
                           INV_SS, INV_SS)

    def _handle_inv(self, events, mp):
        # Button-Positionen aktualisieren (konsistent mit _draw_inv)
        lp = pygame.Rect(10, 60, 540, 530)
        self.btn_equip.rect = pygame.Rect(lp.x + 15,  lp.y + 472, 155, 42)
        self.btn_use.rect   = pygame.Rect(lp.x + 180, lp.y + 472, 155, 42)
        self.btn_drop.rect  = pygame.Rect(lp.x + 345, lp.y + 472, 155, 42)
        self.btn_close.rect = pygame.Rect(lp.right - 138, lp.y + 8, 128, 36)

        for btn in self.inv_btns:
            btn.update(mp)

        p = self.player
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # Slot-Klick
                for idx in range(len(p.inv)):
                    if self._inv_slot_rect(idx).collidepoint(ev.pos):
                        self.inv_sel = idx
                        self.inv_msg = ""
                        break

                if self.btn_close.clicked(ev):
                    self.inv_sel = None
                    self.state   = self.S_PLAY

                sel = self.inv_sel
                if sel is not None and sel < len(p.inv):
                    item = p.inv[sel]
                    if self.btn_equip.clicked(ev):
                        self.inv_msg = p.equip(item)
                        self.dialog.add(self.inv_msg, YELLOW)
                    if self.btn_use.clicked(ev):
                        self.inv_msg = p.use_item(item)
                        self.dialog.add(self.inv_msg, GREEN)
                        self.inv_sel = None
                    if self.btn_drop.clicked(ev):
                        p.drop_item(item)
                        self.gmap.field.loot.append(item)
                        self.dialog.add(f"'{item.name}' abgelegt.", GRAY)
                        self.inv_sel = None
                        self.inv_msg = ""

            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_ESCAPE, pygame.K_e):
                self.inv_sel = None
                self.state   = self.S_PLAY

        # Selektion begrenzen
        if self.inv_sel is not None and self.inv_sel >= len(p.inv):
            self.inv_sel = None

        sel      = self.inv_sel
        has_sel  = sel is not None and sel < len(p.inv)
        sel_item = p.inv[sel] if has_sel else None
        self.btn_equip.enabled = has_sel and isinstance(sel_item, (Sword, Armor))
        self.btn_use.enabled   = has_sel and isinstance(sel_item, HPPlus)
        self.btn_drop.enabled  = has_sel

    def _draw_inv(self):
        s = self.screen

        # Abgedunkelter Hintergrund
        dim = pygame.Surface((SW, SH), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 178))
        s.blit(dim, (0, 0))

        # ─ Linkes Panel: Inventar ─
        lp = pygame.Rect(10, 60, 540, 530)
        pygame.draw.rect(s, (18, 13, 7), lp, border_radius=8)
        pygame.draw.rect(s, GOLD, lp, 2, border_radius=8)

        s.blit(self.fnt_lg.render("Inventar", True, GOLD), (lp.x + 14, lp.y + 10))
        p   = self.player
        cap = self.fnt_sm.render(f"{len(p.inv)}/{p.max_inv} Slots belegt", True, LIGHT_GRAY)
        s.blit(cap, (lp.x + 268, lp.y + 16))

        for idx in range(p.max_inv):
            sr  = self._inv_slot_rect(idx)
            sel = (idx == self.inv_sel)
            pygame.draw.rect(s, (40, 30, 18) if sel else (22, 15, 9), sr, border_radius=5)
            pygame.draw.rect(s, GOLD if sel else STONE, sr, 2, border_radius=5)

            if idx < len(p.inv):
                item = p.inv[idx]
                icx, icy = sr.centerx, sr.y + 36

                # Item-Icon
                if isinstance(item, Sword):
                    pygame.draw.line(s, SILVER, (icx, icy - 22), (icx, icy + 22), 4)
                    pygame.draw.line(s, SILVER, (icx - 13, icy - 4), (icx + 13, icy - 4), 3)
                    pygame.draw.polygon(s, LIGHT_GRAY, [(icx - 4, icy - 22), (icx + 4, icy - 22), (icx, icy - 34)])
                elif isinstance(item, HPPlus):
                    pygame.draw.ellipse(s, (168, 16, 16), (icx - 12, icy - 18, 24, 30))
                    pygame.draw.rect(s, (112, 88, 68), (icx - 5, icy - 27, 10, 10))
                    pygame.draw.line(s, WHITE, (icx - 4, icy - 10), (icx + 4, icy - 10), 2)
                elif isinstance(item, Armor):
                    pygame.draw.polygon(s, SILVER, [
                        (icx, icy - 22), (icx + 14, icy - 10),
                        (icx + 12, icy + 14), (icx - 12, icy + 14), (icx - 14, icy - 10)])
                else:
                    pygame.draw.circle(s, GOLD, (icx, icy), 14)

                # Ausgerüstet-Haken
                if item.equipped:
                    s.blit(self.fnt_sm.render("✓", True, GREEN), (sr.right - 17, sr.y + 3))

                # Item-Name
                nm_surf = self.fnt_sm.render(item.name[:16], True, WHITE)
                s.blit(nm_surf, nm_surf.get_rect(centerx=icx, y=sr.y + 62))
                if len(item.name) > 16:
                    nm2 = self.fnt_sm.render(item.name[16:32], True, WHITE)
                    s.blit(nm2, nm2.get_rect(centerx=icx, y=sr.y + 78))

                # Stat-Vorschau
                if isinstance(item, Sword):
                    st = self.fnt_sm.render(f"+{item.ad} ATK", True, ORANGE)
                elif isinstance(item, HPPlus):
                    st = self.fnt_sm.render(f"+{item.hp_plus} HP", True, GREEN)
                elif isinstance(item, Armor):
                    st = self.fnt_sm.render(f"+{item.defense} DEF", True, BLUE)
                else:
                    st = None
                if st:
                    s.blit(st, st.get_rect(centerx=icx, y=sr.bottom - 20))
            else:
                es = self.fnt_sm.render("Leer", True, DARK_GRAY)
                s.blit(es, es.get_rect(center=sr.center))

        # Aktions-Buttons
        self.btn_equip.rect = pygame.Rect(lp.x + 15,  lp.y + 472, 155, 42)
        self.btn_use.rect   = pygame.Rect(lp.x + 180, lp.y + 472, 155, 42)
        self.btn_drop.rect  = pygame.Rect(lp.x + 345, lp.y + 472, 155, 42)
        for btn in [self.btn_equip, self.btn_use, self.btn_drop]:
            btn.draw(s)

        # Schließen-Button
        self.btn_close.rect = pygame.Rect(lp.right - 138, lp.y + 8, 128, 36)
        self.btn_close.draw(s)

        # ─ Rechtes Panel: Status ─
        rp = pygame.Rect(562, 60, SW - 572, 530)
        pygame.draw.rect(s, (15, 10, 6), rp, border_radius=8)
        pygame.draw.rect(s, GOLD, rp, 2, border_radius=8)

        s.blit(self.fnt_lg.render("Charakter-Status", True, GOLD), (rp.x + 14, rp.y + 10))

        stat_rows = [
            ("Name",          p.name,                                         WHITE),
            ("Level",         str(p.level),                                   GOLD),
            ("Erfahrung",     f"{p.xp} / {p.xp_needed()} XP  →  Level {p.level + 1}",  LIGHT_GRAY),
            ("Lebenspunkte",  f"{p.hp} / {p.max_hp}",                         GREEN),
            ("Angriff",       str(p.ad),                                       ORANGE),
            ("Verteidigung",  str(p.defense),                                  BLUE),
            ("Waffe",         p.eq_weapon.name if p.eq_weapon else "keine",   YELLOW),
            ("Rüstung",       p.eq_armor.name  if p.eq_armor  else "keine",   SILVER),
        ]
        sy2 = rp.y + 52
        for label, val, col in stat_rows:
            ls = self.fnt_md.render(label + ":", True, LIGHT_GRAY)
            vs = self.fnt_md.render(val,         True, col)
            s.blit(ls, (rp.x + 16, sy2))
            s.blit(vs, (rp.x + 210, sy2))
            pygame.draw.line(s, (38, 26, 14), (rp.x + 12, sy2 + 30), (rp.right - 12, sy2 + 30))
            sy2 += 40

        # HP-Balken
        ratio = p.hp / p.max_hp if p.max_hp > 0 else 0
        br = pygame.Rect(rp.x + 16, sy2 + 6, min(420, rp.width - 32), 16)
        pygame.draw.rect(s, DARK_RED, br, border_radius=3)
        if ratio > 0:
            pygame.draw.rect(s, RED, (br.x, br.y, int(br.width * ratio), br.height), border_radius=3)
        pygame.draw.rect(s, WHITE, br, 1, border_radius=3)

        # Ausgewähltes Item Detail
        sel = self.inv_sel
        if sel is not None and sel < len(p.inv):
            item = p.inv[sel]
            dr = pygame.Rect(rp.x + 14, sy2 + 30, rp.width - 28, 100)
            pygame.draw.rect(s, (28, 20, 10), dr, border_radius=6)
            pygame.draw.rect(s, GOLD, dr, 1, border_radius=6)
            s.blit(self.fnt_md.render(f"Ausgewählt: {item.name[:28]}", True, GOLD),
                   (dr.x + 10, dr.y + 8))
            if isinstance(item, Sword):
                detail = f"Waffe  |  ATK +{item.ad}  |  Gewicht {item.weight}  |  Wert {item.worth} G"
            elif isinstance(item, HPPlus):
                detail = f"Heiltrank  |  HP +{item.hp_plus}  |  Einmalig verwendbar"
            elif isinstance(item, Armor):
                detail = f"Rüstung  |  DEF +{item.defense}  |  Gewicht {item.weight}"
            else:
                detail = "Unbekanntes Item"
            s.blit(self.fnt_sm.render(detail, True, WHITE), (dr.x + 10, dr.y + 38))
            if item.equipped:
                s.blit(self.fnt_sm.render("★ Derzeit ausgerüstet", True, GREEN), (dr.x + 10, dr.y + 62))

        # Feedback-Meldung
        if self.inv_msg:
            ms = self.fnt_md.render(self.inv_msg, True, GREEN)
            s.blit(ms, ms.get_rect(centerx=SW // 2, y=SH - 34))

        hint = self.fnt_sm.render("[E] oder [Esc] zum Schließen", True, GRAY)
        s.blit(hint, hint.get_rect(x=rp.x + 14, y=rp.bottom + 6))

    # ── Hilfe-Screen ─────────────────────────────────────────

    def _handle_help(self, events, mp):
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_h, pygame.K_ESCAPE,
                                                         pygame.K_RETURN, pygame.K_SPACE):
                self.state = self.S_PLAY
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.state = self.S_PLAY

    def _draw_help(self):
        s = self.screen
        p = self.player
        # Hintergrund abdunkeln
        self._draw_play()
        dim = pygame.Surface((SW, SH), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 200))
        s.blit(dim, (0, 0))

        W, H = 880, 540
        px, py = (SW - W) // 2, (SH - H) // 2
        pygame.draw.rect(s, (14, 10, 5), (px, py, W, H), border_radius=10)
        pygame.draw.rect(s, GOLD, (px, py, W, H), 2, border_radius=10)

        # Titelleiste
        pygame.draw.rect(s, (38, 24, 6), (px, py, W, 38), border_radius=10)
        t = self.fnt_lg.render("HILFE & STEUERUNG", True, GOLD)
        s.blit(t, t.get_rect(centerx=px + W // 2, y=py + 5))

        col_x = [px + 22, px + 310, px + 590]
        y0    = py + 52

        def head(x, y, text):
            pygame.draw.rect(s, (50, 35, 8), (x, y, 258, 22), border_radius=4)
            s.blit(self.fnt_hud.render(text, True, GOLD), (x + 6, y + 3))

        def row(x, y, text, col=LIGHT_GRAY):
            s.blit(self.fnt_sm.render(text, True, col), (x, y))

        # Spalte 1: Steuerung
        head(col_x[0], y0, "STEUERUNG")
        pairs = [
            ("WASD / ↑↓←→", "Bewegen"),
            ("[F]",           "Angreifen"),
            ("[R]",           "Rasten (ohne Feinde)"),
            ("[P]",           "Beute aufheben"),
            ("[E]",           "Inventar öffnen"),
            ("[H]",           "Diese Hilfe"),
            ("[I]",           "Monsterinfo"),
            ("[Esc]",         "Schließen"),
        ]
        y = y0 + 30
        for key, action in pairs:
            s.blit(self.fnt_sm.render(key,    True, YELLOW),     (col_x[0],       y))
            s.blit(self.fnt_sm.render(action, True, LIGHT_GRAY), (col_x[0] + 105, y))
            y += 24

        # Spalte 2: Kampfsystem
        head(col_x[1], y0, "KAMPF")
        combat = [
            "Pro [F]-Druck: ein Angriff.",
            "Du triffst immer Feind Nr. 1.",
            "Alle lebenden Feinde kontern.",
            "DEF reduziert eingehenden",
            "  Schaden pro Treffer.",
            "HP auf 0 → Tod.",
            "",
            "ITEMS",
            "Heiltrank:  HP wiederherstellen",
            "Waffe:      ATK erhöhen",
            "Rüstung:    DEF erhöhen",
            "",
            "SCHATZ-RÄUME",
            "Selten: keine Feinde,",
            "  dafür gute Ausrüstung.",
        ]
        y = y0 + 30
        for line in combat:
            row(col_x[1], y, line, LIGHT_GRAY)
            y += 24

        # Spalte 3: Levelsystem
        head(col_x[2], y0, "LEVELSYSTEM")
        xp_n = p.xp_needed()
        level_info = [
            f"Aktuelles Level:  {p.level}",
            f"XP bis Level {p.level + 1}:  {p.xp}/{xp_n}",
            "",
            "Formel:",
            f"  Level n→n+1 = n × 120 XP",
            "",
            "Pro Level-Up:",
            f"  + {p.HP_PER_LEVEL} Max-HP",
            f"  + {p.ATK_PER_LEVEL} ATK-Basis",
            "  HP vollständig aufgefüllt",
            "",
            "MONSTER XP-WERTE",
        ]
        xp_rows = [
            ("Goblin",    "30 XP"),
            ("Ork",       "85 XP"),
            ("Wächter",   "160 XP"),
            ("Ork-König", "800 XP"),
        ]
        y = y0 + 30
        for line in level_info:
            row(col_x[2], y, line, LIGHT_GRAY if not line.startswith("  +") else GREEN)
            y += 24
        for mname, mxp in xp_rows:
            s.blit(self.fnt_sm.render(mname, True, YELLOW),     (col_x[2],       y))
            s.blit(self.fnt_sm.render(mxp,   True, LIGHT_GRAY), (col_x[2] + 120, y))
            y += 22

        hint = self.fnt_sm.render("[H] / [Esc] / Klick zum Schließen", True, GRAY)
        s.blit(hint, hint.get_rect(centerx=px + W // 2, y=py + H - 26))

    # ── Monster-Info-Screen ──────────────────────────────────

    def _handle_info(self, events, mp):
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_i, pygame.K_ESCAPE,
                                                         pygame.K_RETURN, pygame.K_SPACE):
                self.state = self.S_PLAY
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.state = self.S_PLAY

    def _draw_info(self):
        s = self.screen
        self._draw_play()
        dim = pygame.Surface((SW, SH), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 210))
        s.blit(dim, (0, 0))

        W, H = 1100, 540
        px, py = (SW - W) // 2, (SH - H) // 2
        pygame.draw.rect(s, (12, 8, 4), (px, py, W, H), border_radius=10)
        pygame.draw.rect(s, GOLD, (px, py, W, H), 2, border_radius=10)
        pygame.draw.rect(s, (38, 24, 6), (px, py, W, 38), border_radius=10)
        t = self.fnt_lg.render("MONSTERINFO", True, GOLD)
        s.blit(t, t.get_rect(centerx=px + W // 2, y=py + 5))

        card_w = (W - 30) // 4
        for ci, info in enumerate(MONSTER_INFO):
            cx2 = px + 10 + ci * (card_w + 6)
            cy2 = py + 45
            ch  = H - 55
            # Karten-Hintergrund
            bg  = (25, 8, 8) if info["sprite"] == "ork_koenig" else (16, 12, 7)
            pygame.draw.rect(s, bg, (cx2, cy2, card_w, ch), border_radius=7)
            pygame.draw.rect(s, STONE, (cx2, cy2, card_w, ch), 1, border_radius=7)

            # Sprite-Vorschau (Thumbnail)
            sprite_area_h = 160
            thumb = pygame.Surface((card_w, sprite_area_h), pygame.SRCALPHA)
            fn = DRAW_FUNCS.get(info["sprite"])
            scl_map = {"goblin": 0.28, "ork": 0.32, "waechter": 0.30, "ork_koenig": 0.34}
            sc  = scl_map.get(info["sprite"], 0.30)
            if fn:
                fn(thumb, card_w // 2, sprite_area_h - 6, sc)
            s.blit(thumb, (cx2, cy2 + 2))

            # Trennlinie
            pygame.draw.line(s, STONE, (cx2 + 6, cy2 + sprite_area_h + 2),
                             (cx2 + card_w - 6, cy2 + sprite_area_h + 2))

            # Texte
            ty = cy2 + sprite_area_h + 8
            name_s = self.fnt_hud.render(info["name"], True, GOLD)
            s.blit(name_s, name_s.get_rect(centerx=cx2 + card_w // 2, y=ty))
            ty += 26

            rating_s = self.fnt_md.render(info["rating"], True, ORANGE)
            s.blit(rating_s, rating_s.get_rect(centerx=cx2 + card_w // 2, y=ty))
            ty += 28

            pygame.draw.line(s, (50, 38, 14), (cx2 + 6, ty), (cx2 + card_w - 6, ty))
            ty += 6

            stat_lines = [
                (f"HP:   {info['hp']}", RED),
                (f"ATK:  {info['atk']}", ORANGE),
                (f"XP:   +{info['xp']}", GOLD),
            ]
            for stat, col in stat_lines:
                s.blit(self.fnt_sm.render(stat, True, col), (cx2 + 10, ty))
                ty += 20

            pygame.draw.line(s, (50, 38, 14), (cx2 + 6, ty + 2), (cx2 + card_w - 6, ty + 2))
            ty += 8

            # Beschreibung (mehrzeilig)
            desc_col = LIGHT_GRAY
            desc = info["desc"]
            words = desc.split()
            line_buf, max_w = "", card_w - 16
            for word in words:
                test = (line_buf + " " + word).strip()
                if self.fnt_sm.size(test)[0] <= max_w:
                    line_buf = test
                else:
                    s.blit(self.fnt_sm.render(line_buf, True, desc_col), (cx2 + 8, ty))
                    ty += 18
                    line_buf = word
            if line_buf:
                s.blit(self.fnt_sm.render(line_buf, True, desc_col), (cx2 + 8, ty))
                ty += 20

            pygame.draw.line(s, (50, 38, 14), (cx2 + 6, ty + 2), (cx2 + card_w - 6, ty + 2))
            ty += 8

            # Drops (mehrzeilig)
            s.blit(self.fnt_sm.render("DROPS:", True, YELLOW), (cx2 + 8, ty))
            ty += 18
            drop_text = info["drops"]
            words = drop_text.split()
            line_buf = ""
            for word in words:
                test = (line_buf + " " + word).strip()
                if self.fnt_sm.size(test)[0] <= max_w:
                    line_buf = test
                else:
                    s.blit(self.fnt_sm.render(line_buf, True, (160, 200, 100)), (cx2 + 8, ty))
                    ty += 18
                    line_buf = word
            if line_buf:
                s.blit(self.fnt_sm.render(line_buf, True, (160, 200, 100)), (cx2 + 8, ty))

        hint = self.fnt_sm.render("[I] / [Esc] / Klick zum Schließen", True, GRAY)
        s.blit(hint, hint.get_rect(centerx=px + W // 2, y=py + H - 22))

    # ── Endbildschirme ────────────────────────────────────────

    def _handle_end(self, events, mp):
        for ev in events:
            if (ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE)
                    or ev.type == pygame.MOUSEBUTTONDOWN):
                self.name_str = ""
                self.state    = self.S_START
                self.player   = None
                self.gmap     = None
                self.dialog.msgs.clear()
                self.inv_sel  = None
                self.t_step   = 0

    def _draw_dead(self):
        s = self.screen
        s.fill((5, 0, 0))
        t = pygame.font.SysFont("Arial", 86, bold=True).render("DU BIST GESTORBEN", True, RED)
        s.blit(t, t.get_rect(centerx=SW // 2, y=185))
        sub = self.fnt_xl.render("Das Ödland wartet noch auf seinen Retter...", True, GRAY)
        s.blit(sub, sub.get_rect(centerx=SW // 2, y=315))
        hint = self.fnt_md.render("Klicke oder drücke [Enter] für ein neues Spiel", True, LIGHT_GRAY)
        s.blit(hint, hint.get_rect(centerx=SW // 2, y=460))

    def _draw_win(self):
        s  = self.screen
        p  = self.player
        s.fill((2, 7, 2))
        fl = int(math.sin(self.tick * 0.06) * 14)
        t  = pygame.font.SysFont("Arial", 80, bold=True).render(
            "SIEG!", True, (212 + fl, 175 + fl // 2, 36))
        s.blit(t, t.get_rect(centerx=SW // 2, y=105))

        lines = [
            "Der Ork-König wurde besiegt!",
            f"Du hast es geschafft, {p.name}!",
            "Dank deiner Hilfe konnte das Ödland befreit werden.",
            "",
            "Wir werden dir für immer dankbar sein...",
        ]
        y = 220
        for line in lines:
            ls = self.fnt_lg.render(line, True, WHITE)
            s.blit(ls, ls.get_rect(centerx=SW // 2, y=y))
            y += 52

        st = self.fnt_md.render(
            f"Level {p.level}   |   {p.xp} XP gesammelt   |   {p.ad} ATK erreicht",
            True, GOLD)
        s.blit(st, st.get_rect(centerx=SW // 2, y=y + 20))

        cr = self.fnt_sm.render(
            "ENDE  ~  Original: Kevin Küster  |  Grafische Version: Claude",
            True, GRAY)
        s.blit(cr, cr.get_rect(centerx=SW // 2, y=SH - 52))
        h2 = self.fnt_sm.render("Klicke oder [Enter] für ein neues Spiel", True, LIGHT_GRAY)
        s.blit(h2, h2.get_rect(centerx=SW // 2, y=SH - 26))


# ════════════════════════════════════════════════════════════
if __name__ == "__main__":
    game = Game()
    game.run()
