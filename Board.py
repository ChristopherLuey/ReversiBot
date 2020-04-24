# File: Board.py
# Written By: Christopher Luey
# Date: 4/28/20
# Board class and Matrix class

from GUI import Tile
import math

class Board:
    def __init__(self, boardState, turn, player):
        self.weightMatrix = Matrix()
        self.boardState = boardState
        self.turn = turn
        self.player = player
        self.playerLegacy = player

        # Define Constants and Other Non-linear functions
        self.stableDiskWeight = 0.0
        self.interiorDiskWeight = 0.0
        self.frontierDiskWeight = 0.0
        # Overtime the number of tiles that the machine can flip becomes more valuable
        self.flipWeightPower = 2
        self.flipWeight = turn^self.flipWeightPower
        self.weightMatrixWeight = 0.0
        # Overtime potential moves becomes less valuable
        self.potentialMovesWeightBase = 2.0
        self.potentialMovesWeight = self.calculatePotentialMovesWeight(self.turn)

        self.opponentPotentialMovesWeight = -0.0
        self.opponentPotentialFlipsWeight = -0.0
        self.opponentStableDisksWeight = -0.0
        self.opponentFrontierDiskWeight = -0.0
        self.opponentInteriorDiskWeight = -0.0
        self.opponentFilpWeight = -0.0

        #
        self.stableDiskCount = 0
        self.interiorDiskCount = 0
        self.frontierDiskCount = 0
        self.potentialMobility = 0.0
        self.potentialFlips = 0
        self.numberOfTiles = 0

        self.opponentStableDiskCount = 0
        self.opponentInteriorDiskCount = 0
        self.opponentFrontierDiskCount = 0
        self.opponentPotentialMobility = 0.0
        self.opponentPotentialFlips = 0
        self.opponentNumberOfTiles = 0

        self.weightAdjustmentBias = 0.0

        # self.stableDiskCountMaximium = self.calculatePossibleStableDisks()
        # self.interiorDiskCountMaximium = self.calculatePossibleInteriorDisks()
        # self.frontierDiskCountMaximium = self.calculatePossibleFrontierDisks()
        # self.potentialMobilityMaximium = self.calculatePossiblePotentialMobility()

        self.turn = 0

        # Corner, edges, buffer
        # Stable disks: cannot flip
        # Frontier vs interior disks: maximize interior disks

    def evaluateBoard(self):
        # val is if the board is good or not

        self.stableDiskCount = self.calculateStableDiskCount(self.player)
        self.interiorDiskCount = self.calculateInteriorDiskCount(self.player)
        self.frontierDiskCount = self.calculateFrontierDiskCount(self.player)
        self.potentialMobility = self.calculateMobility(self.player)
        self.potentialFlips = self.calculateFlipTilesPotential(self.player)
        self.numberOfTiles = self.calculateNumberOfTiles(self.player)

        self.opponentStableDiskCount = self.calculateStableDiskCount(1-self.player)
        self.opponentInteriorDiskCount = self.calculateInteriorDiskCount(1-self.player)
        self.opponentFrontierDiskCount = self.calculateFrontierDiskCount(1-self.player)
        self.opponentPotentialMobility = self.calculateMobility(1-self.player)
        self.opponentPotentialFlips = self.calculateFlipTilesPotential(1-self.player)
        self.opponentNumberOfTiles = self.calculateNumberOfTiles(1-self.player)

        utility = self.utilityScore(self.stableDiskWeight, self.stableDiskCount) + \
                  self.utilityScore(self.interiorDiskWeight, self.interiorDiskCount) + \
                  self.utilityScore(self.frontierDiskWeight, self.frontierDiskCount) + \
                  self.utilityScore(self.opponentPotentialFlipsWeight, self.opponentPotentialFlips)



        if self.playerLegacy == self.player: return utility
        else: return -utility

    def copy(self):
        # Make a copy after changing to board state
        boardState = self.boardState.deepcopy()
        b = Board(boardState, self.turn, 1-self.player)
        return copy.deepcopy(b)


    def move(self, move):


    def getPlayer(self):
        return self.player

    def incrementTurns(self):
        self.turns+=1

    def utilityScore(self, weight, score):
        return weight*score

    def updateBoard(self, boardState):
        self.boardState = boardState

    def getBoardState(self):
        return self.boardState

    def calculateLegalMoves(self, player):
        self.legalMoves = []
        for row in range(len(self.boardState)):
            for col in range(len(self.boardState[0])):
                adjacentSquares = []
                if self.boardState[row][col].getOccupied() == ["black", "white"][player]:
                    for k in [-1, 1]:
                        if self.isWithinBoard(row + k, col + k) == ["black", "white"][1 - player]:
                            adjacentSquares.append(True)
                        else:
                            adjacentSquares.append(False)
                    for k in [-1, 1]:
                        if self.isWithinBoard(row, col + k) == ["black", "white"][1 - player]:
                            adjacentSquares.append(True)
                        else:
                            adjacentSquares.append(False)
                    for k in [-1, 1]:
                        if self.isWithinBoard(row + k, col) == ["black", "white"][1 - player]:
                            adjacentSquares.append(True)
                        else:
                            adjacentSquares.append(False)
                    for k in [-1, 1]:
                        if self.isWithinBoard(row + k, col - k) == ["black", "white"][1 - player]:
                            adjacentSquares.append(True)
                        else:
                            adjacentSquares.append(False)

                    factorList = [[-1, -1], [1, 1], [0, -1], [0, 1], [-1, 0], [1, 0], [-1, 1], [1, -1]]
                    for k in range(8):
                        if adjacentSquares[k] == True:
                            xFactor, yFactor = factorList[k][0], factorList[k][1]
                            while (1 <= xFactor + row <= 6) and (1 <= yFactor + col <= 6) and \
                                    self.boardState[xFactor + row][
                                        yFactor + col].getOccupied() == ["black", "white"][1 - player]:
                                try:
                                    if self.boardState[row + xFactor + factorList[k][0]][
                                        col + yFactor + factorList[k][1]].getOccupied() == "":
                                        legalMoves.append(
                                            [[row + xFactor + factorList[k][0], col + yFactor + factorList[k][1]],
                                             [row, col]])
                                except:
                                    break
                                xFactor, yFactor = xFactor + factorList[k][0], yFactor + factorList[k][1]
        return self.legalMoves

    def setPlayer(self, player):
        self.playerLegacy = player

    def calculateFlipSquares(self, legalMoves, anchor, player):
        numberOfFlips, flipedSquares = 0, []
        for k in anchor:
            dx, dy = legalMoves[k][0][0] - legalMoves[k][1][0], legalMoves[k][0][1] - legalMoves[k][1][1]
            for i in range(1, max(abs(dx), abs(dy))):
                try:
                    dirx = int(dx / abs(dx))
                except:
                    dirx = 0
                try:
                    diry = int(dy / abs(dy))
                except:
                    diry = 0
                self.boardState[legalMoves[k][1][0] + i * dirx][legalMoves[k][1][1] + i * diry].setOccupied(["black", "white"][player])
                flipedSquares.append([legalMoves[k][1][0] + i * dirx, legalMoves[k][1][1] + i * diry])
                numberOfFlips+=1
        return numberOfFlips, flipedSquares

    def isWithinBoard(self, r, c):
        try:
            return self.boardState[r][c].getOccupied()
        except:
            return ""

    def calculateScore(self):
        score = [0,0]
        for i in range(len(self.boardState)):
            for j in range(len(self.boardState[0])):
                if self.boardState[i][j].getOccupied() == "white":
                    score[1] = score[1] + 1
                elif self.boardState[i][j].getOccupied() == "black":
                    score[0] = score[0] + 1
        return score

    def calculateNumberOfTiles(self, player):
        return self.calculateScore()[player]

    def calculateFlipTilesPotential(self, player):
        legalMoves = self.calculateLegalMoves(player)
        anchor = list(range(len(legalMoves)))
        numberOfFlips, flipedSquares = 0, []
        for k in anchor:
            dx, dy = legalMoves[k][0][0] - legalMoves[k][1][0], legalMoves[k][0][1] - legalMoves[k][1][1]
            for i in range(1, max(abs(dx), abs(dy))):
                try:
                    dirx = int(dx / abs(dx))
                except:
                    dirx = 0
                try:
                    diry = int(dy / abs(dy))
                except:
                    diry = 0
                flipedSquares.append([legalMoves[k][1][0] + i * dirx, legalMoves[k][1][1] + i * diry])
                numberOfFlips+=1
        return numberOfFlips, flipedSquares

    def calculateMobility(self, player):
        return len(self.calculateLegalMoves(player))

    def calculateStableDiskCount(self, player):
        stableDisks = []
        # Stable disks cannot be calculated unless a piece has been placed in any of the corners
        for i in [[0, 0], [0, 1], [1, 0], [7, 0], [6, 0], [7, 1], [7, 7], [7, 6], [6, 7], [0, 6], [0, 7], [1, 7]]:
            if self.boardState[i[0]][i[1]].getOccupied() != "":
                flag = True
                break
        if flag:
            flipedSquares = []

            opponentMoves = self.calculateLegalMoves(1-player)
            for i in range(opponentMoves):
                numberOfFlips, flipedSquaresTemp = self.calculateFlipSquares(opponentMoves, i, 1 - player)
                flipedSquares.append(flipedSquaresTemp)
            for i in range(8):
                for j in range(8):
                    if self.boardState[i][j].getOccupied(player) == ["black", "white"][player]:
                        if [i, j] not in flipedSquares:
                            stableDisks.append([i, j])

        return len(stableDisks), stableDisks

    def calculateFrontierDiskCount(self, player):
        # More frontier disks means that you will probably lose
        frontierDisk = []
        for r in range(8):
            for c in range(8):
                if self.boardState[r][c].getOccupied() == ["black","white"][player]:
                    for k in [[0,1],[0,-1],[1,0],[-1,0],[-1,1],[-1,-1],[1,1],[1,-1]]:
                        row, col = r+k[0], c+k[1]
                        if (0<=row<=8) and (0<=col<=8) and (self.boardState[row][col].getOccupied() == ""):
                            frontierDisk.append([row, col])
        return len(frontierDisk), frontierDisk

    def calculateInteriorDiskCount(self, player):
        # More interior disks means higher chance of winning
        interiorDisk = []
        for r in range(8):
            for c in range(8):
                if self.boardState[r][c].getOccupied() == ["black", "white"][player]:
                    for k in [[0, 1], [0, -1], [1, 0], [-1, 0], [-1, 1], [-1, -1], [1, 1], [1, -1]]:
                        row, col = r + k[0], c + k[1]
                        if (0 <= row <= 8) and (0 <= col <= 8) and (self.boardState[row][col].getOccupied() == ["black", "white"][player]):
                            interiorDisk.append([row, col])
        return len(interiorDisk), interiorDisk





    def calculatePotentialMovesWeight(self, turn):
        return -math.log(turn + 1, self.potentialMovesWeightBase)

    def adjustPotentialMovesWeightBase(self, float):
        self.potentialMovesWeightBase = float






class Matrix:
    def __init__(self):
        self.matrix = []
        for i in range(8):
            self.matrix.append([])
            for j in range(8):
                self.matrix[i].append(0.0)

    def adjustWeight(self, row, col, weight):
        self.weightMatrix[row][col] = weight

    def evalutateBoard(self, legalMoves):
