from player import Player
from move import Move
import random

class RandomAI(Player):
    def __init__(self, color):
        super.__init__(color)

    def makeMove(self, possibleMoves):
        move = random.choice(possibleMoves)
        return move

