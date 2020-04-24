



class Bot:

    def __init__(self, player, boardState, turn):
        self.player = player
        self.board = Board(boardState, turn, player)