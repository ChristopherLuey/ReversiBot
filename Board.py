# File: Board.py
# Written By: Christopher Luey
# Date: 4/28/20
# Board class and Matrix class

from GUI import Tile
import math
import copy

class Board:
    def __init__(self, boardState, turn, player):
        self.weightMatrix = Matrix()
        self.boardState = boardState
        self.turn = turn
        self.player = player
        self.playerLegacy = player

        # Define Constants and Other Non-linear functions
        self.stableDiskWeight = 1.0
        self.interiorDiskWeight = 1.0
        self.frontierDiskWeight = 1.0
        # Overtime the number of tiles that the machine can flip becomes more valuable
        self.flipWeightPower = 1.002
        self.flipWeight = turn**self.flipWeightPower
        self.weightMatrixWeight = 1.0
        # Overtime potential moves becomes less valuable
        self.potentialMovesWeightBase = 1.2
        self.potentialMovesWeight = self.calculatePotentialMovesWeight(self.turn)
        self.numberOfTilesWeight = 1.0

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

        self.turn = 0

        # Corner, edges, buffer
        # Stable disks: cannot flip
        # Frontier vs interior disks: maximize interior disks

    def evaluateBoard(self):
        # val is if the board is good or not

        self.stableDiskCount = self.calculateStableDiskCount(self.player)[0]
        self.interiorDiskCount = self.calculateInteriorDiskCount(self.player)[0]
        self.frontierDiskCount = self.calculateFrontierDiskCount(self.player)[0]
        self.potentialMobility = self.calculateMobility(self.player)
        self.potentialFlips = self.calculateFlipTilesPotential(self.player)[0]
        self.numberOfTiles = self.calculateNumberOfTiles(self.player)


        self.opponentStableDiskCount = self.calculateStableDiskCount(1-self.player)[0]
        self.opponentInteriorDiskCount = self.calculateInteriorDiskCount(1-self.player)[0]
        self.opponentFrontierDiskCount = self.calculateFrontierDiskCount(1-self.player)[0]
        self.opponentPotentialMobility = self.calculateMobility(1-self.player)
        self.opponentPotentialFlips = self.calculateFlipTilesPotential(1-self.player)[0]
        self.opponentNumberOfTiles = self.calculateNumberOfTiles(1-self.player)

        maxStableDisk = (self.stableDiskCount + self.opponentStableDiskCount)
        if (self.stableDiskCount + self.opponentStableDiskCount) == 0: maxStableDisk = 1

        maxMobility = (self.potentialMobility+self.opponentPotentialMobility)
        if (self.potentialMobility+self.opponentPotentialMobility) == 0: maxMobility = 1

        maxFlip = (self.potentialFlips+self.opponentPotentialFlips)
        if (self.potentialFlips+self.opponentPotentialFlips) == 0: maxFlip = 1


        self.stableDiskScore = self.stableDiskWeight*(self.stableDiskCount-self.opponentStableDiskCount) / maxStableDisk

        self.interiorDiskScore = self.interiorDiskWeight*(self.interiorDiskCount-self.opponentInteriorDiskCount)/(self.interiorDiskCount+self.opponentInteriorDiskCount)

        self.frontierDiskScore = self.frontierDiskWeight*(self.frontierDiskCount-self.opponentFrontierDiskCount)/(self.frontierDiskCount+self.opponentFrontierDiskCount)

        self.potentialMobilityScore = self.potentialMovesWeight*(self.potentialMobility-self.opponentPotentialMobility)/maxMobility

        self.potentialFlipsScore = self.flipWeight*(self.potentialFlips-self.opponentPotentialFlips)/maxFlip

        self.numberOfTilesScore = self.numberOfTilesWeight*(self.numberOfTiles-self.opponentNumberOfTiles)/(self.numberOfTiles+self.opponentNumberOfTiles)

        matrixScore, opponentMatrixScore = self.weightMatrix.calculateMatrix(self.boardState, self.player)

        utility = self.stableDiskScore + self.interiorDiskScore + self.frontierDiskScore + self.potentialMobilityScore + self.potentialFlipsScore + self.numberOfTilesScore + matrixScore-opponentMatrixScore

        if self.playerLegacy == self.player: return utility
        else: return -utility


    def copy(self):
        # Make a copy after changing to board state
        boardState = []
        for i in range(8):
            boardState.append([])
            for j in range(8):
                boardState[i].append(self.boardState[i][j])

        b = Board(boardState, self.turn, 1-self.player)
        b.setPlayer(self.playerLegacy)
        return b


    def getPlayer(self):
        return self.player

    def incrementTurns(self):
        self.turn+=1

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
                            while (1 <= xFactor + row <= 6) and (1 <= yFactor + col <= 6) and self.boardState[xFactor + row][yFactor + col].getOccupied() == ["black", "white"][1 - player]:
                                try:
                                    if self.boardState[row + xFactor + factorList[k][0]][col + yFactor + factorList[k][1]].getOccupied() == "":
                                        self.legalMoves.append([[row + xFactor + factorList[k][0], col + yFactor + factorList[k][1]], [row, col]])
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
        flag = False
        for i in [[0, 0], [0, 1], [1, 0], [7, 0], [6, 0], [7, 1], [7, 7], [7, 6], [6, 7], [0, 6], [0, 7], [1, 7]]:
            if self.boardState[i[0]][i[1]].getOccupied() != "":
                flag = True
                break
        if flag:
            flipedSquares = []

            opponentMoves = self.calculateLegalMoves(1-player)
            for i in range(opponentMoves):
                numberOfFlips, flipedSquaresTemp = self.calculateFlipSquares(opponentMoves, i, 1-player)
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

    def draw(self):
        for i in range(8):
            for j in range(8):
                self.boardState[i][j].drawPiece(self.boardState[i][j].getOccupied())


class Matrix:
    def __init__(self):
        self.matrix = [[0.9, -0.9, 0.3, 0.5, 0.5, 0.3, -0.9, 0.9],
                        [-0.9, -0.9, 0.3, 0.5, 0.5, 0.3, -0.9, -0.9],
                        [0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3],
                        [0.5, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.5],
                        [0.5, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.5],
                        [0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3],
                        [-0.9, -0.9, 0.3, 0.5, 0.5, 0.3, -0.9, -0.9],
                        [0.9, -0.9, 0.3, 0.5, 0.5, 0.3, -0.9, 0.9]]
        # for i in range(8):
        #     self.matrix.append([])
        #     for j in range(8):
        #         self.matrix[i].append(0.0)
    def calculateMatrix(self, boardState, player):
        p1, p2 = 0.0,0.0
        for i in range(len(boardState)):
            for j in range(len(boardState[0])):
                if boardState[i][j].getOccupied() == ["black", "white"][player]:
                    p1+=self.matrix[i][j]
                elif boardState[i][j].getOccupied() == ["white", "black"][player]:
                    p2+=self.matrix[i][j]
        return p1, p2

    def adjustWeight(self, row, col, weight):
        self.weightMatrix[row][col] = weight
