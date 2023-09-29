from Player import Player
from Agent import AI_Agent
from Monopoly import Monopoly
from utils import create_board


players = [Player("User"), AI_Agent("Ai")]
Monopoly_Game = Monopoly(players, 2, AI_Agent_Mode = False)
create_board(Monopoly_Game)
Monopoly_Game.start_game()
