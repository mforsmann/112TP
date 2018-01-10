import pygame
WHITE = (255,255,255)
BLACK = (0,0,0)

class Move(object):
    def __init__(self, location, color):
        self.location = location
        self.color = color
        if self.location >= 13:
            self.image = pygame.image.load("UpMove.png")
        else:
            self.image = pygame.image.load("DownMove.png")
        self.imgRect = self.image.get_rect()

    def position(self, xcoords):
        if self.color == WHITE:
            self.imgRect.centerx = xcoords[self.location-1]
            
            if self.location < 13:
                self.imgRect.y = 30
            else:
                self.imgRect.y = 300
        elif self.color == BLACK:
            self.imgRect.centerx = xcoords[25 - self.location - 1]

            if self.location >= 13:
                self.imgRect.y = 300
            else:
                self.imgRect.y = 30