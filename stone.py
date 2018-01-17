import pygame
from move import Move
WHITE = (0, 0, 0)
BLACK = (255, 255, 255)

class Stone(object):
    def __init__(self, color, location):
        self.color = color
        self.diameter = 40
        #int from 0 to 25, indicating point/home/on bar
        self.location = location
        self.possibleMoves = []
        
        if self.color == (0, 0, 0):
            self.image = pygame.image.load("lightpiece.png")
        elif self.color == (255, 255, 255):
            self.image = pygame.image.load("darkpiece.png")
        self.rect = self.image.get_rect()
    
    def __repr__(self):
        final = str(self.color) + "stone at " + str(self.location)
        return final

    def position(self, xcoords):
        try:
            if self.color == WHITE:
                self.rect.x = xcoords[self.location - 1] - 0.5*self.diameter
                
            elif self.color == BLACK:
                self.rect.x = xcoords[25 - self.location - 1] - 0.5*self.diameter
        except:
            self.rect.x = 430 - 0.5 * self.diameter
    
    def getPossibleMoves(self, rollValues, opponentStones):
        # taking each die roll separately
        total = 0
        
        for val in rollValues:
            total += val
            newLocation = self.location + val

            opponentStonesPresent = 0
            for stone in opponentStones:
                if 25 - stone.location == newLocation:
                    opponentStonesPresent += 1
            
            if opponentStonesPresent <= 1:
                newMove = Move(newLocation, self.color)
                self.possibleMoves.append(newMove)

       
        return self.possibleMoves