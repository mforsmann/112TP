import pygame
WHITE = (255,255,255)
BLACK = (0,0,0)

class Move(object):
    def __init__(self, location, color):
        self.location = location
        self.color = color
        if self.location >= 13:
            if self.color == BLACK:
                self.image = pygame.image.load("UpMove.png")
            elif self.color == WHITE:
                self.image = pygame.image.load("DownMove.png")
        else:
            if self.color == BLACK:
                self.image = pygame.image.load("DownMove.png")
            elif self.color == WHITE:
                self.image = pygame.image.load("UpMove.png")
        self.rect = self.image.get_rect()
    
    def __repr__(self):
        final = "Move to " + str(self.location)
        return final

    def position(self, xcoords):
        if self.color == BLACK:
            self.rect.centerx = xcoords[self.location-1]
            
            if self.location < 13:
                self.rect.y = 30
            else:
                self.rect.y = 300
        elif self.color == WHITE:
            self.rect.centerx = xcoords[self.location - 1]

            if self.location >= 13:
                self.rect.y = 30
            else:
                self.rect.y = 300