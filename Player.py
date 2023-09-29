import random


class Player:
    def __init__(self, name, appearance=None, money=1500):
        self.name = name
        self.appearance = appearance
        self.money = money
        self.properties = []
        self.properties_value = 0
        self.countries = []
        self.position = 0
        self.jail = False
        self.jail_turns = 0
        self.jail_cards = 0
        self.dices = [0, 0]
        self.doubles = False
        self.doubles_rolls = 0

    def play(self, position, state):
        properties = state["properties"]
        players = state["players"]
        if properties[position].type in ["city" ,"service_centers"]:
            if properties[position].owner != None and properties[position].owner != self:
                print(f"{self.name} has to pay ${properties[position].rent} to {properties[position].owner.name}")
                self.pay_rent(properties[position])
            elif properties[position].owner == None:
                print(f"{self.name} can buy {properties[position].name} for ${properties[position].price}")
                if input(f"Do you want to buy it (you have ${self.money})? (y/n) ") == "y":
                    self.buy_property(properties[position], properties)
                    print(f"You bought {properties[position].name}.")
                else:
                    print(f"You didn't buy {properties[position].name}.")
            elif properties[position].owner == self:
                if self.money < 100:
                    print(f"ALARM: You have less than $100! Better to sell!")
                if input(f"Do you want to sell {properties[position].name} for {0.8 * properties[position].price}? (y/n) ") == "y":
                    self.sell_property(properties[position], properties)
                    print(f"You soled {properties[position].name} for {0.8 * properties[position].price}.")
                else:
                    print(f"You didn't sell {properties[position].name}.")
                if (properties[position].type == "city" and properties[position].country in self.countries) or (properties[position].type == "service_centers" and "Service-Centers" in self.countries):
                    if input(f"Do you want to upgrade {properties[position].name} for {1.5 * properties[position].price}? (y/n) ") == "y":
                        print(f"You upgraded {properties[position].name} for {0.5*properties[position].price}.")
                        self.upgrade_property(properties[position])
                    else:
                        print(f"You didn't upgrade {properties[position].name}.")
        if properties[position].type == "stay_place":
            if properties[position].name == "Go":
                pass
            elif properties[position].name == "Jail":
                if self.jail_cards > 0 and input(f"Do you want to use your Jail-Free card? (y/n) ") == "y":
                    self.jail_cards -= 1
                    self.jail = False
                    print(f"{self.name} used a get out of jail free card.")
                else:
                    if self.doubles:
                        self.doubles = False
                        self.doubles_rolls = 0
                    self.position = 9
                    self.jail = True
                    self.jail_turns += 1
                    print(f"{self.name} went to jail.")
            elif properties[position].name == "Auction(Trade)":
                print("Currently Auction (Trade) is not available!")
                pass
            elif properties[position].name == "FreeParking":
                print("Enjoy your free parking!")
            elif properties[position].name == "Chance":
                self.chance(players)
            elif properties[position].name == "IncomeTax":
                print(f"{self.name} paied ${0.1 * self.money} to the bank for Income Tax!")
                self.money -= 0.1 * self.money
            elif properties[position].name == "LuxuryTax":
                self.money -= 200
                print(f"{self.name} paied $200 to the bank for Luxury Tax!")
            elif properties[position].name == "Treasure":
                rand_mony = random.randint(5, 20)*10
                print(f"{self.name} got ${rand_mony} from the bank!")
                self.money += rand_mony
            else:
                raise Exception("Something went wrong in STAY_PLACE POSITIONS.")

    def roll_dices(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        roll_result = d1 + d2
        if d1 == d2:
            self.doubles_rolls += 1
            if self.doubles_rolls > 2:
                if self.jail_cards > 0 and input(f"You rolled double more than 3 times (Jail Rule). Do you want to use your Jail-Free card? (y/n) ") == "y":
                    self.jail_cards -= 1
                    self.jail = False
                    print(f"{self.name} used a get out of jail free card.")
                else:
                    self.position = 9
                    self.jail = True
                    self.jail_turns += 1
                    print(f"{self.name} went to jail becouse of 3 doubles rolls.")
                self.doubles = False
                self.doubles_rolls = 0
                return
            if self.jail:
                self.jail_turns -= 1
                if self.jail_turns == 0:
                    self.jail = False
                print(f"{self.name} is still in jail and couldn't roll again.")
                self.doubles = False
                self.doubles_rolls = 0
                return
            self.doubles = True
            print(f"{self.name} rolled double ({d1}, {d2}),next turn would be yours.")
        else:
            self.doubles = False
            self.doubles_rolls = 0
            print(f"{self.name} rolled {d1} and {d2}")
        self.dices[0] = d1
        self.dices[1] = d2
        self.move(roll_result)
        return d1, d2, roll_result
        
    def move(self, steps):
        if self.position + steps >= 40:
            self.money += 200
            print(f"{self.name} collected $200 from the bank for passing Go.")
            self.position = (self.position + steps) % 40
        else:
            self.position += steps
            
    def chance(self, players):
        commands = [
            "Go to Jail for 2 rounds",
            "Pay $50 to all players",
            "Give $20 from all players",
            "Get 1 Jail-Free card",
            "Roll the dice again",
            "Nothing..."]
        command = random.choice(commands)
        print("Command is: " + command)
        if command == "Go to Jail for 2 rounds":
            if self.jail_cards > 0 and input(f"Do you want to use your Jail-Free card? (y/n) ") == "y":
                self.jail_cards -= 1
                self.position = 9
                self.jail = True
                self.jail_turns += 1
                print(f"{self.name} used a get out of jail free card (1 round left).")
            else:
                self.position = 9
                self.jail = True
                self.jail_turns += 2
                print(f"{self.name} went to jail for 2 rounds.")
        elif command == "Pay $50 to all players":
            for player in players:
                if player != self:
                    player.money += 50
                    self.money -= len(players) * 50 - 50
        elif command == "Give $20 from all players":
            for player in players:
                if player != self:
                    player.money -= 20
                    self.money += 20
        elif command == "Get 1 Jail-Free card":
            self.jail_cards += 1
        elif command == "Roll the dice again":
            self.doubles = True
        elif command == "Nothing...":
            pass
        else:
            raise Exception("error")

    def buy_property(self, property, properties):
        if property.price < self.money:
            self.properties.append(property)
            self.properties_value += property.price
            self.money -= property.price
            property.owner = self
            if property.type == "city":
                owned_cities = [prop for prop in properties if prop.type == "city" and prop.country == property.country and (prop.owner == self or prop.owner is None)]
                if len(owned_cities) == 4:
                    self.countries.append(property.country)
                    print(f"{self.name} got all the cities in {property.country}!")
            elif property.type == "service_centers":
                owned_service_centers = [prop for prop in properties if prop.type == "service_centers" and (prop.owner == self or prop.owner is None)]
                if len(owned_service_centers) == 2:
                    self.countries.append("Service-Centers")
                    print(f"{self.name} got all the service centers!")
        else:
            print("You don't have enough money to buy it.") 


    def upgrade_property(self, property):
        if property.upgrade_time <= 3:
            if property.price < 2 * self.money:
                property.upgrade()   
            else:
                print("You don't have enough money to Build here.")
        else:
            print(f"{property.name} couldn't UPGRADE anymore.")

    def sell_property(self, property):
        self.properties.remove(property)
        self.properties_value -= property.price
        self.money += 0.8 * property.price
        property.owner = None
        if property.country in self.countries:
            self.countries.remove(property.country)

    def pay_rent(self, property):
        rent = property.rent
        if property.owner and property.owner != self:
            self.money -= rent
            property.owner.money += rent

    def is_bankrupt(self):
        return self.money < 0

    def print_player_status(self, on_property):
        print(f"*{self.name}")
        print(f"money : ${self.money}")
        print(f"properties : {self.properties}")
        print(f"position : {self.position}")
        print(f"jail : {'true' if self.jail else 'False'}")
 

    def __str__(self):
        return ("\n" + "TYPE: " + str(type(self).__name__) + 
                "\n" + "Name: " + str(self.name) + 
                "\n" + "Money: " + str(self.money) + 
                "\n" + "Properties: " + str(self.properties) +  
                "\n" + "Position: " + str(self.position) + 
                "\n" + "Jail: " + str(self.jail)
            )

    def __repr__(self):
        return (str(self.name))
