from player import Player
from move import Move
from dice import Dice
import random

class RandomAI(Player):
    def __init__(self, color):
        super().__init__(color)
        self.chosenPiece = None
        self.possibleMoves = []
        self.chosenMove = None
        self.moveMade = False
        self.moved = 0
    
    def chooseStone(self):
        self.chosenPiece = random.choice(list(self.movableStones))

    def chooseMove(self, opponent, possibleMoves, rollVals, opponentStones):
        #choose a move
        self.chosenPiece.possibleMoves = self.chosenPiece.getPossibleMoves(rollVals, opponentStones)
        self.chosenMove = random.choice(self.chosenPiece.possibleMoves)
        self.possibleMoves = []

        self.moved = self.chosenMove.location - self.chosenPiece.location

        #update chosen stone position
        self.chosenPiece.location = self.chosenMove.location
        print(self.chosenPiece, "   ", self.chosenPiece.possibleMoves, "   ", self.moved)
        self.moveMade = True
        for stone in self.stones:
            stone.possibleMoves = []
        self.getMovable()

        #take enemy pieces at move location
        for stone in opponentStones:
            if stone.location == 25 - self.chosenMove.location:
                stone.location = 0
                opponent.restrict = True
        

