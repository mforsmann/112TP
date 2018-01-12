import pygame
from stone import Stone
WHITE = (0, 0, 0)
BLACK = (255, 255, 255)

class Player(object):
    def __init__(self, color):
        self.xcoords = [800, 738, 676, 613, 550, 485, 373, 308, 247, 182, 121, 60, 60, 121, 182, 247, 308, 373, 485, 550, 613, 676, 738, 800]
        self.stones = []
        self.movableStones = set()
        self.color = color
        #configuring initial positions of stones per game logic
        for i in range(2):
            newStone = Stone(self.color, 1)
            self.stones.append(newStone)

        for i in range(3):
            newStone = Stone(self.color, 17)
            self.stones.append(newStone)

        for i in range(5):
            newStone = Stone(self.color, 12)
            newStone2 = Stone(self.color, 19)
            self.stones.append(newStone)
            self.stones.append(newStone2)

    def getStones(self):
        return self.stones
    
    def drawStones(self):
        for stone in self.stones:
            stone.position(self.xcoords)

    def getMovable(self):
        for i in range(1,25):
            stonesAtPoint = 0
            highestStone = None
            for stone in self.stones:
                if stone.location == i:
                    highestStone = stone
                    if stone.color == WHITE:
                        if stone.location < 13:
                            stone.rect.y = (stonesAtPoint)*stone.diameter + 30
                        else:
                            stone.rect.y = 530 - ((stonesAtPoint+1)*stone.diameter)
                    elif stone.color == BLACK:
                        if stone.location < 13:
                            stone.rect.y = 530 - ((stonesAtPoint+1)*stone.diameter)
                        else:
                            stone.rect.y = (stonesAtPoint)*stone.diameter + 30
                    stonesAtPoint += 1
            if highestStone != None:
                self.movableStones.add(highestStone)
            stonesAtPoint = 0
