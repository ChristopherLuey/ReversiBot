# File: Board.py
# Written By: Christopher Luey
# Date: 4/28/20
# Board class and Matrix class

import math
#import tensorflow as tf
import random
import copy


class Board:
    def __init__(self, boardState, turn, player):
        self.weightMatrix = Matrix()
        self.boardState = boardState
        self.turn = turn
        self.player = player
        self.playerLegacy = player

        # #Define Constants and Other Non-linear functions
        self.stableDiskWeight = -0.000382517*(self.turn)**2 + 0.00000975089*(self.turn)**3+0.0143841*(self.turn)
        if self.turn > 9:
            self.interiorDiskWeight = 0
        else:
            self.interiorDiskWeight = 0.000914589*(self.turn)**2 - 0.0456537*(self.turn) +0.790311 - 0.0000062274*(self.turn)**3
        self.frontierDiskWeight = -0.000229757*(self.turn)**2 - 0.0278324*(self.turn) + 0.916179 + 0.0000086104*(self.turn)**3

        # Overtime the number of tiles that the machine can flip becomes more valuable
        self.potentialMovesWeight = 0.00000842039*(self.turn)**3 - 0.0011153*(self.turn)**2 + 0.0271717*(self.turn) - 0.0317193

        self.flipWeight = -0.000021963*(self.turn)**3 +0.00223059*(self.turn)**2 - 0.0340902*(self.turn) - 0.0634103

        self.weightMatrixWeight = 1.0

        self.numberOfTilesWeight = 0.0000844407*(self.turn)**2 +0.0275302*(self.turn)-0.432643

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

        self.weightAdjustment = 0.0


    def evaluateBoard(self):
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

        maxInterior = (self.interiorDiskCount+self.opponentInteriorDiskCount)
        if (self.interiorDiskCount+self.opponentInteriorDiskCount) == 0: maxInterior = 1

        maxFrontier = (self.frontierDiskCount+self.opponentFrontierDiskCount)
        if (self.frontierDiskCount+self.opponentFrontierDiskCount) == 0: maxFrontier = 1

        maxTiles = (self.numberOfTiles+self.opponentNumberOfTiles)
        if (self.numberOfTiles+self.opponentNumberOfTiles) == 0: maxTiles = 1

        self.stableDiskConstant = (self.stableDiskCount-self.opponentStableDiskCount) / maxStableDisk
        self.interiorDiskConstant = (self.interiorDiskCount-self.opponentInteriorDiskCount)/maxInterior
        self.frontierDiskConstant = (self.frontierDiskCount-self.opponentFrontierDiskCount)/maxFrontier
        self.potentialMobilityConstant = (self.potentialMobility-self.opponentPotentialMobility)/maxMobility
        self.potentialFlipsConstant = (self.potentialFlips-self.opponentPotentialFlips)/maxFlip
        self.numberOfTilesConstant = (self.numberOfTiles-self.opponentNumberOfTiles)/maxTiles


        self.stableDiskScore = self.stableDiskWeight*(self.stableDiskCount-self.opponentStableDiskCount) / maxStableDisk

        self.interiorDiskScore = self.interiorDiskWeight*(self.interiorDiskCount-self.opponentInteriorDiskCount)/maxInterior

        self.frontierDiskScore = self.frontierDiskWeight*(self.frontierDiskCount-self.opponentFrontierDiskCount)/maxFrontier

        self.potentialMobilityScore = self.potentialMovesWeight*(self.potentialMobility-self.opponentPotentialMobility)/maxMobility

        self.potentialFlipsScore = self.flipWeight*(self.potentialFlips-self.opponentPotentialFlips)/maxFlip

        self.numberOfTilesScore = self.numberOfTilesWeight*(self.numberOfTiles-self.opponentNumberOfTiles)/maxTiles

        matrixScore, opponentMatrixScore = self.weightMatrix.calculateMatrix(self.boardState, self.player)
        self.matrixConstant = (matrixScore-opponentMatrixScore)

        utility = self.stableDiskScore + self.interiorDiskScore + self.frontierDiskScore + self.potentialMobilityScore + self.potentialFlipsScore + self.numberOfTilesScore +self.weightMatrixWeight*(matrixScore-opponentMatrixScore)

        if self.playerLegacy == self.player:
            return utility
        else:
            return -utility


    def getConstants(self):
        x = [self.stableDiskConstant, self.interiorDiskConstant, self.frontierDiskConstant, self.potentialMobilityConstant, self.potentialFlipsConstant, self.numberOfTilesConstant, self.matrixConstant]
        return x

    def defineWeights(self, weights):
        # Solely for training
        self.stableDiskWeight = weights[0]
        self.interiorDiskWeight = weights[1]
        self.frontierDiskWeight = weights[2]
        self.flipWeight = weights[3]
        self.potentialMovesWeight = weights[4]
        self.numberOfTilesWeight = weights[5]
        self.weightMatrixWeight = weights[6]


    def getTurn(self):
        return self.turn

    def getPlayerLegacy(self):
        return self.playerLegacy

    def getPlayer(self):
        return self.player

    def updateBoard(self, boardState):
        self.boardState = boardState

    def getBoardState(self):
        return self.boardState

    def incrementTurn(self):
        self.turn+=1

    def calculateLegalMoves(self, player):
        legalMoves = []
        for row in range(len(self.boardState)):
            for col in range(len(self.boardState[0])):
                adjacentSquares = []
                if self.boardState[row][col] == ["black", "white"][player]:
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
                            while (0 <= xFactor + row <= 7) and (0 <= yFactor + col <= 7) and self.boardState[xFactor + row][yFactor + col] == ["black", "white"][1 - player]:
                                try:
                                    if (0 <= xFactor + row + factorList[k][0] <= 7) and (0 <= yFactor + col + factorList[k][1] <= 7) and self.boardState[row + xFactor + factorList[k][0]][col + yFactor + factorList[k][1]] == "":
                                        legalMoves.append([[row + xFactor + factorList[k][0], col + yFactor + factorList[k][1]], [row, col]])
                                except:
                                    break
                                xFactor, yFactor = xFactor + factorList[k][0], yFactor + factorList[k][1]
        return legalMoves

    def setPlayer(self, player):
        self.playerLegacy = player
        print(self.playerLegacy)

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
                self.boardState[legalMoves[k][1][0] + i * dirx][legalMoves[k][1][1] + i * diry] = ["black", "white"][player]
                flipedSquares.append([legalMoves[k][1][0] + i * dirx, legalMoves[k][1][1] + i * diry])
                numberOfFlips+=1
        return numberOfFlips, flipedSquares

    def isWithinBoard(self, r, c):
        try:
            return self.boardState[r][c]
        except:
            return ""

    def calculateScore(self):
        score = [0,0]
        for i in range(8):
            for j in range(8):
                if self.boardState[i][j] == "white":
                    score[1] = score[1] + 1
                elif self.boardState[i][j] == "black":
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
            if self.boardState[i[0]][i[1]] != "":
                flag = True
                break
        if flag:
            flipedSquares = []

            opponentMoves = self.calculateLegalMoves(1-player)
            for i in range(len(opponentMoves)):
                numberOfFlips, flipedSquaresTemp = self.calculateFlipTilesPotential(1-player)
                flipedSquares.append(flipedSquaresTemp)
            for i in range(8):
                for j in range(8):
                    if self.boardState[i][j] == ["black", "white"][player]:
                        if [i, j] not in flipedSquares:
                            stableDisks.append([i, j])

        return len(stableDisks), stableDisks

    def calculateFrontierDiskCount(self, player):
        # More frontier disks means that you will probably lose
        frontierDisk = []
        for r in range(8):
            for c in range(8):
                if self.boardState[r][c] == ["black","white"][player]:
                    for k in [[0,1],[0,-1],[1,0],[-1,0],[-1,1],[-1,-1],[1,1],[1,-1]]:
                        row, col = r+k[0], c+k[1]
                        if (1<=row<=6) and (1<=col<=6) and (self.boardState[row][col] == ""):
                            frontierDisk.append([row, col])
                            break
        return len(frontierDisk), frontierDisk


    def calculateInteriorDiskCount(self, player):
        # More interior disks means higher chance of winning
        interiorDisk = []
        for r in range(8):
            for c in range(8):
                if self.boardState[r][c] == ["black", "white"][player]:
                    flag = True
                    for k in [[0, 1], [0, -1], [1, 0], [-1, 0], [-1, 1], [-1, -1], [1, 1], [1, -1]]:
                        row, col = r + k[0], c + k[1]
                        if (1 <= row <= 6) and (1 <= col <= 6) and not (self.boardState[row][col] == ["black", "white"][player]):
                            flag = False
                    if flag: interiorDisk.append([row, col])
        return len(interiorDisk), interiorDisk


    def calculatePotentialMovesWeight(self, turn):
        return -math.log(turn + 1, self.potentialMovesWeightBase)


    def adjustPotentialMovesWeightBase(self, float):
        self.potentialMovesWeightBase = float

    def draw(self):
        for i in range(8):
            for j in range(8):
                self.boardState[i][j].drawPiece(self.boardState[i][j])

    def getBoard(self):
        return self.boardState

    def setBoard(self, boardState):
        self.boardState = boardState

    def printBoard(self):
        for i in range(8):
            for j in range(8):
                if self.boardState[j][i] == "":
                    print("xxxxx", end=" ")
                else:
                    print(self.boardState[j][i], end=" ")
            print()
        print()

    def move(self, legalMoves, anchor, player):
        self.boardState[legalMoves[anchor[0]][0][0]][legalMoves[anchor[0]][0][1]] = ["black", "white"][player]


class Matrix:
    def __init__(self):
        self.matrix = [ [10.0, -4.0, 3.0, 4.0, 4.0, 3.0, -4.0, 10.0],
                        [-4.0, -5.0, -1.0, -1.0, -1.0, -1.0, -5.0, -4.0],
                        [2.0, -1.0, 1.0, 0.2, 0.2, 1.0, -1.0, 2.0],
                        [2.0, -1.0, 0.2, 1.0, 1.0, 0.2, -1.0, 2.0],
                        [2.0, -1.0, 0.2, 1.0, 1.0, 0.2, -1.0, 2.0],
                        [2.0, -1.0, 1.0, 0.2, 0.2, 1.0, -1.0, 2.0],
                        [-4.0, -5.0, -1.0, -1.0, -1.0, -1.0, -5.0, -4.0],
                        [10.0, -4.0, 3.0, 4.0, 4.0, 3.0, -4.0, 10.0]]

    def calculateMatrix(self, boardState, player):
        p1, p2, total = 0.0,0.0, 0.0
        for i in range(len(boardState)):
            for j in range(len(boardState[0])):
                if boardState[i][j] == ["black", "white"][player]:
                    p1+=self.matrix[i][j]
                if boardState[i][j] == ["white", "black"][player]:
                    p2-=self.matrix[i][j]
                total+=self.matrix[i][j]
        print(p1/total, p2/total)
        return p1/total, p2/total


    def adjustWeight(self, row, col, weight):
        # For training
        self.matrix[row][col] = weight


    def getMatrix(self):
        return self.matrix
