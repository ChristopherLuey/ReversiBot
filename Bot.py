



class Bot:

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