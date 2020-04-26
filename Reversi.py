# File: Reversi.py
# Written By: Chrisotpher Luey
# Date: 04/28/20
# Reversi runner

from GUI import *
from Board import *
from Bot import *

import tensorflow as tf
from tensorflow import keras

def main():
    bGUI = GUI()
    playing = True

    # model = keras.Sequential([
    #     keras.layers.Reshape(target_shape=(8 * 8,), input_shape=(8, 8)),
    #     keras.layers.Dense(units=2, activation='relu'),
    # ])
    # boardsx = []
    # boardsy = []
    #
    # iterations = 0

    while playing:
        boardState = bGUI.getBoard()
        player = startGame(boardState, bGUI)
        score = [0, 0]
        turn = 0
        board = Board(boardState, turn, 0)
        board.setPlayer(1 - player)
        while turn<64:
            for i in range(2):
                board = Board(boardState, turn, i)
                bGUI.setMessage2("It is now " + ["black's", "white's"][i] + " turn.")
                if player == i:

                    legalMoves = board.calculateLegalMoves(player)
                    if not legalMoves:
                        bGUI.setMessage2("There are no valid moves. The bot will now play.")
                        pass
                    else:
                        anchor = bGUI.highlightSquares(legalMoves, True)
                        if anchor:
                            boardState[legalMoves[anchor[0]][0][0]][legalMoves[anchor[0]][0][1]] = ["black", "white"][player]
                            board.calculateFlipSquares(legalMoves, anchor, player)
                            bGUI.draw(boardState)
                        else:
                            playing = False
                            turn = 65
                            break

                        # bot = Bot(player)
                        #
                        # b = Board(copy.deepcopy(boardState), turn, i)
                        # bGUI.highlightSquares(legalMoves, False)
                        # decision, board2, choice = bot.alphabeta(b, 1, -float("inf"), float("inf"), True)
                        # #choice = legalMoves[random.randint(0,len(legalMoves)-1)][0]
                        # anchor = []
                        # for index in range(len(legalMoves)):
                        #     if choice == legalMoves[index][0]:
                        #         anchor.append(index)
                        #
                        # board.move(legalMoves, anchor, player)
                        # board.calculateFlipSquares(legalMoves, anchor, player)
                        # bGUI.unhighlightSquares(legalMoves)
                        # bGUI.draw(boardState)
                        # bGUI.setMessage("AI has played " + str(choice[0] + 1) + ", " + str(choice[1] + 1))
                else:
                    legalMoves = board.calculateLegalMoves(1-player)
                    if not legalMoves:
                        #bGUI.setMessage2("There are no valid moves. The player will now play.")
                        pass

                    else:

                        # call (current state of board, depth, -float inf, float inf, true)

                        bot = Bot(1 - player)

                        b = Board(copy.deepcopy(boardState), turn, 1-i)
                        bGUI.highlightSquares(legalMoves, False)
                        
                        decision, board2, choice = bot.alphabeta(b, 1, -float("inf"), float("inf"), True)
                        #choice = legalMoves[random.randint(0,len(legalMoves)-1)][0]

                        anchor = []
                        for index in range(len(legalMoves)):
                            if choice == legalMoves[index][0]:
                                anchor.append(index)
                        board.move(legalMoves, anchor, 1-player)
                        board.calculateFlipSquares(legalMoves, anchor, 1-player)
                        bGUI.unhighlightSquares(legalMoves)
                        bGUI.draw(boardState)
                        bGUI.setMessage("AI has played " + str(choice[0]+1) + ", " + str(choice[1]+1))

                score = board.calculateScore()
                board.incrementTurn()
                legalMoves.clear()
                turn+=1
        #     c = copy.deepcopy(boardState)
        #     for i in range(8):
        #         for j in range(8):
        #             if c[i][j] == "white":
        #                 c[i][j] = 1
        #             elif c[i][j] == "black":
        #                 c[i][j] = -1
        #             else:
        #                 c[i][j] = 0
        #
        #     boardsx.append(c)
        # if score[0] > score[1]:
        #     for i in range(32):
        #         boardsy.append([1,0])
        # else:
        #     for i in range(32):
        #         boardsy.append([0,1])
        #
        # if iterations%1000 == 0:
        #
        #     learn(boardsx, boardsy, model)

        playing = bGUI.reset()
        #iterations+=1
        #print(iterations)

def learn(boardx, boardy, model):
    model.compile(optimizer='adam',
                  loss=tf.losses.CategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.fit(
        x=boardx[0:len(boardx)-3],
        y=boardy[0:len(boardy)-3],
        epochs=10,
        validation_data=(boardx[len(boardx)-3:len(boardx)-2], boardy[len(boardy)-3:len(boardy)-2]),
        shuffle=True)
    print(len(model.layers))
    arr = model.predict(boardx[len(boardx)-2:len(boardx)-1])
    print(arr)
    model.save("model.h5", save_format='h5')
    model.save_weights("weights.h5", save_format='h5')


def startGame(boardState, bGUI):
    boardState[3][3]= "white"
    boardState[4][4] = "white"
    boardState[4][3] = "black"
    boardState[3][4] = "black"
    bGUI.draw(boardState)
    return bGUI.startGame()
    return 0


main()
