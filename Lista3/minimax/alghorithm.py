from copy import deepcopy
import pygame
from backend import config
from backend.config import *

BLACK = (0,0,0)
WHITE = (255,255,255)

def minimax(curr_board,depth,max_player,game, best_moves = []):
    config.COUNTER += 1

    if depth == 0 or curr_board.winner() != None:
        if config.EVALUATE == 1:
            return curr_board.evaluate1(), curr_board
        if config.EVALUATE == 2:
            return curr_board.evaluate2(), curr_board
    
    if max_player:
        maxEval = float('-inf')

        for move in get_all_moves(curr_board, game):
            evaluation = minimax(move,depth-1,False,game,best_moves)[0]
            if maxEval == evaluation and depth == config.DEPTH:
                best_moves.append(move)
            if maxEval < evaluation:
                maxEval = evaluation
                if depth == config.DEPTH:
                    if len(best_moves) > 0:
                        best_moves.clear()
                    best_moves.append(move)
        return maxEval, best_moves

    else:
        minEval = float('inf')

        for move in get_all_moves(curr_board, game):
            evaluation = minimax(move,depth-1,True,game,best_moves)[0]
            if minEval == evaluation and depth == config.DEPTH:
                best_moves.append(move)
            if minEval > evaluation:
                minEval = evaluation
                if depth == config.DEPTH:
                    if len(best_moves) > 0:
                        best_moves.clear()
                    best_moves.append(move)
        return minEval, best_moves

def minimax_with_prun(curr_board,depth,max_player,game,best_moves = [],alpha=float('-inf'),beta=float('inf')):
    config.COUNTER += 1

    if depth == 0 or curr_board.winner() != None:
        if config.EVALUATE == 1:
            return curr_board.evaluate1(), curr_board
        if config.EVALUATE == 2:
            return curr_board.evaluate2(), curr_board
    
    if max_player:
        for move in get_all_moves(curr_board, game):
            evaluation = minimax_with_prun(move,depth-1,False,game,best_moves,alpha,beta)[0]
            if evaluation == alpha and depth == config.DEPTH:
                # print(alpha,beta)
                # print(best_moves)
                best_moves.append(move)
            elif evaluation > alpha:
                alpha = evaluation
                if depth == config.DEPTH:
                    if len(best_moves) > 0:
                        best_moves.clear()
                    best_moves.append(move)
            if alpha >= beta:
                return alpha, best_moves
        return alpha, best_moves

    else:
        for move in get_all_moves(curr_board, game):
            evaluation = minimax_with_prun(move,depth-1,True,game,best_moves,alpha,beta)[0]
            if evaluation == beta and depth == config.DEPTH:
                best_moves.append(move)
            elif evaluation < beta:
                beta = evaluation
                if depth == config.DEPTH:
                    if len(best_moves) > 0:
                        best_moves.clear()
                    best_moves.append(move)
            if alpha >= beta:
                return beta, best_moves
        return beta, best_moves

def simulate_move(pawn,movement,board,skip):
    # print(skip_move)
    if skip:
        board.move_pawn(pawn, movement[0], movement[1], True)
        board.remove(skip)
    else:
        board.move_pawn(pawn, movement[0], movement[1], False)

    return board

def get_all_moves(board, game):
    moves = []

    for pawn in board.get_all_pawns(game.turn):
        valid_moves = board.get_valid(pawn)
        # print(valid_moves)
        for move, skip in valid_moves.items():
            # print(move,skip)
            temp_board = deepcopy(board)
            temp_pawn = temp_board.get_pawn(pawn.row,pawn.col)
            new_board = simulate_move(temp_pawn,move,temp_board,skip)
            moves.append(new_board)

    # print(moves)
    return moves
