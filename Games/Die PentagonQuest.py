import random
import time

class Item:
    def __init__(self, weigth, worth):
        self.weight = weigth
        self.worth = worth
        self.equipped = False
        
    def set_equipped_true(self):
    	self.equipped = True
    	
    def set_equipped_false(self):
    	self.equipped = False

class Sword(Item):
	def __init__(self, weight, worth, ad, name):
		Item.__init__(self, weight, worth)
		self.ad = ad
		self.name = name

class HPPlus(Item):
    def __init__(self, hpPlus, name):
        self.hpPlus = hpPlus
        self.name = name

class Character:
    def __init__(self, hp, ad, name):
        self.hp = hp
        self.ad = ad
        self.name = name

    def get_hit(self, ad):
        self.hp = self.hp - ad
        if self.hp <= 0:
            self.die()

    def is_dead(self):
        return self.hp <= 0

    def die(self):
        print(self.name + " ist gestorben")

class MobWithDrop():
	def __init__(self, drop):
		self.drop = drop
		
	def get_drop(self):
		return self.drop

class Goblin(Character, MobWithDrop):
    def __init__(self, drop):
        MobWithDrop.__init__(self, drop)
        Character.__init__(self, 100, 10, "Goblin")

class Ork(Character, MobWithDrop):
    def __init__(self, drop):
        MobWithDrop.__init__(self, drop)
        Character.__init__(self, 300, 30, "Ork")

class OrkKoenig(Character):
    def __init__(self):
        Character.__init__(self, 4000, 60, "OrkKoenig")        
                        
class Waechter(Character, MobWithDrop):
	def __init__(self, drop):
		MobWithDrop.__init__(self, drop)
		Character.__init__(self, 800, 15, "Waechter")
	
class Player(Character):
    def __init__(self, name, hp, ad, maxInv):
        Character.__init__(self, hp, ad, name)
        self.adHand = ad
        self.ad = ad
        self.max_hp = hp
        self.inv = []
        self.maxInv = maxInv
        self.equippedItem = 0
     
    def get_inv(self):
           return self.inv
           
    def show_inv(self):
    	print(str(len(self.inv)) + "/" + str(self.maxInv))
    	    
    def die(self):
    	exit("Du bist gestorben.")

    def rest(self):
        self.hp = self.max_hp
        
    def eItem(self):
    	for i in range (len(self.inv)):
    		if self.inv[i].equipped == True:
    			return i


class Field:
    def __init__(self, enemies, loot):
        self.enemies = enemies
        self.loot = loot

    def print_state(self):
        print("Du guckst dich um und siehst ")
        print("\n" + "Feinde:")
        for i in self.enemies:
            print(i.name + " >	HP: " + str(i.hp) + " , " + "Atk: " + str(i.ad))
        print("\n" + "Loot:")
        x = 0
        for i in self.loot:
        	print(str(x) + ". " + i.name)
        	x = x +1

    @staticmethod
    def gen_random():
        rand = random.randint(0,4)
        if rand == 0:
            return Field([Waechter([Sword(1,100,400, "Sword: 400ad")]), Waechter([Sword(1,100,400, "Sword: 400ad")])],[])
        if rand == 1:
            return Field([Ork([Sword(1,100,250, "Sword: 250ad"), HPPlus(50, "+50 Hp")])],[])
        if rand == 2:
            return Field([Goblin([]), Waechter([Sword(1,100,400, "Sword: 400ad")]), Ork([Sword(1,100,250, "Sword: 250ad"), HPPlus(50, "+50 Hp")])],[])
        if rand == 3:
        	return Field([Goblin([Sword(1,100,100, "Sword: 100ad")]), Goblin([]), Goblin([])],[])
        if rand == 4:
        	return Field([Goblin([]), Ork([Sword(1,100,250, "Sword: 250ad"), HPPlus(50, "+50 Hp")])],[])

class Map:
    def __init__(self, width, height):
        self.state = []
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        for i in range(width):
            fields = []
            for j in range(height):
                #print("width: " + str(width) + " height: " + str(width))
                #print("x: " + str(i) + " y: "+ str(j))
                if i == 0 and j == 0:
                	fields.append(Field([Goblin([Sword(1,100,100, "Sword: 100ad")]), Goblin([]), Goblin([])],[]))
                elif i == width-1 and j == height-1:
                	fields.append(Field([OrkKoenig()],[]))
                else:
                	fields.append(Field.gen_random())
            self.state.append(fields)
            	
    def print_state(self):
        print("x: " + str(self.x) , "y: " + str(self.y))
        self.state[self.x][self.y].print_state()

    def get_enemies(self):
        return self.state[self.x][self.y].enemies
        
    def get_loot(self):
    	return self.state[self.x][self.y].loot

    def forward(self):
        if self.x == len(self.state) - 1:
            print("Du siehst riesige Berge, welche du nicht überqueren kannst")
        else:
            self.x = self.x + 1

    def backwards(self):
        if self.x == 0:
            print("Du siehst Klippen, kannst aber nicht sicher hinunterspringen")
        else:
            self.x = self.x - 1

    def right(self):
        if self.y == len(self.state[self.x]) - 1:
            print("Du siehst riesige Berge, welche du nicht überqueren kannst")
        else:
            self.y = self.y + 1

    def left(self):
        if self.y == 0:
            print("Du siehst Klippen, kannst aber nicht sicher hinunterspringen")
        else:
            self.y = self.y - 1

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
    print("Du hast Selbstmord begannen und diese Welt verlassen.")
    exit(0)

def print_help(p, m):
    print(Commands.keys())

def pickup(p, m, item):
    loot = m.get_loot()
    if len(p.inv) < p.maxInv:
    	p.inv.append(loot[item])
    	loot.remove(loot[item])
    	m.print_state()
    	print('\n')
    else:
    	print("Dein inventar ist voll")

def fight(p, m):
    enemies = m.get_enemies()
    if len(enemies) != 0:
        while len(enemies) > 0:
        	enemies[0].get_hit(p.ad)
        	if enemies[0].is_dead():
        		try:
        			drop = enemies[0].get_drop()
        			loot = m.get_loot()
        			for i in drop:
        				loot.append(i)
        		except AttributeError:
        			pass
        		enemies.remove(enemies[0])
        	for i in enemies:
        		p.get_hit(i.ad)
        	print("Du bist verwundet und hast " + str(p.hp) + " hp übrig")
    else:
    	print("Alle Feinde sind besiegt worden")
    print('\n')
    m.print_state()

def ende(p, m):
	if len(map.state[m.width-1][m.height-1].enemies) == 0:
		return False
	else:
		return True

def rest(p, m):
    p.rest()
    
def inventar(p,m):
	itemsIninv = p.get_inv()
	x = 0
	for i in itemsIninv:
		print(str(x) + ". " + i.name)
		x = x +1
	print("\n")

def equip(p,m,item):
	try:
		p.inv[p.eItem()].set_equipped_false()
		try:
			p.ad = p.inv[item].ad
			p.inv[item].set_equipped_true()
		except AttributeError:
		  print ("Du kannst dieses Item nicht ausrüsten")
	except TypeError:
		try:
			p.ad = p.inv[item].ad
			p.inv[item].set_equipped_true()
		except AttributeError:
		  print ("Du kannst dieses Item nicht ausrüsten")

def stats(p, m):
	item = 0	
	print("Name: " + p.name + '\n' + "Gesundheit: " + str(p.hp) +"/" + str(p.max_hp) +"\n" + "Angriff: " + str(p.ad) + "\n" + "Inventar: ")
	p.show_inv()

def map(p, m):
	m.print_state()

def drop(p, m, item):
	item = p.inv[item]
	loot = m.get_loot()
	if item.equipped == True:
		p.ad = p.adHand
	loot.append(item)
	p.inv.remove(item)
	
def use(p, m, item):
	item = p.inv[item]
	try:
		p.max_hp = p.max_hp + item.hpPlus
		p.inv.remove(item)
	except AttributeError:
		print("Du kannst dieses Item nicht benutzen")
		
Commands = {
    'help': print_help,
    'quit': quit_game,
    'pickup': pickup,
    'forward': forward,
    'right': right,
    'left': left,
    'backwards': backwards,
    'fight': fight,
    'rest': rest,
    'inventar': inventar,
    'equip': equip,
    'stats': stats,
    'map': map,
    'drop': drop,
    'use': use
}

if __name__ == '__main__':
    print("Wilkommen im Ödland Fremder!")
    time.sleep(3)
    print('\n' + "Das Ödland wird schon seit langer Zeit von dem Ork-König unterdrückt...")
    time.sleep(2)
    print("Hilf uns ihn zu besiegen!")
    time.sleep(3)
    print("Du siehst aus, als könntest du kämpfen. Wie ist dein Name Fremder ?")
    time.sleep(3)
    name = input("Gib deinen Namen ein: ")
    time.sleep(2)
    print('\n' + "Sehr gut " + name + ", beginnen wir mit den Grundlagen:")
    time.sleep(2)
    print("Mit 'map' kannst du dir den aktuellen Status deiner Umgebung anzeigen lassen. Dir werden Beute und Gegner auf dem aktuellen Feld angezeigt, sowie die Koordinaten des Feldes")
    p = Player(name, 200, 50, 5)
    map = Map(5,5)
    while True:
    	if input(">") == "map":
    		map.print_state()
    		break
    	else:
    		print("Mit 'map' kannst du dir den aktuellen Status deiner Umgebung anzeigen lassen. Dir werden Beute und Gegner auf dem aktuellen Feld angezeigt, sowie die Koordinaten des Feldes")
    
    print('\n' + "Oh nein, Goblins haben das Gebiet besetzt. Du kannst sie mit 'fight' bekämpfen")				
    while True:
    	if input(">") == "fight":
    		fight(p, map)
    		break
    	else:
    		print("Oh nein, Goblins haben das Gebiet besetzt. Du kannst sie mit 'fight' bekämpfen")		
    
    print('\n' + '\n' + "Während des Kampfes kannst du sehen, welchen Schaden du einstecken musstest. Fallen deine Lebenspunkte auf 0, stirbst du!" + '\n' + '\n' + "Die Goblins haben ein Schwert fallen lassen. Du kannst Items mit 'pickup' aufheben. Im Anschluss musst du auswählen, welches Item du von dem jeweiligen Bereich nehmen möchtest. Die Zahl vor dem Item bestimmt, welches Item du aufheben kannst. In diesem Fall: 'pickup 0'")
    while True:
    	if input(">") == "pickup 0":
    		pickup(p, map, 0)
    		break
    	else:
    		print("Die Goblins haben ein Schwert fallen lassen. Du kannst Items mit 'pickup' aufheben. Im Anschluss musst du auswählen, welches Item du von dem jeweiligen Bereich nehmen möchtest. Die Zahl vor dem Item bestimmt, welches Item du aufheben kannst. In diesem Fall: 'pickup 0'")

    print("Das Item wurde deinem Inventar hinzugefügt. Du kannst dir ein Inventar mit 'inventar' ausgeben lassen")
    while True:
    	if input(">") == "inventar":
    		inventar(p, map)
    		break
    	else:
    		print("Das Item wurde deinem Inventar hinzugefügt. Du kannst dir ein Inventar mit 'inventar' ausgeben lassen")
    
    print("Mit 'stats' kannst du dir deinen aktuellen Status ausgeben lassen. Du kannst deinen Namen, deine aktuellen Lebenspunkte, den Schaden, den du verursachst, sowie deinen Platz in deinem inventar sehen")
    while True:
    	if input(">") == "stats":
    		stats(p, map)
    		break
    	else:
    		print("Mit 'stats' kannst du dir deinen aktuellen Status ausgeben lassen. Du kannst deinen Namen, deine aktuellen Lebenspunkte, den Schaden, den du verursachst, sowie deinen Platz in deinem inventar sehen")
    
    print("Du kannst aufgesammelte Items, die sich in deinem Ineventar befinden ausrüsten oder benutzen. Das Schwert, welches du von den Goblins bekommen, kannst du ausrüsten. Dadurch verursachst du erhöhten Schaden. Ausrüsten kannst du ein Item mit 'equip', benutzen kannst du ein Item mit 'use'. Auch hier musst du mit einem Index angeben, welches Item du ausrüsten bzw. benutzen möchtest. Rüste das Schwert aus deinem Inventar mit 'equip 0' aus")
    while True:
    	if input(">") == "equip 0":
    		equip(p, map, 0)
    		break
    	else:
    		print("Du kannst aufgesammelte Items, die sich in deinem Ineventar befinden ausrüsten oder benutzen. Das Schwert, welches du von den Goblins bekommen, kannst du ausrüsten. Dadurch verursachst du erhöhten Schaden. Ausrüsten kannst du ein Item mit 'equip', benutzen kannst du ein Item mit 'use'. Auch hier musst du mit einem Index angeben, welches Item du ausrüsten bzw. benutzen möchtest. Rüste das Schwert aus deinem Inventar mit 'equip 0' aus")
    
    print("Über eine erneute Ausgabe deines Status mit 'stats' siehst du, dass du nun Schaden in Höhe des Angriffswertes des Schwertes verursachst")
    while True:
    	if input(">") == "stats":
    		stats(p, map)
    		break
    	else:
    		print("Über eine erneute Ausgabe deines Status mit 'stats' siehst du, dass du nun Schaden in Höhe des Angriffswertes des Schwertes verursachst")
    		
    print("Deine Lebenspunkte sind zur Zeit auf 200 begrenzt, lassen sich aber z.B. durch HPPlus items erhöhen. Nach jedem Kampf kannst du deine Lebenspunkte mit 'rest' wieder auffüllen")
    while True:
    	if input(">") == "rest":
    		rest(p, map)
    		break
    	else:
    		print("Deine Lebenspunkte sind zur Zeit auf 200 begrenzt, lassen sich aber z.B. durch HPPlus items erhöhen. Nach jedem Kampf kannst du deine Lebenspunkte mit 'rest' wieder auffüllen")
    
    print("Sollte dein Inventar voll sein, kannst du Items die du nicht länger benötigst mit 'drop' ablegen. Diese findest du im Anschluss in dem Bereich, in dem du dich aktuell befindest." + '\n' + "Mit 'forward', 'backwards', 'left' und 'right' kannst du dich auf der Karte bewegen")
    print('\n' + "help zeigt dir alle verfügbaren Handelsoptionen\n")
    map.print_state()
    
    while ende(p, map):
        command = input(">").lower().split(" ")
        parameter = 0
        if command[0] in Commands:
            if Commands[command[0]] == Commands['pickup']:
            	try:
            		parameter = int(command[1])
            		Commands[command[0]](p, map, parameter)
            	except ValueError:
            		print("Du begibst dich auf einen Pfad, dem keiner folgen kann...")
            	except IndexError:
            		print("Wähle ein Item")
            		
            elif Commands[command[0]] == Commands['drop']:
            	try:
            		parameter = int(command[1])
            		Commands[command[0]](p, map, parameter)
            	except ValueError:
            		print("Du begibst dich auf einen Pfad, dem keiner folgen kann...")
            	except IndexError:
            		print("Wähle ein Item")
            				
            elif Commands[command[0]] == Commands['equip']:
            	try:
            		parameter = int(command[1])
            		Commands[command[0]](p, map, parameter)
            	except ValueError:
            		print("Du begibst dich auf einen Pfad, dem keiner folgen kann...")
            	except IndexError:
            		print("Wähle ein Item")
            			
            elif Commands[command[0]] == Commands['use']:
            	try:
            		parameter = int(command[1])
            		Commands[command[0]](p, map, parameter)
            	except ValueError:
            		print("Du begibst dich auf einen Pfad, dem keiner folgen kann...")
            	except IndexError:
            		print("Wähle ein Item")
            			
            else:
            	Commands[command[0]](p, map)
        else:
            print("Du begibst dich auf einen Pfad, dem keiner folgen kann...")
           
    print('\n' + '\n' + "Der Ork-König wurde besiegt..." + '\n' + "Du hast es geschafft " + name + "!" + '\n' + "Danke deiner Hilfe konnte das Ödland befreit werden." + '\n' + '\n' + "Wir werden dir für immer dankbar sein..." + '\n' + '\n' + '\n' + "ENDE ~progammed by Kevin Küster")
    time.sleep(15)