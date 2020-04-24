# File: Board.py
# Written By: Kyler Rosen
# Date: 4/28/20
# Finds the most effective move

from Board import *

#https://en.wikipedia.org/wiki/Alpha–beta_pruning

class Bot:

	def __init__(self, player, boardState, turn):
		self.player = player
		self.board = Board(boardState, turn, player)

	def alphabeta(board, depth, alpha, beta, maximizingPlayer):
		legalMoves = board.calculateLegalMoves(self.player)
		boards = []

		for move in legalMoves:
            for index in range(len(validMove)):
                if move[0] == validMove[index][0]:
                    anchor.append(index)
            board = board.copy()
            board.calculateFlipSquares(legalMoves, anchor, board.getPlayer())
            boards.append(board)

		if depth == 0 or legalMoves == []:
		    return board.evaluateBoard()

		if maximizingPlayer:
			value = -float("inf")

			for board in boards:
				calcValue = alphabeta(child, depth − 1, alpha, beta,False)[0]

				if calcValue > value:
					value = calcValue
					maxBoard = board
					maxChoice = legalMoves[boards.index(board)]

				alpha = max(alpha, value)
				if alpha >= beta:
					break

			return [value,maxBoard,maxChoice]

		else:
			value = float("inf")

			for board in boards:
				calcValue = alphabeta(child, depth − 1, alpha, beta,True)[0]

			   	if calcValue < value:
			   		value = calcValue
			   		maxBoard = board
			   		maxChoice = legalMoves[boards.index(board)]

				beta = min(beta, value)
				if alpha >= beta:
					break

<<<<<<< HEAD
			return value
=======
			return [value,maxBoard,maxChoice]		
>>>>>>> a8933a3381f1fddf606795e7af9c9c883053f613
