import pygame, sys
from pygame.locals import *
import random

WHITE = (0,0,0)
BLACK = (255,255,255)

class Dice(object):
    def __init__(self):
        self.roll1 = None
        self.roll2 = None
        self.rollValues = []
        self.isRolled = False
        self.textFont = pygame.font.SysFont('calibri', 18, bold=True, italic=False)
        self.textBeforeRoll = self.textFont.render('Click to roll dice', True, WHITE, BLACK)
        self.textBeforeRect = self.textBeforeRoll.get_rect()
        self.rollstr = str(self.roll1) + ", " + str(self.roll2)
        self.textAfterRoll = self.textFont.render("Your roll: " + self.rollstr, True, WHITE, BLACK)
        self.textAfterRect = self.textAfterRoll.get_rect()
        self.buttonRect = (120, 260, 125, 45)
        self.buttonCenter = (182,282)

    def getRoll(self):
        return self.rollValues

    def roll(self):
        roll1 = random.randint(1,6)
        roll2 = random.randint(1,6)
        self.rollValues = [roll1, roll2]
        self.rollstr = str(roll1) + ", " + str(roll2)
        self.textAfterRoll = self.textFont.render("Your roll: " + self.rollstr, True, WHITE, BLACK)
        self.textAfterRect = self.textAfterRoll.get_rect()
        self.isRolled = True