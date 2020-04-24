# File: Reversi.py
# Written By: Chrisotpher Luey
# Date: 04/21/20

from Board import *
from Bot import *

def main():
    b = Board()
    boardState = b.getBoard()
    player = startGame(boardState, b)
    playing = True
    score = [0,0]

    while playing:
        bot = Bot(1-player)
        for i in range(2):
            b.setMessage("It is now " + ["black's", "white's"][i] + "turn.")
            if player == i:
                legalMoves = calculateLegalMoves(boardState, player)
                if not legalMoves: b.setMessage("There are no valid moves. The bot will now play.")
                else:
                    index = b.highlightSquares(legalMoves)
                    if index != -1:
                        boardState[legalMoves[index][0][0]][legalMoves[index][0][1]].setOccupied(["black", "white"][player])
                        calculateFlipSquares(boardState, legalMoves, index, player, score)
                    else:
                        playing = False
                        break
            else:
                legalMoves = calculateLegalMoves(boardState, 1-player)
                if not legalMoves:
                    b.setMessage("There are no valid moves. The player will now play.")
                else:
                    # index = bot.play(boardState, legalMoves)
                    # boardState[legalMoves[index][0][0]][legalMoves[index][0][1]].setOccupied(["black", "white"][player])
                    # calculateFlipSquares(legalMoves, index)
                    index = b.highlightSquares(legalMoves)
                    if index != -1:
                        boardState[legalMoves[index][0][0]][legalMoves[index][0][1]].setOccupied(
                            ["black", "white"][1-player])
                        calculateFlipSquares(boardState, legalMoves, index, 1-player, score)
                    else:
                        playing = False
                        break


            legalMoves.clear()


def startGame(boardState, b):
    boardState[3][3].setOccupied("white")
    boardState[4][4].setOccupied("white")
    boardState[4][3].setOccupied("black")
    boardState[3][4].setOccupied("black")
    return b.startGame()


def calculateLegalMoves(boardState, player):
    legalMoves = []
    for row in range(len(boardState)):
        for col in range(len(boardState[0])):
            adjacentSquares = []
            if boardState[row][col].getOccupied() == ["black", "white"][player]:
                for k in [-1, 1]:
                    if isWithinBoard(row+k, col+k, boardState) == ["black", "white"][1-player]: adjacentSquares.append(True)
                    else: adjacentSquares.append(False)
                for k in [-1, 1]:
                    if isWithinBoard(row, col+k, boardState) == ["black", "white"][1-player]: adjacentSquares.append(True)
                    else: adjacentSquares.append(False)
                for k in [-1, 1]:
                    if isWithinBoard(row+k, col, boardState) == ["black", "white"][1-player]: adjacentSquares.append(True)
                    else: adjacentSquares.append(False)

                factorList = [[-1,-1], [1,1], [0,-1], [0,1], [-1,0], [1,0]]
                for k in range(6):
                    if adjacentSquares[k] == True:
                        xFactor, yFactor = factorList[k][0], factorList[k][1]
                        while (1<=xFactor+row<=6) and (1<=yFactor+col<=6) and boardState[xFactor+row][yFactor+col].getOccupied() == ["black", "white"][1-player]:
                            try:
                                if boardState[row+xFactor+factorList[k][0]][col+yFactor+factorList[k][1]].getOccupied() == "":
                                    legalMoves.append([[row+xFactor+factorList[k][0], col+yFactor+factorList[k][1]], [row, col]])
                            except: break
                            xFactor, yFactor = xFactor+factorList[k][0], yFactor+factorList[k][1]
    print(legalMoves)
    return legalMoves


def calculateFlipSquares(boardState, legalMoves, index, player, score):
    dx, dy = legalMoves[index][0][0]-legalMoves[index][1][0], legalMoves[index][0][1]-legalMoves[index][1][1]
    for i in range(1, max(abs(dx), abs(dy))):
        try: dirx = int(dx/abs(dx))
        except: dirx = 0
        try: diry = int(dy/abs(dy))
        except: diry = 0
        boardState[legalMoves[index][1][0]+i*dirx][legalMoves[index][1][1]+i*diry].setOccupied(["black", "white"][player])
        score[player] = score[player]+1


def isWithinBoard(r, c, boardState):
    try: return boardState[r][c].getOccupied()
    except: return ""


main()
