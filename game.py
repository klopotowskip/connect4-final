import utils
from constants import *
import numpy as np


class Game:
    def __init__(self):
        self._roundCnt = 0
        self._isHumanTurn = True
        self._board = utils.createEmptyBoard()
        self.winner = None
        utils.print_board(self._board)

    def getBoard(self):
        """Returns the copy of a board"""
        return np.copy(self._board)

    def showLegalMoves(self):
        return utils.showLegalMoves(self._board)

    def makeAMove(self, col):
        value = HUMAN_VALUE if self._isHumanTurn else AI_VALUE

        row = utils.makeAMove(self._board, col, value)

        victory = utils.checkForVictory(self._board, value, row, col)
        if victory:
            self.winner = HUMAN_LABEL if value == HUMAN_VALUE else AI_LABEL

        utils.print_board(self._board)

        self._isHumanTurn = not self._isHumanTurn

        return victory
