from copy import deepcopy
import pygame
from backend import config
from backend.config import *

BLACK = (0,0,0)
WHITE = (255,255,255)

#def minimax_with_prun(curr_board,depth,max_player,game,best_moves = [],alpha=float('-inf'),beta=float('inf')):
def minimax(curr_board, depth, max_player, game, starting_turn, best_moves = {}):
    config.COUNTER += 1

    if depth == 0 or curr_board.winner() != None:
        check = 0
        if starting_turn == WHITE:
            check = config.EVAS[0]
        else:
            check = config.EVAS[1]
        if check == 1:
            return curr_board.field_heur(), curr_board
        elif check == 2:
            return curr_board.pawn_heur(), curr_board
        else:
            return curr_board.field_heur() + curr_board.pawn_heur(), curr_board
    
    if max_player:
        max_eval = float('-inf')

        for move, queen in get_all_moves(curr_board, WHITE).items():
            evaluation = minimax(move,depth-1,False,game,starting_turn,best_moves)[0]
            if max_eval == evaluation and depth == config.DEPTH:
                best_moves[move] = queen
            if max_eval < evaluation:
                max_eval = evaluation
                if depth == config.DEPTH:
                    best_moves.clear()
                    best_moves[move] = queen
        return max_eval, best_moves

    else:
        min_eval = float('inf')

        for move, queen in get_all_moves(curr_board, BLACK).items():
            evaluation = minimax(move,depth-1,True,game,starting_turn,best_moves)[0]
            if min_eval == evaluation and depth == config.DEPTH:
                best_moves[move] = queen
            if min_eval > evaluation:
                min_eval = evaluation
                if depth == config.DEPTH:
                    best_moves.clear()
                    best_moves[move] = queen
        return min_eval, best_moves

def minimax_with_prun(curr_board, depth, max_player, game, starting_turn, best_moves = {}, alpha=float('-inf'), beta=float('inf')):
    config.COUNTER += 1

    if depth == 0 or curr_board.winner() != None:
        check = 0
        if starting_turn == WHITE:
            check = config.EVAS[0]
        else:
            check = config.EVAS[1]
        if check == 1:
            return curr_board.field_heur(), curr_board
        elif check == 2:
            return curr_board.pawn_heur(), curr_board
        else:
            return curr_board.field_heur() + curr_board.pawn_heur(), curr_board
    
    if max_player:
        for move, queen in get_all_moves(curr_board, WHITE).items():
            evaluation = minimax_with_prun(move,depth-1,False,game,starting_turn,best_moves,alpha,beta)[0]
            if evaluation == alpha and depth == config.DEPTH:
                best_moves[move] = queen
            elif evaluation > alpha:
                alpha = evaluation
                if depth == config.DEPTH:
                    best_moves.clear()
                    best_moves[move] = queen
            if alpha >= beta:
                return alpha, best_moves
        return alpha, best_moves

    else:
        for move, queen in get_all_moves(curr_board, BLACK).items():
            evaluation = minimax_with_prun(move,depth-1,True,game,starting_turn,best_moves,alpha,beta)[0]
            if evaluation == beta and depth == config.DEPTH:
                best_moves[move] = queen
            elif evaluation < beta:
                beta = evaluation
                if depth == config.DEPTH:
                    best_moves.clear()
                    best_moves[move] = queen
            if alpha >= beta:
                return beta, best_moves
        return beta, best_moves

def simulate_move(pawn,movement,board,skip):
    if skip:
        board.move_pawn(pawn, movement[0], movement[1], True)
        board.remove(skip)
    else:
        board.move_pawn(pawn, movement[0], movement[1], False)

    return board

def get_all_moves(board, color):
    all_valid = {}
    moves = {}

    max_skipped = 0
    for pawn in board.get_all_pawns(color):
        valid_moves = board.get_valid(pawn)
        all_valid[pawn] = {}
        for move, skip in valid_moves.items():
            if len(skip) > max_skipped:
                max_skipped = len(skip)
                all_valid = {}
                all_valid[pawn] = {move: skip}
            elif len(skip) == max_skipped:
                all_valid[pawn].update({move: skip})
            
    for pawn, valid in all_valid.items():
        for move, skip in valid.items():
            temp_board = deepcopy(board)
            temp_pawn = temp_board.get_pawn(pawn.row,pawn.col)
            new_board = simulate_move(temp_pawn,move,temp_board,skip)
            if len(skip) > 0:
                moves[new_board] = False
            else:
                moves[new_board] = pawn.queen
    return moves
