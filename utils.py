import numpy as np
from constants import *


def isInLine(line, match):
    if match in ''.join(line.astype(str).tolist()):
        return True
    return False


def checkForVictory(board, player, row, col):
    pattern = str(player) * 4

    # row
    line = np.copy(board[row, :])
    if isInLine(line, pattern):
        return True

    # col
    line = np.copy(board[:, col])
    if isInLine(line, pattern):
        return True

    # diagonal 1
    line = np.copy(np.diagonal(board, offset=(col - row)))
    if isInLine(line, pattern):
        return True

    # diagonal 2
    line = np.copy(np.diagonal(np.rot90(board), offset=-board.shape[1] + (col + row) + 1))
    if isInLine(line, pattern):
        return True

    return False


def showLegalMoves(board):
    legal = list()
    for col in range(BOARD_WIDTH):
        if board[0][col] == VOID_VALUE:
            legal.append(col)
    return legal


def print_s(text):
    print(text, end='')


def print_board(board):
    for _ in range(BOARD_WIDTH + 2):
        print_s('█')
    print()
    for i in range(BOARD_HEIGHT):
        print_s('█')
        for j in range(BOARD_WIDTH):
            if board[i][j] == HUMAN_VALUE:
                print_s(HUMAN_LABEL)
            elif board[i][j] == AI_VALUE:
                print_s(AI_LABEL)
            else:
                print_s(VOID_LABEL)
        print_s('█')
        print()
    for _ in range(BOARD_WIDTH + 2):
        print_s('█')
    print()
    print_s('█')
    legal = showLegalMoves(board)
    for i in range(BOARD_WIDTH):
        if legal.__contains__(i):
            print_s(i)
        else:
            print_s(' ')
    print('█')
    print()
    print()


def getNextOpenRow(board, col):
    row = BOARD_HEIGHT - 1
    while row >= 0:
        if board[row][col] == VOID_VALUE:
            return row
        else:
            row -= 1

    raise Exception("Cannot place a piece in the col {}!", col)


def makeAMove(board, col, value):
    row = getNextOpenRow(board, col)

    board[row][col] = value

    return row

def createEmptyBoard():
    return np.zeros((BOARD_HEIGHT, BOARD_WIDTH), dtype=int)
