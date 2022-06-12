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


class AIPlayer:
    def __init__(self):
        pass

    def makeAMove(self, game: Game):
        legal = game.showLegalMoves()

        max_score = -math.inf
        best_move = random.choice(legal)
        for move in legal:
            board_n = game.getBoard()
            utils.makeAMove(board_n, move, AI_VALUE)

            score = score_position(board_n, AI_VALUE)

            if score > max_score:
                max_score = score
                best_move = move
        return game.makeAMove(best_move)
