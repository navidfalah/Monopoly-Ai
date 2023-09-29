from Player import Player
from utils import all_possible_actions, all_rolls
import numpy as np
from copy import deepcopy
import random


class AI_Agent(Player):
    def __init__(self, name, depth=3, appearance=None, money=1500):
        super().__init__(name, appearance, money)
        self.depth = depth

    def play(self, position, state):
        properties = state["properties"]
        players = state["players"]

        if properties[position].type == "city" or properties[position].type == "service_centers":
            if properties[position].owner != None and properties[position].owner != self:
                print(f"{self.name} has to pay ${properties[position].rent} to {properties[position].owner.name}")
                self.pay_rent(properties[position])
            elif properties[position].owner == None:
                print(f"{self.name} can buy {properties[position].name} for ${properties[position].price}")
                if self.make_decision(state) == "buy":
                    self.buy_property(properties[position], properties)
                    print(f"You bought {properties[position].name}.")
                else:
                    print(f"You didn't buy {properties[position].name}.")
            elif properties[position].owner == self:
                if self.make_decision(state) == "sell":
                    self.sell_properties[position](properties[position])
                    print(f"You soled {properties[position].name} for {0.8 * properties[position].price}.")
                else:
                    print(f"You didn't sell {properties[position].name}.")
                if (properties[position].type == "city" and properties[position].country in self.countries) or (properties[position].type == "service_centers" and "Service-Centers" in self.countries):
                    if self.make_decision(state) == "upgrade":
                        print(f"You upgraded {properties[position].name} for {0.5*properties[position].price}.")
                        self.upgrade_property(properties[position])
                    else:
                        print(f"You didn't upgrade {properties[position].name}.")
        if properties[position].type == "stay_place":
            if properties[position].name == "Go":
                pass
            elif properties[position].name == "Jail":
                if self.jail_cards > 0 and self.make_decision(state) == "use_jail_card":
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
                print("CurrentlyAuction(Trade) is not available!")
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
                raise Exception("error")

    def current_possible_actions(self, state):
        possible_actions = []
        properties = state["properties"]
        if properties[self.position].type == "city" or properties[self.position].type == "service_centers":
            if properties[self.position].owner == None:
                possible_actions.append(all_possible_actions[5])
                possible_actions.append(all_possible_actions[0])
            elif properties[self.position].owner == self:
                possible_actions.append(all_possible_actions[5])
                possible_actions.append(all_possible_actions[1])
                if (properties[self.position].type == "city" and properties[self.position].country in self.countries) or (properties[self.position].type == "service_centers" and "Service-Centers" in self.countries):
                    possible_actions.append(all_possible_actions[2])
        if properties[self.position].type == "stay_place":
            if properties[self.position].name == "Jail":
                possible_actions.append(all_possible_actions[5])
                possible_actions.append(all_possible_actions[3])
            elif properties[self.position].name == "Auction (Trade)":
                possible_actions.append(all_possible_actions[5])
                possible_actions.append(all_possible_actions[4])
        return possible_actions

    def make_decision(self, state):
        actions = self.current_possible_actions(state)
        action_values = []
        for action in actions:
            new_state = self.get_next_state(state, action)
            value = self.expectiminimax(new_state, self.depth)
            action_values.append((action, value))
        sorted_actions = sorted(action_values, key=lambda x: x[1], reverse=True)
        best_action = sorted_actions[0][0]
        return best_action

    def expectiminimax(self, state, depth):
        if state["rounds_left"] == 0 or depth == 0:
            return self.evaluate_state(state)

        if state["current_player"] == self:
            max_value = -np.inf
            actions = self.current_possible_actions(state)
            for action in actions:
                new_state = self.get_next_state(state, action)
                value = self.expectiminimax(new_state, depth-1)
                max_value = max(max_value, value)
            return max_value
        elif state["current_player"] != self:
            min_value = np.inf
            actions = self.current_possible_actions(state)
            for action in actions:
                new_state = self.get_next_state(state, action)
                value = self.expectiminimax(new_state, depth-1)
                min_value = min(min_value, value)
            return min_value
        else:
            total_value = 0
            probabilities = all_rolls()
            for outcome, probability in probabilities.items():
                new_state = self.get_next_state_2(state, outcome)
                value = self.expectiminimax(new_state, depth-1)
                total_value += value * probability
            return total_value

    def evaluate_state(self, state):
        properity_all_value = 0
        for properitie in self.properties:
            properity_all_value += properitie.price
            properity_all_value += properitie.rent * 1.3
        value = self.money + properity_all_value
        return value

    def get_next_state(self, state, action):
        new_state = deepcopy(state)
        current_player = new_state["current_player"]
        properties = new_state["properties"]
        if action == "buy":
            current_player.buy_property(properties[current_player.position], properties)
        elif action == "sell":
            current_player.sell_property(properties[current_player.position])
        elif action == "upgrade":
            current_player.upgrade_property(properties[current_player.position])
        elif action == "use_jail_card":
            current_player.jail_cards -= 1
            current_player.jail = False
        elif action == "auction" or action == "nothing_just_stay":
            pass
        else:
            raise Exception("error")
        return new_state

    def get_next_state_2(self, state, outcome):
        new_state = deepcopy(state)
        new_state["current_player"].move(int(outcome))
        return new_state
    