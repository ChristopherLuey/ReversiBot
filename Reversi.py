# File: Reversi.py
# Written By: Chrisotpher Luey
# Date: 04/28/20
# Reversi runner

from GUI import *
from Board import *
from Bot import *

def main():
    bGUI = GUI()
    playing = True

    while playing:
        boardState = bGUI.getBoard()
        player = startGame(boardState, bGUI)
        score = [0, 0]
        turn = 0
        board = Board(boardState, turn, 0)
        board.setPlayer(1 - player)
        game = True
        while game:
            for i in range(2):
                board = Board(boardState, turn, i)
                bGUI.setMessage("It is now " + ["black's", "white's"][i] + "turn.")
                if player == i:
                    legalMoves = board.calculateLegalMoves(player)
                    print(legalMoves)

                    if not legalMoves: bGUI.setMessage("There are no valid moves. The bot will now play.")
                    else:
                        anchor = bGUI.highlightSquares(legalMoves)
                        if anchor:
                            boardState[legalMoves[anchor[0]][0][0]][legalMoves[anchor[0]][0][1]].setOccupied(["black", "white"][player])
                            board.calculateFlipSquares(legalMoves, anchor, player)
                            board.draw()
                        else:
                            playing = False
                            game = False
                            break
                else:
                    legalMoves = board.calculateLegalMoves(1-player)
                    print(legalMoves)
                    if not legalMoves:  bGUI.setMessage("There are no valid moves. The player will now play.")
                    else:

                        # call (current state of board, depth, -float inf, float inf, true)
                        bot = Bot(1 - player, boardState, turn)
                        decision, b, choice = bot.alphabeta(Board(boardState, turn, i), 2, -float("inf"), float("inf"), True)

                        print(decision, b, choice)

                        anchor = []
                        for index in range(len(legalMoves)):
                            if choice == legalMoves[index][0]:
                                anchor.append(index)

                        boardState[legalMoves[anchor[0]][0][0]][legalMoves[anchor[0]][0][1]].setOccupied(["black", "white"][1-player])
                        board.calculateFlipSquares(legalMoves, anchor, 1-player)
                        board.draw()


                board.calculateScore()
                board.incrementTurns()
                legalMoves.clear()
                turn+=1


def startGame(boardState, bGUI):
    boardState[3][3].setOccupied("white")
    boardState[4][4].setOccupied("white")
    boardState[4][3].setOccupied("black")
    boardState[3][4].setOccupied("black")
    for i in range(8):
        for j in range(8):
            boardState[i][j].drawPiece(boardState[i][j].getOccupied())
    return bGUI.startGame()


main()
