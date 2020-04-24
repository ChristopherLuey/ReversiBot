


class Board:
    def __init__(self, boardState):
        self.player = player # 0: black, 1: white
        self.weightMatrix = Matrix()

        # Define Constants
        self.stableDiskWeight = 0.0
        self.interiorDiskWeight = 0.0
        self.frontierDiskWeight = 0.0
        self.flipWeight = 0.0
        self.weightMatrixWeight = 0.0
        self.potentialMovesWeight = 0.0
        self.opponentPotentialMovesWeight = 0.0
        self.opponentPotentialFlipsWeight = 0


        self.stableDiskCount = 0
        self.interiorDiskCount = 0
        self.frontierDiskCount = 0
        self.potentialMobility = 0.0
        self.opponentPotentialMobility = 0.0
        self.potentialFlips = 0
        self.opponentPotentialFlips = 0

        self.stableDiskCountMaximium = self.calculatePossibleStableDisks()
        self.interiorDiskCountMaximium = self.calculatePossibleInteriorDisks()
        self.frontierDiskCountMaximium = self.calculatePossibleFrontierDisks()
        self.potentialMobilityMaximium = self.calculatePossiblePotentialMobility()

        self.turn = 0

        # Corner, edges, buffer
        # Stable disks: cannot flip
        # Frontier vs interior disks: maximize interior disks


    def evaluateBoard(self, boardState):
        # val is if the board is good or not
        howGoodTheBoardIsBasedOnHowMuchWeWeightThings = 0

        val = self.stableDiskWeight*self.stableDiskCount/self.stableDiskCountMaximium
        return howGoodTheBoardIsBasedOnHowMuchWeWeightThings

    def



class Matrix:
    def __init__(self):
        self.matrix = []
        for i in range(8):
            self.matrix.append([])
            for j in range(8):
                self.matrix[i].append(0.0)

    def adjustWeight(self, row, col, weight):
        self.weightMatrix[row][col] = weight
