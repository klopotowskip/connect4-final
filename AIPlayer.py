import math
import random

import utils
from game import Game
from constants import *


def getChunkPoints(chunk, piece):
    enemy_piece = AI_VALUE if piece == HUMAN_VALUE else AI_VALUE
    score = 0

    if chunk.count(piece) == 4:
        score += 100
    elif chunk.count(piece) == 3 and chunk.count(VOID_VALUE) == 1:
        score += 10
    elif chunk.count(piece) == 2 and chunk.count(VOID_VALUE) == 2:
        score += 3

    if chunk.count(enemy_piece) == 3 and chunk.count(VOID_VALUE) == 1:
        score -= 6

    return score


def getPositionPoints(board, piece):
    points = 0

    # Bonus from center column
    center_array = [int(i) for i in list(board[:, BOARD_WIDTH // 2])]
    center_count = center_array.count(piece)
    points += 3 * center_count

    for r in range(BOARD_HEIGHT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(BOARD_WIDTH - 3):
            chunk = row_array[c:c + CHUNK_SIZE]
            points += getChunkPoints(chunk, piece)

    for c in range(BOARD_WIDTH):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(BOARD_HEIGHT - 3):
            chunk = col_array[r:r + CHUNK_SIZE]
            points += getChunkPoints(chunk, piece)

    for r in range(BOARD_HEIGHT - 3):
        for c in range(BOARD_WIDTH - 3):
            chunk = [board[r + i][c + i] for i in range(CHUNK_SIZE)]
            points += getChunkPoints(chunk, piece)

    for r in range(BOARD_HEIGHT - 3):
        for c in range(BOARD_WIDTH - 3):
            chunk = [board[r + 3 - i][c + i] for i in range(CHUNK_SIZE)]
            points += getChunkPoints(chunk, piece)

    return points


def winning_move(board, player_value):
    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT):
            if board[r][c] == player_value and board[r][c + 1] == player_value and board[r][c + 2] == player_value and board[r][c + 3] == player_value:
                return True

    for c in range(BOARD_WIDTH):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == player_value and board[r + 1][c] == player_value and board[r + 2][c] == player_value and board[r + 3][c] == player_value:
                return True

    for c in range(BOARD_WIDTH - 3):
        for r in range(BOARD_HEIGHT - 3):
            if board[r][c] == player_value and board[r + 1][c + 1] == player_value and board[r + 2][c + 2] == player_value and board[r + 3][c + 3] == player_value:
                return True

    for c in range(BOARD_WIDTH - 3):
        for r in range(3, BOARD_HEIGHT):
            if board[r][c] == player_value and board[r - 1][c + 1] == player_value and board[r - 2][c + 2] == player_value and board[r - 3][c + 3] == player_value:
                return True


def is_terminal_node(board):
    return winning_move(board, HUMAN_VALUE) or winning_move(board, AI_VALUE) or len(utils.showLegalMoves(board)) == 0


def minimax(board, level, alpha, beta, maximizing):
    valid_locations = utils.showLegalMoves(board)
    is_terminal = is_terminal_node(board)

    if is_terminal:
        if winning_move(board, AI_VALUE):
            return None, math.inf
        elif winning_move(board, HUMAN_VALUE):
            return None, -math.inf
        else:
            return None, 0
    elif level == 0:
        return None, getPositionPoints(board, AI_VALUE)

    if maximizing:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            board_c = board.copy()
            utils.makeAMove(board_c, col, AI_VALUE)
            new_score = minimax(board_c, level - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            board_c = board.copy()
            utils.makeAMove(board_c, col, HUMAN_VALUE)
            new_score = minimax(board_c, level - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def bestMovePossible(board, piece):
    legal_moves = utils.showLegalMoves(board)

    max_points = -math.inf
    max_points_col = random.choice(legal_moves)

    for col in legal_moves:
        temp_board = board.copy()
        utils.makeAMove(temp_board, col, piece)
        score = getPositionPoints(temp_board, piece)

        if score > max_points:
            max_points = score
            max_points_col = col

    return max_points_col


class AIPlayer:
    def __init__(self):
        pass

    def makeAMove(self, game: Game):
        col, minimax_score = minimax(game.getBoard(), 6, -math.inf, math.inf, True)

        return game.makeAMove(col)
