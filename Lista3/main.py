import pygame
import time
from backend import config
from backend.config import *
from backend.rules import Rules

def get_mouse_position(pos):
    x, y = pos
    row = int(y / FIELD_SIZE)
    col = int(x / FIELD_SIZE)

    return row, col

def play():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')

    pygame.init()
    pygame.font.init()

    run = True
    clock = pygame.time.Clock()

    game = Rules(window)
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_position(pos)
                game.select_pos(row, col)

        if game.win_text != '':
            print(game.win_text)
            run = False

        game.update()

if __name__ == "__main__":
    for i in range(1):
        start_time = time.time()
        play()
        end_time = time.time()
        print(f"{(i+1)}) Nodes visited {config.COUNTER}", end=", ")
        config.COUNTER = 0
        print(f"Time elapsed: {round((end_time - start_time),2)} s")
