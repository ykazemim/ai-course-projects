import numpy as np
from game import PLAYER, AI

def evaluate_window(window, piece):
    """
    Evaluate a window of 4 consecutive cells for a given piece.

    :param window: A list of 4 consecutive cells.
    :param piece: The piece to evaluate (PLAYER or AI).
    :return: A score based on the number of pieces in the window.
    """
    score = 0
    opp_piece = PLAYER if piece == AI else AI

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def evaluate_board(board, piece):
    """
    Evaluate the board and return a score based on potential winning moves and threats.

    :param board: The current game board.
    :param piece: The piece to evaluate (PLAYER or AI).
    :return: A score representing the board state.
    """
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, board.shape[1] // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(board.shape[0]):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(board.shape[1] - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(board.shape[1]):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(board.shape[0] - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    # Score positive diagonal
    for r in range(board.shape[0] - 3):
        for c in range(board.shape[1] - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negative diagonal
    for r in range(3, board.shape[0]):
        for c in range(board.shape[1] - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score