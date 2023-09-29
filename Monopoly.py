import random
import numpy as np
from Property import *

class Monopoly():
    def __init__(self, players, players_num=2, max_rounds=50, max_money=2500, AI_Agent_Mode=False):
        self.players = players
        self.properties = []
        self.players_num = players_num
        self.max_rounds = max_rounds
        self.max_money = max_money
        self.AI_Agent_Mode = AI_Agent_Mode
        self.round = 0
        self.current_player = None
        self.losers = []
        self.winner = None

    def check_winner(self):
        richest = None
        richestmoney = -np.inf
        for p in self.players:
            if p.money == self.max_money:
                self.winner = p
            elif p.money > richestmoney:
                richest = p
                richestmoney = p.money
        self.winner = richest
        self.losers = self.players[:]
        self.losers.remove(self.winner)

    def game_state(self):
        state = {"properties": self.properties,
                 "players": self.players,
                 "rounds_left": self.max_rounds - self.round,
                 "current_player": self.current_player,
                 "winner": self.winner,
                 "max_money": self.max_money}
        return state

    def display_game_state(self, mode="players"):
        for p in self.players:
            p.print_player_status(self.properties)


    def start_game(self):
        random.shuffle(self.players)
        self.display_game_state()
        wtd = "c"
        while self.round < self.max_rounds and wtd != "end":
            if wtd == "g":
                self.display_game_state()
            elif wtd == "p":
                self.display_game_state("properties")
            for turn_counter in range(self.players_num):
                current_player = self.players[turn_counter]
                self.current_player = current_player
                if current_player.is_bankrupt():
                    print(f"{current_player.name} is bankrupt!")
                    for _ in current_player.properties:
                        self.properties[_].owner = None
                    self.players_num -= 1
                    self.players.remove(current_player)
                    self.losers.append(current_player)
                    if self.players_num == 1:
                        self.winner = self.players[0]
                        print(f"Winner: {self.winner.name}")
                        print(f"Loser: {self.losers}")
                        return
                if current_player.jail and current_player.jail_turns > 0:
                    current_player.doubles = False
                    current_player.doubles_rolls = 0
                    current_player.jail_turns -= 1
                    print(f"{current_player.name} is in JAIL and can't roll dices.")
                    if current_player.jail_turns == 0:
                        current_player.jail = False
                    continue
                print(f"\n{current_player.name}'s turn")
                for i in range(4):
                    if type(current_player).__name__ == "Player":
                        input("press inter to roll")
                    current_player.roll_dices()
                    print(f"{current_player.name} is on {self.properties[current_player.position].name}")
                    if type(current_player).__name__ == "AI_Agent":
                        current_player.play(current_player.position, self.game_state())
                    if type(current_player).__name__ == "Player":
                        current_player.play(current_player.position, self.game_state())
                    print("**** Status ****")
                    self.display_game_state("players")
                    if not current_player.doubles:
                        break
            self.check_winner()
            print(f"\n<<<<<<<<--------- ROUND {self.round+1} / {self.max_rounds} END ----------->>>>>>>\n")
            self.round += 1
            wtd = input("Inter \"c\" to continue \n" + "Inter \"end\" to END this game: ")
            
        self.check_winner()
        print("\n", "Game ended.")
        print(f"Winner: {self.winner.name}")
        print(f"Loser: {self.losers}", "\n")
        return
