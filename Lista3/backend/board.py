from copy import deepcopy
import pygame
from .config import *
from .pawn import Pawn

class Board():
    def __init__(self) -> None:
        self.board = []
        self.w_pawns = 8
        self.b_pawns = 8
        self.w_queens = 0
        self.b_queens = 0
    
    def draw_squares(self, window):
        window.fill(BLACK)

        for r in range(ROWS):
            for c in range(r % 2, COLS, 2):
                pygame.draw.rect(window, WHITE, (r*FIELD_SIZE, c*FIELD_SIZE, FIELD_SIZE, FIELD_SIZE))

    def init_pawns(self):
        for r in range(ROWS):
            self.board.append([])
            for c in range(COLS):
                if c % 2 == ((r + 1) % 2):
                    if r < 2:
                        self.board[r].append(Pawn(r, c, BLACK, DARK_GOLD))
                    elif r > 5:
                        self.board[r].append(Pawn(r, c, WHITE, LIGHT_GOLD))
                    else:
                        self.board[r].append(0)
                else:
                    self.board[r].append(0)

    def get_all_pawns(self, color):
        pawns = []
        for row in self.board:
            for pawn in row:
                if pawn != 0 and pawn.color == color:
                    #print(pawn)
                    pawns.append(pawn)
        return pawns
    
    def move_pawn(self, pawn, row, col, skip_move):
        if isinstance(pawn, Pawn):
            self.board[pawn.row][pawn.col], self.board[row][col] =  self.board[row][col], self.board[pawn.row][pawn.col]
            pawn.move(row, col)
            # print(pawn)
            if (row == ROWS - 1 and pawn.color == BLACK) or (row == 0 and pawn.color == WHITE) and not skip_move:
                pawn.promote_to_queen()
                if pawn.color == WHITE:
                    self.w_queens += 1
                else:
                    self.b_queens += 1

    def get_pawn(self, row, col):
        return self.board[row][col]

    def draw_board(self, window):
        self.draw_squares(window)
        for r in range(ROWS):
            for c in range(COLS):
                pawn = self.board[r][c]
                
                if pawn != 0:
                    pawn.draw(window)

    def remove(self, pawns):
        for pawn in pawns:
            self.board[pawn.row][pawn.col] = 0

    def get_valid(self, pawn):
        moves = {}

        col = pawn.col

        row = pawn.row

        if pawn.color == BLACK:
            moves.update(self._test_traverse_left(row, col, pawn.color, pawn.queen, [], 1))
            moves.update(self._test_traverse_right(row, col, pawn.color, pawn.queen, [], 1))
            moves.update(self._test_traverse_left(row, col, pawn.color, pawn.queen, [], -1))
            moves.update(self._test_traverse_right(row, col, pawn.color, pawn.queen, [], -1))
        if pawn.color == WHITE:
            moves.update(self._test_traverse_left(row, col, pawn.color, pawn.queen, [], -1))
            moves.update(self._test_traverse_right(row, col, pawn.color, pawn.queen, [], -1))
            moves.update(self._test_traverse_left(row, col, pawn.color, pawn.queen, [], 1))
            moves.update(self._test_traverse_right(row, col, pawn.color, pawn.queen, [], 1))
        
        if moves:
            max_skip_len = max(len(v) for k, v in moves.items())
        else:
            max_skip_len = 0
        only_skipped = {k: v for k, v in moves.items() if len(v) == max_skip_len}

        return only_skipped

    def _test_traverse_left(self, row, col, color, queen, skipped_pawns, direction):
        moves = {}
        skipped = deepcopy(skipped_pawns)
        if col - 1 >= 0 and row + direction >= 0 and row + direction < ROWS:
            field = self.board[row + direction][col - 1]

            if field == 0 and not skipped:
                if (direction == 1 and color == BLACK) or (direction == -1 and color == WHITE) or queen:
                    moves[(row + direction, col - 1)] = skipped_pawns
                    if queen and col - 1 >= 0 and row + direction < ROWS and row + direction >= 0:
                        moves.update(self._test_traverse_left(row + direction, col - 1, color, queen, skipped, direction))
            elif field != 0 and field not in skipped_pawns:
                if col - 2 >= 0 and row + 2*direction < ROWS and row + 2*direction >= 0 and field.color != color:
                    behind = self.board[row + 2*direction][col - 2]
                    if behind == 0:
                        skipped.append(field)
                        moves[(row + 2*direction, col - 2)] = skipped
                        moves.update(self._test_traverse_left(row + 2*direction, col - 2, color, queen, skipped, direction))
                        moves.update(self._test_traverse_right(row + 2*direction, col - 2, color, queen, skipped, direction))
                        moves.update(self._test_traverse_left(row + 2*direction, col - 2, color, queen, skipped, -direction))
        
        return moves

    def _test_traverse_right(self, row, col, color, queen, skipped_pawns, direction):
        moves = {}
        skipped = deepcopy(skipped_pawns)
        if col + 1 < COLS and row + direction >= 0 and row + direction < ROWS:
            field = self.board[row + direction][col + 1]

            if field == 0 and not skipped:
                if (direction == 1 and color == BLACK) or (direction == -1 and color == WHITE) or queen:
                    moves[(row + direction, col + 1)] = skipped_pawns
                    if queen and col + 1 < COLS and row + direction < ROWS and row + direction >= 0:
                        moves.update(self._test_traverse_right(row + direction, col + 1, color, queen, skipped, direction))
            elif field != 0 and field not in skipped_pawns:
                if col + 2 < COLS and row + 2*direction < ROWS and row + 2*direction >= 0 and field.color != color:
                    behind = self.board[row + 2*direction][col + 2]
                    if behind == 0:
                        # print(field)
                        skipped.append(field)
                        moves[(row + 2*direction, col + 2)] = skipped
                        moves.update(self._test_traverse_left(row + 2*direction, col + 2, color, queen, skipped, direction))
                        moves.update(self._test_traverse_right(row + 2*direction, col + 2, color, queen, skipped, direction))
                        moves.update(self._test_traverse_right(row + 2*direction, col + 2, color, queen, skipped, -direction))
            
        return moves

    # new
    def field_to_eval(self, field):
        if field.color == BLACK:
            if field.queen:
                return (0, 2)
            else:
                return (0, 1)
        else:
            if field.queen:
                return (2, 0)
            else:
                return (1, 0)
    
    def evaluate1(self):
        w_score = 0
        b_score = 0
        for row in range(ROWS):
            for col in range(COLS):
                field = self.board[row][col]
                if  field != 0:
                    evaluated = self.field_to_eval(field)
                    if row == 0 or col == 0 or row == ROWS - 1 or col == COLS - 1:
                        w_score += evaluated[0]
                        b_score += evaluated[1]
                    elif row < 2 or col < 2 or row > 5 or col > 5:
                        w_score += 1.5*evaluated[0]
                        b_score += 1.5*evaluated[1]
                    else:
                        w_score += 2*evaluated[0]
                        b_score += 2*evaluated[1]
                        
        # print(w_score, b_score)
        return w_score - b_score
    
    def evaluate2(self):
        w_score = 0
        b_score = 0
        for row in range(ROWS):
            for col in range(COLS):
                field = self.board[row][col]
                if  field != 0:
                    evaluated = self.field_to_eval(field)
                    if col <= 1:
                        if evaluated[0] != 0:
                            w_score += evaluated[0]
                        else:
                            b_score += 2*evaluated[1]
                    elif col <= 3:
                        if evaluated[0] != 0:
                            w_score += 1.25*evaluated[0]
                        else:
                            b_score += 1.75*evaluated[1]
                    elif col <= 5:
                        if evaluated[0] != 0:
                            w_score += 1.5*evaluated[0]
                        else:
                            b_score += 1.5*evaluated[1]
                    elif col <= 7:
                        if evaluated[0] != 0:
                            w_score += 1.75*evaluated[0]
                        else:
                            b_score += 1.25*evaluated[1]
                    else:
                        if evaluated[0] != 0:
                            w_score += 2*evaluated[0]
                        else:
                            b_score += evaluated[1]
                    
                        
        # print(w_score, b_score)
        return w_score - b_score

    def winner(self):
        if self.b_pawns <= 0 and self.b_queens <= 0:
            return WHITE
        elif self.w_pawns <= 0 and self.w_queens <= 0:
            return BLACK

        return None
