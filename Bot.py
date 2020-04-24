# File: Board.py
# Written By: Christopher Luey
# Date: 4/28/20
# Board class and Matrix class

from Board import *

#https://en.wikipedia.org/wiki/Alpha–beta_pruning

class Bot:

<<<<<<< HEAD
    def __init__(self, player, boardState, turn):
        self.player = player
        self.board = Board(boardState, turn, player)

	# def alphabeta(node, depth, α, β, maximizingPlayer) is
	#     if depth = 0 or node is a terminal node then
    #           if maximizingPlayer:
    #                b = Board(boardstate, turn, player)
    #                utility = b.evaluateBoard()
    #           else:
    #                b = Board(boardstate, turn, 1-player)
    #                utility = -b.evaluateBoard()

	#         return the heuristic value of node
	#     if maximizingPlayer then
	#         value := −∞
	#         for each child of node do
	#             value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
	#             α := max(α, value)
	#             if α ≥ β then
	#                 break (* β cut-off *)
	#         return value
	#     else
	#         value := +∞
	#         for each child of node do
	#             value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
	#             β := min(β, value)
	#             if α ≥ β then
	#                 break (* α cut-off *)
	#         return value
=======
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
					bestBoard = board
					bestChoice = legalMoves[boards.index(board)]

				alpha = max(alpha, value)
				if alpha >= beta:
					break
			return value

		else:
			value = float("inf")
			for board in boards:
				calcValue = alphabeta(child, depth − 1, alpha, beta,True)[0]
			   	if calcValue < value:
			   		value = calcValue
			   		bestBoard = board
			   		bestChoice = legalMoves[boards.index(board)]

				beta = min(beta, value)
				if alpha >= beta:
					break

			return value		
>>>>>>> 368bff5ba7a424ce3ec1971bb8089a69b76e8c66
