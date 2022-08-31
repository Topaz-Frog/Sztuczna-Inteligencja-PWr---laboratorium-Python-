import pygame
import random
from backend import config

from backend.board import Board
from backend.config import *
from minimax.alghorithm import minimax, minimax_with_prun

class Rules():
    def __init__(self, window) -> None:
        self.selected_pawn = None
        self.board = Board()
        self.turn = WHITE
        self.valid = {}

        self.window = window
        self.font = pygame.font.SysFont('Comic Sans MS', 50)
        self.win_text = ''
        self.all_valid = {}
        self.queens_move_counter = 0
        self.board.init_pawns()

    def update(self):
        self.board.draw_board(self.window)
        if self.selected_pawn is not None:
            self.draw_valid(self.valid)
        text = self.font.render(self.win_text, False, LIGHT_BLUE)
        self.window.blit(text, (WIDTH/2-50, HEIGHT/2-50))
        pygame.display.update()
        self.check_win_cond()

        if self.turn == BLACK and PLAYERS[1] == 'BOT':
            best_moves = minimax(self.board, config.DEPTH, False, self)[1]
            if len(best_moves) > 0:
                # self.ai_move(random.choice(best_moves))
                if self.win_text != '':
                    print(config.MOVES)
                self.ai_move(best_moves[0])
                config.MOVES += 1
            # pygame.time.delay(config.DELAY)
        elif self.turn == WHITE and PLAYERS[0] == 'BOT':
            best_moves = minimax(self.board, config.DEPTH, True, self)[1]
            if len(best_moves) > 0:
                # self.ai_move(random.choice(best_moves))
                if self.win_text != '':
                    print(config.MOVES)
                self.ai_move(best_moves[0])
                config.MOVES += 1
            # pygame.time.delay(config.DELAY)
        # print('update')

    def check_all_moves(self):
        self.all_valid = {}
        for r in range(ROWS):
            for c in range(COLS):
                if self.board.board[r][c] != 0:
                    if self.board.board[r][c].color == self.turn:
                        self.all_valid[(r, c)] = self.board.get_valid(self.board.board[r][c])
        
        max_skip_len = 0

        for k, v in self.all_valid.items():
            for k_pawn, v_pawn in v.items():
                if len(v_pawn) > max_skip_len:
                    max_skip_len = len(v_pawn)

        only_max_skipped = {}
        for k, v in self.all_valid.items():
            for k_pawn, v_pawn in v.items():
                if len(v_pawn) == max_skip_len:
                    only_max_skipped[k] = v
        self.all_valid = only_max_skipped

        if not self.all_valid:
            return True
        
        return False

    def check_win_cond(self):
        if self.board.w_pawns == 0 and self.board.w_queens == 0:
            self.win_text = "Black won!"
        elif self.board.b_pawns == 0 and self.board.b_queens == 0:
            self.win_text = "White won!"
        elif self.check_all_moves():
            if self.turn == WHITE:
                self.win_text = "Black won!"
            else:
                self.win_text = "White won!"
        elif self.queens_move_counter == 15:
            self.win_text = "Draw!"
        # if self.win_text != '':
        #     print(self.win_text)
    
    def reset(self):
        self._init()

    def select_pos(self, row, col):
        if self.selected_pawn:
            result = self._move(row, col)
            if not result:
                self.selected_pawn = None
                self.select_pos(row, col)
        
        pawn = self.board.get_pawn(row, col)
        if pawn != 0 and pawn.color == self.turn:
            if (pawn.row, pawn.col) in self.all_valid:
                self.selected_pawn = pawn
                self.valid = self.all_valid[(pawn.row, pawn.col)]
                return True
        
        return False

    def _move(self, row, col):
        field = self.board.get_pawn(row, col)
        if self.selected_pawn and field == 0 and (row, col) in self.valid:
            skipped_pawns = self.valid[(row, col)]
            if skipped_pawns:
                self.board.move_pawn(self.selected_pawn, row, col, True)
                if self.selected_pawn.queen:
                    self.queens_move_counter = 0
            else:
                self.board.move_pawn(self.selected_pawn, row, col, False)
                if self.selected_pawn.queen:
                    self.queens_move_counter += 1
            if skipped_pawns:
                self.board.remove(skipped_pawns)
            self.next_turn()
        else:
            return False
        return True

    def draw_valid(self, moves):
        for move in moves:
            r, c = move
            pygame.draw.rect(self.window, BLUE, (c*FIELD_SIZE, r*FIELD_SIZE, FIELD_SIZE, FIELD_SIZE))
    
    def next_turn(self):
        self.valid = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    # new
    def get_board(self):
        return self.board
    
    def ai_move(self, board):
        self.board = board
        self.next_turn()
