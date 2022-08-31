import pygame
from .config import *

class Pawn():
    def __init__(self, row, col, color, queen_color) -> None:
        self.row = row
        self.col = col
        self.color = color
        self.queen_color = queen_color
        self.queen = False

        self.x = 0
        self.y = 0
        self.position()

    def position(self):
        self.x = FIELD_SIZE * self.col + FIELD_SIZE/2
        self.y = FIELD_SIZE * self.row + FIELD_SIZE/2
    
    def draw(self, window):
        radius = FIELD_SIZE / 2 - PAWN_PADDING
        pygame.draw.circle(window, LIGHT_RED, (self.x, self.y), radius + PAWN_BORDER)
        if not self.queen:
            pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        else:
            pygame.draw.circle(window, self.queen_color, (self.x, self.y), radius)
    
    def move(self, row, col):
        self.row = row
        self.col = col
        self.position()

    def promote_to_queen(self):
        self.queen = True
        #pygame.draw.circle(window, self.color, (self.x, self.y), FIELD_SIZE/4)

    def __repr__(self) -> str:
        return str(self.color) + ' ' + str(self.col) + ' ' + str(self.row)