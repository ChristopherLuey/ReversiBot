# File: Reversi.py
# Written By: Chrisotpher Luey
# Date: 04/21/20

from reversiBoard import *

def main():
    b = Board()
    bArr = b.getBoard()
    player = startGame(bArr, b)

    while True:
        if player == 0:
            validMoves, centerData = calculateValidMoves(bArr, 0)
            if not validMoves: b.setMessage("There are no valid moves. The bot will now play.")
            else:
                playedSquare = b.highlightSquares(validMoves)
                bArr[playedSquare[0]][playedSquare[1]].setOccupied(["black", "white"][player])
                calculateFlipSquares(playedSquare, centerData)


        else:
            print("lmao")



def startGame(bArr, b):
    b.startGame()
    bArr[3][3].setOccupied("white")
    bArr[4][4].setOccupied("white")
    bArr[4][3].setOccupied("black")
    bArr[3][4].setOccupied("black")


def calculateValidMoves(bArr, player):
    validMoves, centerData = [], []
    for row in bArr:
        for col in bArr[0]:
            adjacentSquares = []
            if bArr[row][col].getOccupied() == ["black", "white"][player]:
                for k in [-1, 1]:
                    if isWithinBoard(row+k, col+k, bArr) == ["black", "white"][1-player]: adjacentSquares.append(True)
                    else: adjacentSquares.append(False)
                for k in [-1, 1]:
                    if isWithinBoard(row, col+k, bArr) == ["black", "white"][1-player]: adjacentSquares.append(True)
                    else: adjacentSquares.append(False)
                for k in [-1, 1]:
                    if isWithinBoard(row+k, col, bArr) == ["black", "white"][1-player]: adjacentSquares.append(True)
                    else: adjacentSquares.append(False)

                factorList = 0, 0, [[-1,-1], [1,1], [0,-1], [0,1], [-1,0], [1,0]]
                for k in range(8):
                    if adjacentSquares[k] == True:
                        xFactor, yFactor = factorList[k][0], factorList[k][1]
                        while (0<=xFactor+row<=8) and (0<=yFactor+col<=8) and bArr[xFactor+row][yFactor+col].getOccupied() == ["black", "white"][1-player]:
                            try:
                                if bArr[row+xFactor+factorList[k][0]][col+yFactor+factorList[k][1]].getOccupied() == "":
                                    validMoves.append([row+xFactor+factorList[k][0], col+yFactor+factorList[k][1]])
                                    centerData.append(row, col)
                            except: break
                            xFactor, yFactor = xFactor+factorList[k][0], yFactor+factorList[k][1]
    return validMoves, centerData


def calculateFlipSquares(bArr, square):
    for


def isWithinBoard(r, c, b):
    try: return b[r][c].getOccupied()
    except: return ""


main()
