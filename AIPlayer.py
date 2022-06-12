import math
import random

import utils
from game import Game
from constants import *


def assess_points(window, piece):
    enemy_piece = AI_VALUE if piece == HUMAN_VALUE else AI_VALUE
    score = 0

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(VOID_VALUE) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(VOID_VALUE) == 2:
        score += 3

    if window.count(enemy_piece) == 3 and window.count(VOID_VALUE) == 1:
        score -= 6

    return score


def score_position(board, piece):
    score = 0

    # Score center
    center_array = [int(i) for i in list(board[:, BOARD_WIDTH // 2])]
    center_count = center_array.count(piece)
    score += 3 * center_count

    # Horizontal
    for r in range(BOARD_HEIGHT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(BOARD_WIDTH - 3):
            window = row_array[c:c + CHUNK_SIZE]
            score += assess_points(window, piece)

    # Vertical
    for c in range(BOARD_WIDTH):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(BOARD_HEIGHT - 3):
            window = col_array[r:r + CHUNK_SIZE]
            score += assess_points(window, piece)

    # Positive sloped diag
    for r in range(BOARD_HEIGHT - 3):
        for c in range(BOARD_WIDTH - 3):
            window = [board[r + i][c + i] for i in range(CHUNK_SIZE)]
            score += assess_points(window, piece)

    # Negative sloped diag
    for r in range(BOARD_HEIGHT - 3):
        for c in range(BOARD_WIDTH - 3):
            window = [board[r + 3 - i][c + i] for i in range(CHUNK_SIZE)]
            score += assess_points(window, piece)

    return score


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(BOARD_WIDTH):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(BOARD_WIDTH - 3):
        for r in range(3, BOARD_HEIGHT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def is_terminal_node(board):
    return winning_move(board, HUMAN_VALUE) or winning_move(board, AI_VALUE) or len(utils.showLegalMoves(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = utils.showLegalMoves(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_VALUE):
                return None, 100000000000000
            elif winning_move(board, HUMAN_VALUE):
                return None, -10000000000000
            else:  # Game is over, no more valid moves
                return None, 0
        else:  # Depth is zero
            return None, score_position(board, AI_VALUE)
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = board.copy()
            utils.makeAMove(b_copy, col, AI_VALUE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = board.copy()
            utils.makeAMove(b_copy, col, HUMAN_VALUE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def pick_best_move(board, piece):
    valid_locations = utils.showLegalMoves(board)

    best_score = -9999999
    best_col = random.choice(valid_locations)

    for col in valid_locations:
        temp_board = board.copy()
        utils.makeAMove(temp_board, col, piece)
        score = score_position(temp_board, piece)

        if score > best_score:
            best_score = score
            best_col = col

    return best_col


class AIPlayer:
    def __init__(self):
        pass

    def makeAMove(self, game: Game):
        col, minimax_score = minimax(game.getBoard(), 6, -math.inf, math.inf, True)

        return game.makeAMove(col)
