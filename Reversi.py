# File: Reversi.py
# Written By: Chrisotpher Luey
# Date: 04/21/20

from reversiBoard import *

def main():
    b = Board()
    bArr = b.getBoard()
    player = startGame(bArr, b)

    while True:
        if player == "black":
            print("lmao")

        elif player == "white":
            print("lmao")



def startGame(bArr, b):
    b.startGame()
    bArr[3][3].setOccupied("white")
    bArr[4][4].setOccupied("white")
    bArr[4][3].setOccupied("black")
    bArr[3][4].setOccupied("black")

    b.setMessage("Hello there my name is Kyler and I really like to mess things up because this is fun but right now I need a really long message to make sure that the text box works as expected. ily")

    pt = Point(-1,-1)

    while True:
    	pt = b.getClick()
    	bArr[pt[0]][pt[1]].highlight()


def calculateValidMoves(bArr, player):
    validMoves = []
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

                xFactor, yFactor = 0,0
                for k in range(8):
                    if adjacentSquares[k] == True:
                        while (0<=xFactor+row<=8) and (0<=yFactor+col<=8) and bArr[xFactor+row][yFactor+col].getOccupied() == ["black", "white"][1-player]
                            




def isWithinBoard(r, c, b):
    try: return b[r][c].getOccupied()
    except: return ""


main()
