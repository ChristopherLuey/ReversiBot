# File: Reversi.py
# Written By: Chrisotpher Luey
# Date: 04/28/20
# Reversi runner

from GUI import *
from Board import *
from Bot import *

def main():
    # Create GUI
    bGUI = GUI()
    playing = True

    while playing:
        # Gather board array
        score = [0,0]
        boardState = bGUI.getBoard()
        # Determine who the human player is
        player, turn = startGame(boardState, bGUI), 0

        # Play the game until the game is over
        while (score[0]+score[1]) != 64:
            for i in range(2):
                # Initialize new board
                board = Board(boardState, turn, i)
                board.setPlayer(i)
                bGUI.setMessage2("It is now " + ["black's", "white's"][i] + " turn.")

                # Check whether it is the human player's turn
                if player == i:
                    legalMoves = board.calculateLegalMoves(player)
                    if not legalMoves: bGUI.setMessage2("There are no valid moves. The bot will now play.")
                    else:
                        # Gather a list of the square that was played, and the squares that need to be flipped
                        anchor = bGUI.highlightSquares(legalMoves, True)
                        if anchor != -1:
                            # Add the played square to the 2d board array
                            boardState[legalMoves[anchor[0]][0][0]][legalMoves[anchor[0]][0][1]] = ["black", "white"][player]
                            board.calculateFlipSquares(legalMoves, anchor, player)
                            bGUI.draw(boardState)
                            bGUI.setMessage("Player has played " + str(legalMoves[anchor[0]][0][0] + 1) + ", " + str(legalMoves[anchor[0]][0][1] + 1))

                        else:
                            playing, turn = False, 65
                            break

                else:
                    # Calculate legal moves
                    legalMoves = board.calculateLegalMoves(1-player)
                    if not legalMoves: bGUI.setMessage2("There are no valid moves. The player will now play.")
                    else:
                        # Create a bot
                        bot = Bot(1 - player)
                        # Create a board to give to the bot
                        b = Board(copy.deepcopy(boardState), turn, 1-player)
                        b.setPlayer(1-player)
                        bGUI.highlightSquares(legalMoves, False)
                        # Gather bot decision
                        decision, board2, choice = bot.alphabeta(b, 4, -float("inf"), float("inf"), True)

                        # Use this to determine which squares to flip
                        anchor = []
                        for index in range(len(legalMoves)):
                            if choice == legalMoves[index][0]: anchor.append(index)
                        board.move(legalMoves, anchor, 1-player)
                        board.calculateFlipSquares(legalMoves, anchor, 1-player)
                        bGUI.unhighlightSquares(legalMoves)
                        bGUI.draw(boardState)
                        bGUI.setMessage("AI has played " + str(choice[0]+1) + ", " + str(choice[1]+1))

                board.incrementTurn()
                score=board.calculateScore()
                legalMoves.clear()
                turn+=1
        if playing:
            playing = bGUI.reset()


def startGame(boardState, bGUI):
    boardState[3][3]= "white"
    boardState[4][4] = "white"
    boardState[4][3] = "black"
    boardState[3][4] = "black"
    bGUI.draw(boardState)
    return bGUI.startGame()


main()
