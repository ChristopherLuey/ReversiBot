# File: Board.py
# Written By: Christopher Luey
# Date: 4/28/20
# Board class and Matrix class

from Board import *

#https://en.wikipedia.org/wiki/Alpha–beta_pruning

class Bot:
    def __init__(self, player, boardState, turn):
        self.player = player
        self.board = Board(boardState, turn, player)
        self.maxBoard, self.maxChoice = self.board, [-1,-1]


    def alphabeta(self, board, depth, alpha, beta, maximizingPlayer):
        legalMoves = board.calculateLegalMoves(self.player)
        boards = []
        for move in legalMoves:
            anchor = []
            for index in range(len(legalMoves)):
                if move[0] == legalMoves[index][0]:
                    anchor.append(index)
            boardtemp = board.copy()
            boardtemp.calculateFlipSquares(legalMoves, anchor, boardtemp.getPlayer())
            boards.append(boardtemp)

        if depth == 0 or legalMoves == []:
            eval = board.evaluateBoard()
            print(eval)
            return eval, board, [0,0]

        if maximizingPlayer:
            value = -float("inf")

            for boardVar in boards:
                calcValue, l, m = self.alphabeta(boardVar, depth - 1, alpha, beta,False)

                if calcValue > value:
                    value = calcValue
                    maxBoard = boardVar
                    maxChoice = legalMoves[boards.index(boardVar)][0]

                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return value, maxBoard, maxChoice

        else:
            value = float("inf")

            for boardVar in boards:
                calcValue, l, m = self.alphabeta(boardVar, depth - 1, alpha, beta,True)

                if calcValue < value:
                    value = calcValue
                    maxBoard = boardVar
                    maxChoice = legalMoves[boards.index(boardVar)][0]

                beta = min(beta, value)
                if alpha >= beta:
                    break

            return value, maxBoard, maxChoice
