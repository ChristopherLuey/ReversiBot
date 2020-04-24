# File: Reversi.py
# Written By: Chrisotpher Luey
# Date: 04/28/20
# Reversi runner

from GUI import *
from Board import *

def main():
    bGUI = GUI()
    boardState = bGUI.getBoard()
    player = startGame(boardState, bGUI)
    playing = True
    score = [0,0]
    while playing:
        board = Board(boardState)
        #bot = Bot(1-player)
        for i in range(2):
            bGUI.setMessage("It is now " + ["black's", "white's"][i] + "turn.")
            if player == i:
                legalMoves = board.calculateLegalMoves(player)
                if not legalMoves: bGUI.setMessage("There are no valid moves. The bot will now play.")
                else:
                    anchor = bGUI.highlightSquares(legalMoves)
                    if anchor != -1:
                        boardState[legalMoves[anchor[0]][0][0]][legalMoves[anchor[0]][0][1]].setOccupied(["black", "white"][player])
                        board.calculateFlipSquares(legalMoves, anchor, player)
                    else:
                        playing = False
                        break
            else:
                legalMoves = board.calculateLegalMoves(1-player)
                if not legalMoves:
                    bGUI.setMessage("There are no valid moves. The player will now play.")
                else:
                    anchor = bGUI.highlightSquares(legalMoves)
                    if anchor != -1:
                        boardState[legalMoves[anchor[0]][0][0]][legalMoves[anchor[0]][0][1]].setOccupied(
                            ["black", "white"][1-player])
                        board.calculateFlipSquares(legalMoves, anchor, 1-player)
                    else:
                        playing = False
                        break
            calculateScore(board, score)
            print(score)

            legalMoves.clear()


def startGame(boardState, bGUI):
    boardState[3][3].setOccupied("white")
    boardState[4][4].setOccupied("white")
    boardState[4][3].setOccupied("black")
    boardState[3][4].setOccupied("black")
    return bGUI.startGame()


def calculateScore(board, score):
    boardState = board.getBoardState()
    score.clear()
    score.append(0)
    score.append(0)
    for i in range(len(boardState)):
        for j in range(len(boardState[0])):
            if boardState[i][j].getOccupied() == "white": score[1] = score[1]+1
            elif boardState[i][j].getOccupied() == "black": score[0] = score[0]+1


main()
