import random
import pygame
import pandas as pd
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
    for eva_white in range(1,4):
        for eva_black in range(1,4):
            config.EVAS = [eva_white, eva_black]
            all_nodes = 0
            games = 1
            nodes_list = []
            times_list = []
            moves_list = []
            winners = []

            for i in range(games):
                config.MOVES = 0
                config.WINNER = None

                start_time = time.time()
                play()
                end_time = time.time()
                nodes_list.append(config.COUNTER)
                times_list.append(round((end_time - start_time),2))
                moves_list.append(config.MOVES)
                winners.append(config.WINNER)
                # print(f"{(i+1)}) Nodes visited {config.COUNTER}", end=", ")
                all_nodes += config.COUNTER
                config.COUNTER = 0
                # print(f"Time elapsed: {round((end_time - start_time),2)} s, Moves {config.MOVES}")
            print(config.DEPTH, config.ALPHA_BETA, config.EVAS[0], config.EVAS[1])
            print(all_nodes/games)

            # data = {"Nodes": nodes_list,
            #         "Times": times_list,
            #         "Moves": moves_list,
            #         "Winner": winners}

            # df = pd.DataFrame(data)

            # df.to_csv(f"archive/{config.ALPHA_BETA}_{config.DEPTH}_{config.EVALUATE}")
