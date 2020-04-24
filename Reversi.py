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
    turn = 0
    while playing:
        #bot = Bot(1-player)

        for i in range(2):
            board = Board(boardState, turn, i)
            board.setPlayer(1-player)
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

                    # call (current state of board, depth, -float inf, float inf, true)
                    anchor = bGUI.highlightSquares(legalMoves)
                    if anchor != -1:
                        boardState[legalMoves[anchor[0]][0][0]][legalMoves[anchor[0]][0][1]].setOccupied(
                            ["black", "white"][1-player])
                        board.calculateFlipSquares(legalMoves, anchor, 1-player)
                    else:
                        playing = False
                        break

            board.calculateScore()
            board.incrementTurns()
            print(score)



            legalMoves.clear()
            turn+=1


def startGame(boardState, bGUI):
    boardState[3][3].setOccupied("white")
    boardState[4][4].setOccupied("white")
    boardState[4][3].setOccupied("black")
    boardState[3][4].setOccupied("black")
    return bGUI.startGame()


main()
