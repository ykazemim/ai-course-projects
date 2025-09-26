"""
engine.py

AI Algorithms: Implement the following functions:

- minimax
- alpha_beta_pruning
- expectimax

Each function should evaluate board states using a heuristic (see utils.py)
and return the best column to play.
"""

import random
from utils import evaluate_board
from game import ConnectFourGame, PLAYER, AI
ROW_COUNT, COLUMN_COUNT = 6,6
def minimax(game, depth, maximizing_player):
    """
    Minimax algorithm to determine the best move.

    :param game: Current game object (contains board state and methods).
    :param depth: Depth limit for recursion.
    :param maximizing_player: Boolean indicating if AI is maximizing.
    :return: Best column to play and its score.
    """
    valid_locations = game.get_valid_locations()
    is_terminal = game.winning_move(PLAYER) or game.winning_move(AI) or game.is_draw()
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if game.winning_move(AI):
                return (None, 100000000000000)
            elif game.winning_move(PLAYER):
                return (None, -100000000000000)
            else:  # Draw
                return (None, 0)
        else:  # Depth is zero
            return (None, evaluate_board(game.board, AI))
    
    if maximizing_player:
        value = -float('inf')
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = game.get_next_open_row(col)
            game.drop_piece(row, col, AI)
            new_score = minimax(game, depth - 1, False)[1]
            game.board[row][col] = 0  # Undo the move
            if new_score > value:
                value = new_score
                column = col
        return column, value
    
    else:  # Minimizing player
        value = float('inf')
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = game.get_next_open_row(col)
            game.drop_piece(row, col, PLAYER)
            new_score = minimax(game, depth - 1, True)[1]
            game.board[row][col] = 0  # Undo the move
            if new_score < value:
                value = new_score
                column = col
        return column, value


def alpha_beta_pruning(game, depth, alpha, beta, maximizing_player):
    """
    Alpha-Beta Pruning to optimize Minimax.

    :param game: Current game object (contains board state and methods).
    :param depth: Depth limit for recursion.
    :param alpha: Alpha value.
    :param beta: Beta value.
    :param maximizing_player: Boolean indicating if AI is maximizing.
    :return: Best column to play and its score.
    """
    valid_locations = game.get_valid_locations()
    is_terminal = game.winning_move(PLAYER) or game.winning_move(AI) or game.is_draw()
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if game.winning_move(AI):
                return (None, 100000000000000)
            elif game.winning_move(PLAYER):
                return (None, -100000000000000)
            else:  # Draw
                return (None, 0)
        else:  # Depth is zero
            return (None, evaluate_board(game.board, AI))
    
    if maximizing_player:
        value = -float('inf')
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = game.get_next_open_row(col)
            game.drop_piece(row, col, AI)
            new_score = alpha_beta_pruning(game, depth - 1, alpha, beta, False)[1]
            game.board[row][col] = 0  # Undo the move
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    
    else:  # Minimizing player
        value = float('inf')
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = game.get_next_open_row(col)
            game.drop_piece(row, col, PLAYER)
            new_score = alpha_beta_pruning(game, depth - 1, alpha, beta, True)[1]
            game.board[row][col] = 0  # Undo the move
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def expectimax(game, depth, maximizing_player):
    """
    Expectimax algorithm for environments with randomness.

    :param game: Current game object (contains board state and methods).
    :param depth: Depth limit for recursion.
    :param maximizing_player: Boolean indicating if AI is maximizing.
    :return: Best column to play and its score.
    """
    valid_locations = game.get_valid_locations()
    is_terminal = game.winning_move(PLAYER) or game.winning_move(AI) or game.is_draw()
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if game.winning_move(AI):
                return (None, 100000000000000)
            elif game.winning_move(PLAYER):
                return (None, -100000000000000)
            else:  # Draw
                return (None, 0)
        else:  # Depth is zero
            return (None, evaluate_board(game.board, AI))
    
    if maximizing_player:
        value = -float('inf')
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = game.get_next_open_row(col)
            game.drop_piece(row, col, AI)
            new_score = expectimax(game, depth - 1, False)[1]
            game.board[row][col] = 0  # Undo the move
            if new_score > value:
                value = new_score
                column = col
        return column, value
    
    else:  # Chance node (opponent's move)
        value = 0
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = game.get_next_open_row(col)
            game.drop_piece(row, col, PLAYER)
            new_score = expectimax(game, depth - 1, True)[1]
            game.board[row][col] = 0  # Undo the move
            value += new_score * (1.0 / len(valid_locations))  # Average the scores
        return column, value