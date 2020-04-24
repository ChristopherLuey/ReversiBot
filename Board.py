# File: Board.py
# Written By: Christopher Luey
# Date: 4/28/20
# Board class and Matrix class

from GUI import Tile

class Board:
    def __init__(self, boardState):
        self.weightMatrix = Matrix()
        self.boardState = boardState

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

        # self.stableDiskCountMaximium = self.calculatePossibleStableDisks()
        # self.interiorDiskCountMaximium = self.calculatePossibleInteriorDisks()
        # self.frontierDiskCountMaximium = self.calculatePossibleFrontierDisks()
        # self.potentialMobilityMaximium = self.calculatePossiblePotentialMobility()

        self.turn = 0

        # Corner, edges, buffer
        # Stable disks: cannot flip
        # Frontier vs interior disks: maximize interior disks

    def evaluateBoard(self, boardState):
        # val is if the board is good or not
        howGoodTheBoardIsBasedOnHowMuchWeWeightThings = 0

        val = self.stableDiskWeight * self.stableDiskCount / self.stableDiskCountMaximium
        return howGoodTheBoardIsBasedOnHowMuchWeWeightThings

    def updateBoard(self, boardState):
        self.boardState = boardState

    def getBoardState(self):
        return self.boardState

    def calculateLegalMoves(self, player):
        legalMoves = []
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
        return legalMoves

    def calculateFlipSquares(self, legalMoves, anchor, player):
        numberOfFlips = 0
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
                numberOfFlips+=1
        return numberOfFlips


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


    def calculateStableDiskCount(self):
        # Stable disks cannot be calculated unless a piece has been placed in any of the corners
        for i in [[0,0], [0,1], [1,0], [7,0],[6,0],[7,1],[7,7],[7,6],[6,7],[0,6],[0,7],[1,7]]:
            if self.boardState[i[0]][i[1]].getOccupied() != "":
                


class Matrix:
    def __init__(self):
        self.matrix = []
        for i in range(8):
            self.matrix.append([])
            for j in range(8):
                self.matrix[i].append(0.0)

    def adjustWeight(self, row, col, weight):
        self.weightMatrix[row][col] = weight
