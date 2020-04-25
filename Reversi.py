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
        while turn<64:
            for i in range(2):
                board = Board(boardState, turn, i)
                bGUI.setMessage("It is now " + ["black's", "white's"][i] + "turn.")
                if player == i:
                    legalMoves = board.calculateLegalMoves(player)
                    print(legalMoves)

                    if not legalMoves:
                        bGUI.setMessage("There are no valid moves. The bot will now play.")
                    else:
                        anchor = bGUI.highlightSquares(legalMoves)
                        if anchor:
                            boardState[legalMoves[anchor[0]][0][0]][legalMoves[anchor[0]][0][1]] = ["black", "white"][player]
                            board.calculateFlipSquares(legalMoves, anchor, player)
                            bGUI.draw(boardState)
                        else:
                            playing = False
                            game = False
                            break
                else:
                    legalMoves = board.calculateLegalMoves(1-player)
                    print(legalMoves)
                    if not legalMoves:
                        bGUI.setMessage("There are no valid moves. The player will now play.")

                    else:

                        # call (current state of board, depth, -float inf, float inf, true)
                        tempboard = boardState[:]

                        bot = Bot(1 - player)

                        b = Board(tempboard, turn, i)

                        decision, board2, choice = bot.alphabeta(b, 1, -float("inf"), float("inf"), True)

                        print(decision, board2, choice)
                        b.printBoard()
                        board.printBoard()
                        anchor = []
                        for index in range(len(legalMoves)):
                            if choice == legalMoves[index][0]:
                                anchor.append(index)
                        print(legalMoves, anchor)
                        board.move(legalMoves, anchor, 1-player)
                        board.calculateFlipSquares(legalMoves, anchor, 1-player)
                        bGUI.draw(boardState)



                board.calculateScore()
                board.incrementTurns()
                legalMoves.clear()
                turn+=1


def startGame(boardState, bGUI):
    boardState[3][3]= "white"
    boardState[4][4] = "white"
    boardState[4][3] = "black"
    boardState[3][4] = "black"
    bGUI.draw(boardState)
    return bGUI.startGame()


main()
