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
		legalMoves = board.calculateLegalMoves(board.getPlayer())
		boards = []

		for move in legalMoves:
			boards.append(board.copy().move(move))

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

			return [value,maxBoard,maxChoice]		