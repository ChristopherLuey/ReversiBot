# File: Board.py
# Written By: Kyler Rosen
# Date: 4/28/20
# Finds the most effective move

from Board import *
import copy

#https://en.wikipedia.org/wiki/Alpha–beta_pruning


class Bot:
    def __init__(self, player):
        self.player = player


    def alphabeta(self, board, depth, alpha, beta, maximizingPlayer):
    	#determines which player perpective to look at
        if not maximizingPlayer: player = 1-self.player
        else: player = self.player


        legalMoves = board.calculateLegalMoves(player)

        boards = []
        #creates a list of board scenarios that will be simulated on
        tempboard = copy.deepcopy(board.getBoard())
        for move in legalMoves:
            anchor = []
            for index in range(len(legalMoves)):
                if move[0] == legalMoves[index][0]:
                    anchor.append(index)

            boardtemp = Board(copy.deepcopy(tempboard), board.getTurn()+1, player)
            boardtemp.setPlayer(board.getPlayerLegacy())
            boardtemp.move(copy.deepcopy(legalMoves), copy.deepcopy(anchor), boardtemp.getPlayer())
            boardtemp.calculateFlipSquares(copy.deepcopy(legalMoves), copy.deepcopy(anchor), player)
            boards.append(boardtemp)

        #ends the recursion if the bot checks enough steps ahead
        if depth == 0 or legalMoves == []:
            eval = board.evaluateBoard()
            return eval, board, [0,0]

        #maximizes possible score
        if maximizingPlayer:
            value = -float("inf")

            for boardVar in boards:
                calcValue, l, m = self.alphabeta(boardVar, depth - 1, alpha, beta,False)

                #stores highest scoring board
                if calcValue > value:
                    value = calcValue
                    maxBoard = boardVar
                    maxChoice = legalMoves[boards.index(boardVar)][0]

                #checks if its possible for other branches to achieve higher scores
                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return value, maxBoard, maxChoice

        #mimimizes possible score
        else:
            value = float("inf")

            for boardVar in boards:
                calcValue, l, m = self.alphabeta(boardVar, depth - 1, alpha, beta,True)

                #stores lowest scoring board
                if calcValue < value:
                    value = calcValue
                    maxBoard = boardVar
                    maxChoice = legalMoves[boards.index(boardVar)][0]

                #checks if its possible for other branches to achieve lower scores
                beta = min(beta, value)
                if alpha >= beta:
                    break

            return value, maxBoard, maxChoice
