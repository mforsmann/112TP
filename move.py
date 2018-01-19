import pygame

BLACK = (0,0,0)
WHITE = (255,255,255)


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

    def __eq__(self, other):
        if isinstance(other, Move) and self.location == other.location and self.color == other.color:
            return True
        return False
        
    
    def __repr__(self):
        final = "Move to " + str(self.location) 
        return final

    def position(self, xcoords):
        if 0 < self.location  and self.location <= len(xcoords):
            if self.color == BLACK:
                self.rect.centerx = xcoords[self.location-1]
                
                if self.location < 13:
                    self.rect.y = 30
                else:
                    self.rect.y = 300
            elif self.color == WHITE:
                self.rect.centerx = xcoords[self.location-1]

                if self.location >= 13:
                    self.rect.y = 30
                else:
                    self.rect.y = 300
