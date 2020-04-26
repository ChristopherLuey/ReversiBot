# File: Board.py
# Written By: Kyler Rosen
# Date: 4/28/20
# Finds the most effective move

from Board import *
import copy

#https://en.wikipedia.org/wiki/Alpha–beta_pruning
def valueFunction(e):
    matrix = [[3.0, 0.3, 0.3, 0.5, 0.5, 0.3, 0.3, 3.0],
                    [0.3, 0.3, 0.3, 0.5, 0.5, 0.3, 0.3, 0.3],
                    [0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3],
                    [0.5, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.5],
                    [0.5, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.5],
                    [0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3],
                    [0.3, 0.3, 0.3, 0.5, 0.5, 0.3, 0.3, 0.3],
                    [3.0, 0.3, 0.3, 0.5, 0.5, 0.3, 0.3, 3.0]]

    return matrix[e[0][0]][e[0][1]]

class Bot:
    def __init__(self, player):
        self.player = player


    def alphabeta(self, board, depth, alpha, beta, maximizingPlayer):
        if not maximizingPlayer:
            player = 1-self.player
        else:
            player = self.player


        legalMoves = board.calculateLegalMoves(player)

        boards = []
        tempboard = copy.deepcopy(board.getBoard())
        for move in legalMoves:
            anchor = []
            for index in range(len(legalMoves)):
                if move[0] == legalMoves[index][0]:
                    anchor.append(index)

            boardtemp = Board(copy.deepcopy(tempboard), board.getTurn(), player)
            boardtemp.setPlayer(board.getPlayerLegacy())
            boardtemp.move(copy.deepcopy(legalMoves), copy.deepcopy(anchor), boardtemp.getPlayer())
            boardtemp.calculateFlipSquares(copy.deepcopy(legalMoves), copy.deepcopy(anchor), player)
            boards.append(boardtemp)

        if depth == 0 or legalMoves == []:
            eval = board.evaluateBoard()
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
