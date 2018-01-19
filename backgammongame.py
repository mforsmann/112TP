import pygame, sys
import math
import random
from enum import Enum
from player import Player
from humanplayer import HumanPlayer
from aiplayer import AIPlayer
from stone import Stone
from dice import Dice

WHITE = (0,0,0)
BLACK = (255,255,255)

class GameState(Enum):
    INITIAL_ROLL = 1
    WHITE_TO_ROLL = 2
    WHITE_TO_SELECT = 3
    BLACK_TO_ROLL = 4
    BLACK_TO_SELECT = 5
    GAME_OVER = 6


class BackgammonGame(object):

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        #draw board
        screen.blit(self.boardImage, (self.margin, self.margin))

        #update movable stones and draw stones
        for player in (self.player1, self.player2):
            player.getMovable()
            player.drawStones()

        for stone in self.player1.getStones():
            screen.blit(stone.image, (stone.rect.x, stone.rect.y))
        for stone in self.player2.getStones():
            screen.blit(stone.image, (stone.rect.x, stone.rect.y))
            
        #draw roll button
        screen.fill((255,255,255), self.dice.buttonRect)
        pygame.draw.rect(screen, (0,0,0), self.dice.buttonRect, 2)
        if self.dice.rollValues == []:
            (self.dice.textBeforeRect.centerx,self.dice.textBeforeRect.centery) = self.dice.buttonCenter
            screen.blit(self.dice.textBeforeRoll, self.dice.textBeforeRect)
        else:
            (self.dice.textAfterRect.centerx, self.dice.textAfterRect.centery) = self.dice.buttonCenter
            screen.blit(self.dice.textAfterRoll, self.dice.textAfterRect)
        
        #draw possible moves
        for move in self.possibleMoves:
            screen.blit(move.image, move.rect)
        
        #update/indicate board state message
        if self.gameState == GameState.INITIAL_ROLL:
            self.gsMessage = "Initial Roll"
        elif self.gameState == GameState.WHITE_TO_ROLL:
            self.gsMessage = "White to Roll Dice"
        elif self.gameState == GameState.WHITE_TO_SELECT:
            self.gsMessage = "White to Select a Piece"
        elif self.gameState == GameState.BLACK_TO_ROLL:
            self.gsMessage = "Black to Roll Dice"
        elif self.gameState == GameState.BLACK_TO_SELECT:
            self.gsMessage = "Black to Select a Piece"
        elif self.gameState == GameState.GAME_OVER:
            if self.player1.victory == True:
                self.gsMessage = "Game Over - Player 1 Wins"
            elif self.player2.victory == True:
                self.gsMessage = "Game Over - Player 2 Wins"
                
        self.gsText = self.textFont.render(self.gsMessage, True, WHITE, BLACK)
        self.gsRect = self.gsText.get_rect()
        (self.gsRect.centerx, self.gsRect.centery) = (self.width//2, self.margin//2)
        screen.blit(self.gsText, self.gsRect)

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, player1, player2, width=860, height=560, fps=50, title="112 Term Project: Backgammon"):
        pygame.init()
        self.player1 = player1
        self.player2 = player2
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        self.boardImage = pygame.image.load("board.png")
        self.boardRect = self.boardImage.get_rect()
        self.margin = 30
        self.xcoords = [800, 738, 676, 613, 550, 485, 373, 308, 247, 182, 121, 60, 60, 121, 182, 247, 308, 373, 485, 550, 613, 676, 738, 800]
        self.isGameOver = False
        self.textFont = pygame.font.SysFont('calibri',12, bold=True, italic=False)
        self.selected = None
        self.possibleMoves=[]
        self.dice = Dice()

        self.gameState = GameState.INITIAL_ROLL
        self.gsMessage = "Initial Roll"
        self.gsText = self.textFont.render(self.gsMessage, True, WHITE, BLACK)
        self.gsRect = self.gsText.get_rect()
        (self.gsRect.centerx, self.gsRect.centery) = (self.width//2, self.margin//2)

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.gameState = GameState.BLACK_TO_ROLL
        playing = True
        while playing:
            for event in pygame.event.get():
                if self.gameState == GameState.INITIAL_ROLL:
                    # one die for black, one for white - highest roll takes first turn
                    # roll used on first turn is the combined decision roll
                    self.gameState = GameState.WHITE_TO_ROLL

                elif self.gameState == GameState.WHITE_TO_ROLL:
                    if event.type == pygame.MOUSEBUTTONUP:
                        # white rolls dice (mouse click on roll button)
                        (x, y) = (event.pos)
                        if self.dice.buttonRect[0] <= x <= self.dice.buttonRect[0]+self.dice.buttonRect[2] and\
                           self.dice.buttonRect[1] <= y <= self.dice.buttonRect[1]+self.dice.buttonRect[3]:
                            #if self.dice.isRolled == False:
                            self.dice.roll()
                            for stone in self.player1.movableStones:
                                stone.possibleMoves = []
                            self.gameState = GameState.WHITE_TO_SELECT

                elif self.gameState == GameState.WHITE_TO_SELECT:
                    # white selects a piece to move (mouse click on a piece) - legal
                    # moves are highlighted points
                    if event.type == pygame.MOUSEBUTTONUP:
                        (x, y) = (event.pos)
                        if self.player1.movableStones != []:
                            for stone in self.player1.movableStones:
                                if stone.rect.x <= x <= stone.rect.x + stone.diameter and\
                                stone.rect.y <= y <= stone.rect.y + stone.diameter:
                                    self.selected = stone
                                    self.possibleMoves = []
                                    self.possibleMoves = stone.getPossibleMoves(self.dice.rollValues, self.player2.stones)
                                    for move in self.possibleMoves:
                                        move.position(self.xcoords)

                        #self.gameState = GameState.WHITE_TO_MOVE -- handle later
                        #if a point is selected to move the selected piece to, move the piece there and clear highlights
                        
                        #check if no movable stones have possible moves - if so, update gameState
                        immobile = 0
                        for stone in self.player1.movableStones:
                            if stone.getPossibleMoves(self.dice.rollValues, self.player2.stones) == []:
                                immobile += 1
                        if len(self.player1.movableStones) == immobile:
                            self.gameState = GameState.BLACK_TO_ROLL
                        
                        #make move
                        if self.selected != None and self.selected.possibleMoves != []:
                            for move in self.selected.possibleMoves:
                                if move.rect.x <= x <= move.rect.x + move.rect.width and\
                                move.rect.y <= y <= move.rect.y + move.rect.height:
                                    #update stone position
                                    moved = abs(move.location - self.selected.location)
                                    self.selected.location = move.location
                                    self.player1.getMovable()
                                    self.possibleMoves = []

                                    #take enemy pieces at move location
                                    for stone in self.player2.stones:
                                        if stone.location == 25 - move.location:
                                            stone.location = 0
                                            self.player2.restrict = True
                                
                                    #update unused dice
                                    if moved in self.dice.rollValues:
                                        self.dice.rollValues.remove(moved)
                                        self.player1.getMovable()
                                    
                                    #update dice roll
                                    if self.dice.rollValues != []:
                                        self.dice.rollstr = str(self.dice.rollValues[0])
                                    self.dice.textAfterRoll = self.dice.textFont.render("Your roll: " + self.dice.rollstr, True, WHITE, BLACK)
                                    self.dice.textAfterRect = self.dice.textAfterRoll.get_rect()

                                    if self.dice.rollValues == []:
                                        self.gameState = GameState.BLACK_TO_ROLL

                                    #check for win condition
                                    home = 0
                                    for stone in self.player1.stones:
                                        if stone.location >= 19:
                                            home += 1
                                    if home == len(self.player1.stones):
                                        self.player1.victory = True
                                        self.gameState = GameState.GAME_OVER
                                

                elif self.gameState == GameState.BLACK_TO_ROLL:
                    for stone in self.player1.stones:
                        stone.possibleMoves = []
                    self.dice.isRolled = False

                    # black rolls dice (mouse click on roll button)
                    if event.type == pygame.MOUSEBUTTONUP:
                        #self.possibleMoves = []
                        (x, y) = (event.pos)
                        if self.dice.buttonRect[0] <= x <= self.dice.buttonRect[0]+self.dice.buttonRect[2] and\
                           self.dice.buttonRect[1] <= y <= self.dice.buttonRect[1]+self.dice.buttonRect[3]:
                            self.dice.roll()
                            for stone in self.player2.movableStones:
                                stone.possibleMoves = []
                            self.gameState = GameState.BLACK_TO_SELECT

                elif self.gameState == GameState.BLACK_TO_SELECT:
                    # black selects a piece to move (mouse click on a piece) - legal
                    # moves are highlighted points
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.player2.getMovable()
                        (x, y) = (event.pos)
                        if self.player2.movableStones != []:
                            for stone in self.player2.movableStones:
                                if stone.rect.x <= x <= stone.rect.x + stone.diameter and\
                                stone.rect.y <= y <= stone.rect.y + stone.diameter:
                                    self.selected = stone
                                    self.possibleMoves = []
                                    self.possibleMoves = stone.getPossibleMoves(self.dice.rollValues, self.player1.stones)
                                    for move in self.possibleMoves:
                                        move.position(self.xcoords)

                        #check if no movable stones have possible moves - if so, update gameState
                        immobile = 0
                        for stone in self.player2.movableStones:
                            if stone.getPossibleMoves(self.dice.rollValues, self.player1.stones) == []:
                                immobile += 1
                        if len(self.player1.movableStones) == immobile:
                            self.gameState = GameState.WHITE_TO_ROLL

                        #make move
                        if self.selected != None and self.selected.possibleMoves != []:
                            for move in self.selected.possibleMoves:
                                if move.rect.x <= x <= move.rect.x + move.rect.width and\
                                move.rect.y <= y <= move.rect.y + move.rect.height:

                                    #update stone position
                                    moved = abs(move.location - self.selected.location)
                                    self.selected.location = move.location
                                    self.player2.getMovable()
                                    self.possibleMoves = []

                                    #take enemy pieces at move location
                                    for stone in self.player1.stones:
                                        if stone.location == 25 - move.location:
                                            stone.location = 0
                                            self.player1.restrict = True

                                    #update unused dice
                                    if moved in self.dice.rollValues:
                                        self.dice.rollValues.remove(moved)
                                        self.player2.getMovable()

                                    #update dice roll
                                    if self.dice.rollValues != []:
                                        self.dice.rollstr = str(self.dice.rollValues[0])
                                    self.dice.textAfterRoll = self.dice.textFont.render("Your roll: " + self.dice.rollstr, True, WHITE, BLACK)
                                    self.dice.textAfterRect = self.dice.textAfterRoll.get_rect()
                                    if self.dice.rollValues == []:
                                        self.gameState = GameState.WHITE_TO_ROLL
                                        
                                    #check for win condition
                                    home = 0
                                    for stone in self.player2.stones:
                                        if stone.location >= 19:
                                            home += 1
                                    if home == len(self.player2.stones):
                                        self.player2.victory = True
                                        self.gameState = GameState.GAME_OVER


                elif self.gameState == GameState.GAME_OVER:
                    # winner is displayed, user clicks a restart button to play again
                    pass

            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()
            if event.type == pygame.QUIT:
                pygame.quit()



def main():
    player1 = Player(WHITE)
    player2 = Player(BLACK)
    game = BackgammonGame(player1, player2)
    game.run()

if __name__ == '__main__':
    main()
