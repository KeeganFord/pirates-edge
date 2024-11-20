####################################################################################################
# Imports
####################################################################################################

from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
import game.items as item
import random
from game.display import menu


####################################################################################################
# Events and supporting classes
####################################################################################################

####################################################################################################
# candle stick puzzle
####################################################################################################

class tall_candle(item.Item):
    def __init__(self):
        super().__init__("Tall Candle Stick", 1)
        self.height = 3

class med_candle(item.Item):
    def __init__(self):
        super().__init__("Candle Stick", 1)
        self.height = 2

class short_candle(item.Item):
    def __init__(self):
        super().__init__("Small Candle Stick", 1)
        self.height = 1

####################################################################################################
#Dragon
####################################################################################################
class dragon(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(35,51), (10,30)]
        attacks["fire breath"] = ["sets alight",random.randrange(35,51), (20,40)]
        super().__init__(name, random.randrange(100,151), attacks, 110 + random.randrange(-10,11))
        self.type_name = "Deadly Dragon"
    def pickTargets(self, action, attacker, allies, enemies):
        if action.name == "bite":
            return [random.choice(enemies)]
        elif action.name == "fire breath":
            return enemies
        return [random.choice(enemies)]

class DragonAttack (event.Event):
    def __init__ (self):
        self.name = " Dragon Attack!!"
    def process (self, world):
        result = {}
        result["message"] = "the dragon has been defeated! Go forth and claim your prize!"
        monsters = []
        monsters.append(dragon("Red Dragon"))
        self.type_name = "Red Dragon"
        monsters[0].speed = 1.2*monsters[0].speed
        monsters[0].health = 2*monsters[0].health
        display.announce ("You are attacked by a deadly red Dragon!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result
####################################################################################################
# old woman attack
####################################################################################################

class Old_Woman(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["gum"] = ["gums",random.randrange(70,101), (0,1)]
        attacks["flail"] = ["flails", random.randrange(70,101), (1,2)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))
        self.type_name = "Decrepit Old Woman"

class old_woman_attack (event.Event):
    def __init__ (self):
        self.name = " Old woman attacks"

    def process (self, world):
        result = {}
        result["message"] = "The woman is defeated, I hope it was worth it"
        monsters = []
        n_appearing = random.randrange(1,2)
        n = 1
        while n <= n_appearing:
            monsters.append(Macaque("Old Woman "+str(n)))
            n += 1
        display.announce ("The crew is attacked by the old woman who come running from the shed!")
        combat.Combat(monsters).combat()
        if random.randrange(2) == 0:
            result["newevents"] = [ self ]
        else:
            result["newevents"] = [ ]
        config.the_player.ship.food += n_appearing*5

        return result

#########################
# Man-eating macaques
#########################

class Macaque(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(70,101), (10,20)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))
        self.type_name = "Man-eating Macacque"

class ManEatingMonkeys (event.Event):
    def __init__ (self):
        self.name = " monkey attack"

    def process (self, world):
        result = {}
        result["message"] = "the macaques are defeated! ...Those look pretty tasty!"
        monsters = []
        n_appearing = random.randrange(4,8)
        n = 1
        while n <= n_appearing:
            monsters.append(Macaque("Man-eating Macaque "+str(n)))
            n += 1
        display.announce ("The crew is attacked by a troop of man-eating macaques!")
        combat.Combat(monsters).combat()
        if random.randrange(2) == 0:
            result["newevents"] = [ self ]
        else:
            result["newevents"] = [ ]
        config.the_player.ship.food += n_appearing*5

        return result

###########
# Skeletons
###########

class Skeleton(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(35,51), (5,15)]
        attacks["Slash"] = ["slashes",random.randrange(35,51), (1,10)]
        attacks["Rib"] = ["Throws rib",random.randrange(35,51), (1,10)]
        #10 to 20 hp, bite attack, 55 to 65 speed (100 is "normal")
        super().__init__(name, random.randrange(10,21), attacks, 65 + random.randrange(-10,11))
        self.type_name = "Decrepite Skeletons"

class DungeonSkeletons (event.Event):
    petemade = False
    '''
    A combat encounter with a group of skeletons upon entering the dungeon.
    When the event is drawn, creates a combat encounter with 5 to 10 marooned pirates, kicks control over to the combat code to resolve the fight, then adds itself and a simple success message to the result
    '''

    def __init__ (self):
        self.name = " marooned pirate attack"

    def process (self, world):
        result = {}
        result["message"] = "the skeletal pirates are defeated!"
        monsters = []
        min = 5
        uplim = 10
        if not DungeonSkeletons.petemade:
            DungeonSkeletons.petemade = True
            min = 1
            uplim = 5
            monsters.append(Skeleton("Skelly Doug"))
            self.type_name = "Skelly Doug"
            monsters[0].health = 3*monsters[0].health
        elif random.randrange(2) == 0:
            min = 1
            uplim = 5
            monsters.append(Skeleton("Skeleton captain"))
            self.type_name = "Skeleton Captain"
            monsters[0].speed = 1.2*monsters[0].speed
            monsters[0].health = 2*monsters[0].health
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(Skeleton("Skeleton "+str(n)))
            n += 1
        display.announce ("You are attacked by a crew of skeletal pirates!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result
    

####################################################################################################
# Treasure
####################################################################################################

class RubyBroadSword(item.Item):
    def __init__(self):
        super().__init__("Ruby-Sword", 300) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (15,80)
        self.skill = "swords"
        self.verb = "cut"
        self.verb2 = "cuts"

class Dragons_hoard(item.Item):
    def __init__(self):
        super().__init__("Dragon's Hoard", 1000) #Note: price is in shillings (a silver coin, 20 per pound)
       
class Ancient_Flintlock(item.Item):
    def __init__(self):
        super().__init__("Ancient flintlock", 300) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (20,100)
        self.firearm = True
        self.charges = 1
        self.skill = "guns"
        self.verb = "shoot"
        self.verb2 = "shoots"
        self.NUMBER_OF_ATTACKS = 2

    def pickTargets(self, action, attacker, allies, enemies):
        if (len(enemies) <= self.NUMBER_OF_ATTACKS): # If less than or equal to two targets, hit everyone
            return enemies
        else:
            options = []
            for t in enemies:
                options.append("attack " + t.name)
            targets = []

            while(len(targets) < self.NUMBER_OF_ATTACKS): # While loop so that it keeps going until the player picks two different targets.
                display.announce(f"Pick target number {len(targets)}.", pause=False)
                choice = menu(options)
                if(not choice in targets):
                    targets.append(enemies[choice])
            return targets

####################################################################################################
# Island definition
####################################################################################################

class Puzzle_Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = " island"
        self.symbol = 'PI'
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = Beach_with_ship(self)
        self.locations["clearing"] = clearing(self)
        self.locations["old_house"] = oldhouse(self)
        self.locations["dungeon_entrance"] = dungeon_entrance(self)
        self.locations["dungeon_hallway"] = dungeon_hallway(self)
        self.locations["hoard_room"] = hoard_room(self)

        self.starting_location = self.locations["beach"]

    def enter (self, ship):
        display.announce ("arrived at an island", pause=False)

class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.append (seagull.Seagull())
    def enter (self):
        display.announce ("arrive at the beach. Your ship is at anchor in a small bay to the south.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["dungeon_entrance"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["old_house"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["clearing"]

class dungeon_entrance (location.SubLocation):

    def __init__ (self, m):
        super().__init__(m)
        self.name = "dungeon entrance"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['place'] = self
        self.ped_a = False
        self.ped_b = False
        self.ped_c = False
       


        # Include a couple of items and the ability to pick them up, for demo purposes
        self.verbs['take'] = self
        self.item_in_tree = med_candle() #Treasure from this island
        self.item_in_clothes = items.Flintlock() #Flintlock from the general item list

        self.event_chance = 50
        eh = 0
        if eh == 0:
            self.events.append(ManEatingMonkeys())
            eh += 1

    def enter (self):
        edibles = False
        for e in self.events:
            if isinstance(e, ManEatingMonkeys):
                edibles = True
        #The description has a base description, followed by variable components.
        description = "You walk through the woods and come upon what looks like a door carved into stone. In front of it you notice three pedistals."
        if edibles == False:
             description = description + " Nothing around here looks very edible."

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_in_tree != None:
            description = description + f" You see a {self.item_in_tree.name} on the ground."
        if self.item_in_clothes != None:
            description = description + f" You see a {self.item_in_clothes.name} in a pile of shredded clothes on the forest floor."
        display.announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        
        if (verb == "place"):
            tall = False
            med = False
            short = False
            
            for item in config.the_player.inventory:
                if type(item) == tall_candle:
                    tall = True
                if type(item) == med_candle:
                    med = True
                if type(item) == short_candle:
                    short = True

            if (tall == True and med == True and short == True ):
                display.announce("which candlestick should be put on the first pedestal\nShort\nMedium\nTall")
                ped_1 = display.get_text_input(">")
                if (ped_1 == "short" or ped_1 == "Short"):
                    self.ped_a = True
                display.announce("which candlestick should be put on the second pedestal\nShort\nMedium\nTall")
                ped_2 = display.get_text_input(">")
                if (ped_2 == "medium" or ped_2 == "Medium"):
                    self.ped_b = True
                display.announce("which candlestick should be put on the last pedestal\nShort\nMedium\nTall")
                ped_3 = display.get_text_input(">")
                if (ped_3 == "tall" or ped_3 == "Tall"):
                    self.ped_c = True
            else:
                display.announce("You can not complete this puzzle yet. search the island you may find what you are looking for.")

        
        if (verb == "south" ):
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["clearing"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["old_house"]
        elif (verb == "north"):
            if (self.ped_a == True and self.ped_b == True and self.ped_c == True):
                config.the_player.next_loc = self.main_location.locations["dungeon_hallway"]
            else:
                display.announce ("the way north into the cave is blocked.\n " + 
                                  "Maybe it has something to do with the pedestals.")
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None:
                display.announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You take the {item.name} from the ground.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You pick up the {item.name} out of the pile of clothes. ...It looks like someone was eaten here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    display.announce ("You don't see one of those around.")

class clearing (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "clearing"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes
        self.verbs['take'] = self
        self.item_in_tree = short_candle() #Treasure from this island
        self.item_in_clothes = items.BelayingPin() 

    def enter (self):
        edibles = False
        #The description has a base description, followed by variable components.
        description = "As you come into a clearing, you see what looks like the remenants of massive fire."
        if edibles == False:
             description = description + " Nothing around here looks very edible."

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_in_tree != None:
            description = description + f" Upon closer inspeection you see a charred skeleton clutching a {self.item_in_tree.name}."
        if self.item_in_clothes != None:
            description = description + f" You see a {self.item_in_clothes.name} among the charred boxes and remains."
        display.announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["dungeon_entrance"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["old_house"]
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None:
                display.announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You take the {item.name} from the skeleton.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You pick up the {item.name} out of the pile.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    display.announce ("You don't see one of those around.")

class oldhouse (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "old house"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes
        self.verbs['take'] = self
        self.item_in_tree = tall_candle() #Treasure from this island
        self.item_in_clothes = None

        self.event_chance = 100
        self.events.append(old_woman_attack())

    def enter (self):
        edibles = False
        #The description has a base description, followed by variable components.
        description = "Stumbling through the forest you come across an old house."
        if edibles == False:
             description = description + " Nothing around here looks very edible."

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_in_tree != None:
            description = description + f" Upon entering the house you find a {self.item_in_tree.name}."
        display.announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "east"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["dungeon_entrance"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["clearing"]
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None:
                display.announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You take the {item.name} from the house.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    display.announce ("You don't see one of those around.")

class dungeon_hallway (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = " hallway"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 100
        self.events.append(DungeonSkeletons())

    def enter (self):
        edibles = False
        #The description has a base description, followed by variable components.
        description = "You enter the dungeon and walk through a dark damp hallway. "

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["hoard_room"]
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            display.announce ("There is nothing here to take.")

class hoard_room (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "dungeon entrance"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes
        self.verbs['take'] = self
        self.item_in_tree = RubyBroadSword() 
        self.item_in_clothes = Dragons_hoard() 
        self.item_on_ground = Ancient_Flintlock()

        self.event_chance = 100
        self.events.append(DragonAttack())

    def enter (self):
        #The description has a base description,
        description = "upon entering the finally chamber you see massive room that must have been a safe house for pirates long past."

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_in_tree != None:
            description = description + f" You see a {self.item_in_clothes.name} covering the ground."
        if self.item_in_clothes != None:
            description = description + f" You see a {self.item_in_tree.name} shinning from beneath the gold."
        if self.item_on_ground != None:
            description = description + f" You see a {self.item_on_ground.name} discarded to the side."
        display.announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None and self.item_on_ground == None:
                display.announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You take the {item.name} from beneath the gold.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You collect the {item.name} you'll be rich if you can make it home.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_on_ground
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You collect the {item.name} use it wisely.")
                    config.the_player.add_to_inventory([item])
                    self.item_on_ground = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    display.announce ("You don't see one of those around.")