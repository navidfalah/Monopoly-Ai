from Property import Property
from Monopoly import Monopoly

all_possible_actions = ["buy", "sell", "upgrade", "use_jail_card", "auction", "nothing_just_stay"]

def all_rolls():
    all_results = []
    for i in range(2,13):
        favorable = 0
        for j in range(1,7):
            if i-j >= 1 and i-j <= 6:
                favorable += 1
        probability = favorable / 36
        all_results.append((i,probability))
    return all_results


def create_board(Monopoly):
    property_place, property_price, property_rent, property_country, property_type, properties = [], [], [], [], [], []
    with open('board.txt', 'r') as f:
        for line in f:
            txt = f.readline().replace("\n", "")
            list_me = txt.split(" ")
            property_place.append(list_me[1])
            property_type.append(list_me[2])
            property_country.append(list_me[3])
            property_price.append(float(list_me[4]))
            property_rent.append(float(list_me[5]))
    for i in range(40):
        properties.append(Property(property_place[i], 
                                    property_type[i], 
                                    property_country[i], 
                                    property_price[i], 
                                    property_rent[i], i))
    Monopoly.properties = properties
