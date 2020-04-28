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
        print(self.matrixConstant, self.playerLegacy, self.player)
        if self.playerLegacy == self.player:
            pass
        else:
            #self.matrixConstant = -self.matrixConstant
            pass

        # print((self.stableDiskCount-self.opponentStableDiskCount) / maxStableDisk)
        # print((self.interiorDiskCount-self.opponentInteriorDiskCount)/maxInterior)
        # print((self.frontierDiskCount-self.opponentFrontierDiskCount)/maxFrontier)
        # print((self.potentialMobility-self.opponentPotentialMobility)/maxMobility)
        # print((self.potentialFlips-self.opponentPotentialFlips)/maxFlip)
        # print((self.numberOfTiles-self.opponentNumberOfTiles)/maxTiles)
        #print(self.stableDiskScore, self.interiorDiskScore, self.frontierDiskScore, self.potentialMobilityScore, self.potentialFlipsScore, self.numberOfTilesScore, matrixScore, opponentMatrixScore)
        #print(self.stableDiskWeight, self.interiorDiskWeight, self.frontierDiskWeight, self.potentialMovesWeight, self.flipWeight, self.numberOfTilesWeight, self.weightMatrixWeight)
        # print("Turn: "+ str(self.turn))

        utility = self.stableDiskScore + self.interiorDiskScore + self.frontierDiskScore + self.potentialMobilityScore + self.potentialFlipsScore + self.numberOfTilesScore +self.weightMatrixWeight*(matrixScore-opponentMatrixScore)
        # c = copy.deepcopy(self.boardState)
        # for i in range(8):
        #     for j in range(8):
        #         if c[i][j] == "white":
        #             c[i][j] = 1
        #         elif c[i][j] == "black":
        #             c[i][j] = -1
        #         else:
        #             c[i][j] = 0
        # model = tf.keras.models.load_model('model.h5')
        # arr = model.predict([c])
        # print(arr)
        if self.playerLegacy == self.player:
            return utility
        else:
            return -utility

        if self.playerLegacy == self.player:
            if self.player == 0:
            #return -random.random()
            #print("Utility: " + str(-utility))
                #return -utility
                return -arr[0][0]
            else:
                return -arr[0][1]

        else:
            #print("Utility: "+str(utility))
            #return utility
            #return random.random()
            if self.player == 0:
            #return -random.random()
            #print("Utility: " + str(-utility))
                #return -utility
                return arr[0][0]
            else:
                return arr[0][1]

    # def learn(self, expected):
    #     w1*const + w2*const + w3*const = utility
    #     c1x + c2y + c3z + c4w + c5p = utility

    def getConstants(self):
        #print([self.stableDiskConstant, self.interiorDiskConstant, self.frontierDiskConstant, self.potentialMobilityConstant, self.potentialFlipsConstant, self.numberOfTilesConstant, self.matrixConstant])
        x = [self.stableDiskConstant, self.interiorDiskConstant, self.frontierDiskConstant, self.potentialMobilityConstant, self.potentialFlipsConstant, self.numberOfTilesConstant, self.matrixConstant]
        return x

    def defineWeights(self, weights):
        # Define Constants and Other Non-linear functions

        # self.stableDiskWeightBase = weights[0]
        # self.stableDiskWeightCoefficient = weights[1]
        # self.stableDiskWeightShift = weights[2]
        # self.stableDiskWeightCoefficient2 = weights[3]
        # self.stableDiskWeightShiftUp = weights[4]
        #
        # self.stableDiskWeight = self.stableDiskWeightCoefficient * math.log(
        #     ((self.turn+1) / 64 + abs(self.stableDiskWeightShift)) * abs(self.stableDiskWeightCoefficient2), abs(self.stableDiskWeightBase)) +self.stableDiskWeightShiftUp
        #
        # self.interiorDiskWeightBase = weights[5]
        # self.interiorDiskWeightCoefficient = weights[6]
        # self.interiorDiskWeightShift = weights[7]
        # self.interiorDiskWeightCoefficient2 = weights[8]
        # self.interiorDiskWeightShiftUp = weights[9]
        # self.interiorDiskWeight = self.interiorDiskWeightCoefficient * math.log(
        #     ((self.turn + 1) / 64 + abs(self.interiorDiskWeightShift)) * abs(self.interiorDiskWeightCoefficient2),
        #     abs(self.interiorDiskWeightBase)) + self.interiorDiskWeightShiftUp
        #
        # self.frontierDiskWeightBase = weights[10]
        # self.frontierDiskWeightCoefficient = weights[11]
        # self.frontierDiskWeightShift = weights[12]
        # self.frontierDiskWeightCoefficient2 = weights[13]
        # self.frontierDiskWeightShiftUp = weights[14]
        #
        # self.frontierDiskWeight = self.frontierDiskWeightCoefficient * math.log(
        #     ((self.turn + 1) / 64 + abs(self.frontierDiskWeightShift)) * abs(self.frontierDiskWeightCoefficient2),
        #     abs(self.frontierDiskWeightBase)) + self.frontierDiskWeightShiftUp
        #
        # # Overtime the number of tiles that the machine can flip becomes more valuable
        # self.flipWeightBase = weights[15]
        # self.flipWeightCoefficient = weights[16]
        # self.flipWeightShift = weights[17]
        # self.flipWeightCoefficient2 = weights[18]
        # self.flipWeightShiftUp = weights[19]
        # self.flipWeight = self.flipWeightCoefficient * math.log(
        #     ((self.turn + 1) / 64 + abs(self.flipWeightShift)) * abs(self.flipWeightCoefficient2),
        #     abs(self.flipWeightBase)) + self.flipWeightShiftUp
        #
        # self.potentialMovesWeightBase = weights[20]
        # self.potentialMovesWeightCoefficient = weights[21]
        # self.potentialMovesWeightShift = weights[22]
        # self.potentialMovesWeightCoefficient2 = weights[23]
        # self.potentialMovesWeightShiftUp = weights[24]
        # self.potentialMovesWeight = self.potentialMovesWeightCoefficient * math.log(
        #     ((self.turn + 1) / 64 + abs(self.potentialMovesWeightShift)) * abs(self.potentialMovesWeightCoefficient2),
        #     abs(self.potentialMovesWeightBase)) + self.potentialMovesWeightShiftUp
        #
        # self.numberOfTilesWeightBase = weights[25]
        # self.numberOfTilesWeightCoefficient = weights[26]
        # self.numberOfTilesWeightShift = weights[27]
        # self.numberOfTilesWeightCoefficient2 = weights[28]
        # self.numberOfTilesWeightShiftUp = weights[29]
        # self.numberOfTilesWeight = self.numberOfTilesWeightCoefficient * math.log(
        #     ((self.turn + 1) / 64 + abs(self.numberOfTilesWeightShift)) * abs(self.numberOfTilesWeightCoefficient2),
        #     abs(self.numberOfTilesWeightBase)) + self.numberOfTilesWeightShiftUp
        #
        # self.weightMatrixWeight = weights[30]
        self.stableDiskWeight = weights[0]
        self.interiorDiskWeight = weights[1]
        self.frontierDiskWeight = weights[2]
        self.flipWeight = weights[3]
        self.potentialMovesWeight = weights[4]
        self.numberOfTilesWeight = weights[5]
        self.weightMatrixWeight = weights[6]




    def eval(self, model):
        c = copy.deepcopy(self.boardState)
        for i in range(8):
            for j in range(8):
                if c[i][j] == "white":
                    c[i][j] = 1
                elif c[i][j] == "black":
                    c[i][j] = -1
                else:
                    c[i][j] = 0
        arr = model.predict([c])
        for i in arr[0]:
            i = float(i)
        print(arr)

        if arr[0][0] > arr[0][1]:
            print("black win")
        else:
            print('white win')

        if self.playerLegacy == self.player:
            if self.player == 0:
                # return -random.random()
                # print("Utility: " + str(-utility))
                # return -utility
                return -arr[0][0]
            else:
                return -arr[0][1]

        else:
            # print("Utility: "+str(utility))
            # return utility
            # return random.random()
            if self.player == 0:
                # return -random.random()
                # print("Utility: " + str(-utility))
                # return -utility
                return arr[0][0]
            else:
                return arr[0][1]



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
        # for i in range(8):
        #     self.matrix.append([])
        #     for j in range(8):
        #         self.matrix[i].append(0.0)
    def calculateMatrix(self, boardState, player):

        # if boardState[0][0] == ["black", "white"][player]:
        #     self.matrix[0][1] = 2.0
        #     self.matrix[1][0] = 2.0
        #     self.matrix[1][1] = 2.0
        # elif boardState[0][0] == ["black", "white"][1-player]:
        #     self.matrix[0][1] = -2.0
        #     self.matrix[1][0] = -2.0
        #     self.matrix[1][1] = -2.0
        #
        # if boardState[0][7] == ["black", "white"][player]:
        #     self.matrix[0][6] = 2.0
        #     self.matrix[1][7] = 2.0
        #     self.matrix[1][6] = 2.0
        # elif boardState[0][7] == ["black", "white"][1-player]:
        #     self.matrix[0][6] = -2.0
        #     self.matrix[1][7] = -2.0
        #     self.matrix[1][6] = -2.0
        # if boardState[7][7] == ["black", "white"][player]:
        #     self.matrix[6][6] = 2.0
        #     self.matrix[6][7] = 2.0
        #     self.matrix[7][6] = 2.0
        # elif boardState[7][7] == ["black", "white"][1-player]:
        #     self.matrix[6][6] = -2.0
        #     self.matrix[6][7] = -2.0
        #     self.matrix[7][6] = -2.0
        #
        # if boardState[0][7] == ["black", "white"][player]:
        #     self.matrix[0][6] = 2.0
        #     self.matrix[1][7] = 2.0
        #     self.matrix[1][6] = 2.0
        # elif boardState[7][7] != ["black", "white"][1-player]:
        #     self.matrix[6][6] = -2.0
        #     self.matrix[6][7] = -2.0
        #     self.matrix[7][6] = -2.0


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
        self.weightMatrix[row][col] = weight


    def getMatrix(self):
        return self.matrix
