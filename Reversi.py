# File: Reversi.py
# Written By: Chrisotpher Luey
# Date: 04/28/20
# Reversi runner

from GUI import *
from Board import *
from Bot import *
from sympy import *
from sklearn.linear_model import LinearRegression
import sklearn


# import tensorflow as tf
# from tensorflow import keras

#[ 1.15069158  0.03068858 -0.18516679 -0.25227567  0.80942462  0.37203484, -0.04971215]

def main():
    bGUI = GUI()
    playing = True

    # model = keras.Sequential([
    #     keras.layers.Reshape(target_shape=(8 * 8,), input_shape=(8, 8)),
    #     keras.layers.Dense(units=2, activation='sigmoid'),
    # ])
    # model.compile(optimizer='adam',
    #               loss=tf.losses.CategoricalCrossentropy(from_logits=True),
    #               metrics=['accuracy'])
    # boardsx = []
    # boardsy = []
    # weights1 = []
    # weights2 = []
    # weights = []

    iterations = 0

    # f = open('weights.txt', 'w')
    # # for line in f:
    # #     weights.append(float(line))
    # for i in range(7):
    #     weights1.append(random.random()*2-1)
    #     weights2.append(random.random()*2-1)
    #     weights.append(random.random()*2-1)




    while playing:
        boardState = bGUI.getBoard()
        player = startGame(boardState, bGUI)
        score = [0, 0]
        turn = 0
        board = Board(boardState, turn, 0)
        board.setPlayer(1 - player)
        #print(weights1, weights2)
        while turn<60:
            for i in range(2):
                board = Board(boardState, turn, i)
                #board.defineWeights(weights)
                board.setPlayer(i)
                # b1 = Board(copy.deepcopy(boardState), turn, i)
                # if i == 0:
                #     b1.defineWeights(weights1)
                # elif i == 1:
                #     b1.defineWeights(weights2)
                # b1.setPlayer(i)
                # boardsx.append(b1)
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
                        # decision, board2, choice = bot.alphabeta(b, 3, -float("inf"), float("inf"), True)
                        # print(decision)
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
                        bGUI.setMessage2("There are no valid moves. The player will now play.")
                        pass

                    else:


                        bot = Bot(1 - player)

                        b = Board(copy.deepcopy(boardState), turn, 1-player)
                        b.setPlayer(1-player)
                        bGUI.highlightSquares(legalMoves, False)
                        
                        decision, board2, choice = bot.alphabeta(b, 3, -float("inf"), float("inf"), True)
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
            # c = copy.deepcopy(boardState)
            # for i in range(8):
            #     for j in range(8):
            #         if c[i][j] == "white":
            #             c[i][j] = 1
            #         elif c[i][j] == "black":
            #             c[i][j] = -1
            #         else:
            #             c[i][j] = 0
            #
            # boardsx.append(c)
        # if score[0] > score[1]:
        #     # weights1.clear()
        #     # for i in range(31):
        #     #     weights1.append(random.random() * 2 - 1)
        #
        #     for i in range(30):
        #         boardsy.append([1.0])
        #         boardsy.append([-1.0])
        #
        # else:
        #     for i in range(30):
        #         boardsy.append([-1.0])
        #         boardsy.append([1.0])

            # weights2.clear()
            #
            # for i in range(31):
            #     weights2.append(random.random() * 2 - 1)
        # print(len(boardsx), len(boardsy))
        # weights1.clear()
        # weights2.clear()
        # weights.clear()
        # for i in range(7):
        #     weights1.append(random.random() * 2 - 1)
        #     weights2.append(random.random() * 2 - 1)
        #     weights.append(random.random() * 2 - 1)

        # if iterations != 0 and iterations%1000 == 0:
        #
        #
        #
        #
        #     #learn(boardsx, boardsy, model)
        #     #weights = learn2(boardsx, boardsy, iterations, weights)
        #     boardsxnew = []
        #     for i in range(len(boardsx)):
        #         boardsx[i].evaluateBoard()
        #         boardsxnew.append(boardsx[i].getConstants())
        #     for i in range(60):
        #         reg = LinearRegression()
        #         reg.fit(boardsxnew[i::60], boardsy[i::60])
        #         print(reg.coef_)
        #         weights1.clear()
        #         weights1 = list(copy.deepcopy(list(reg.coef_)[0]))
        #         print(reg.intercept_)
        #         print("Coefficients at: " + str(i), file=f)
        #         print(weights1, file=f)
        #         print(reg.intercept_, file=f, end="\n\n")
        #     f.close()

        #print(weights1, weights2)
        playing = bGUI.reset()
        iterations+=1



# def learn(boardx, boardy, model):
#     model.fit(
#         x=boardx[0:len(boardx)-3],
#         y=boardy[0:len(boardy)-3],
#         epochs=10,
#         validation_data=(boardx[len(boardx)-3:len(boardx)-2], boardy[len(boardy)-3:len(boardy)-2]),
#         shuffle=True)
#     print(len(model.layers))
#     arr = model.predict(boardx[len(boardx)-2:len(boardx)-1])
#     print(arr)
#     print(boardy[len(boardy)-2:len(boardy)-1])
#     model.save("model.h5", save_format='h5')
#     model.save_weights("weights.h5", save_format='h5')

# def learn2(boardsx, boardsy, iteration, w):
#     adjustedWeights = []
#     for i in range(31):
#         adjustedWeights.append(0.0)
#
#     for i in range(len(boardsx)):
#         table = []
#         boardsx[i].defineWeights(w)
#         print(boardsx[i].evaluateBoard())
#         table.append(boardsx[i].getConstants())
#         table[k].append(boardsy[i])
#
#         print(table)
#         weights = rref(table)
#
#         for j in range(len(weights)):
#             adjustedWeights[j]+=weights[j]
#
#     f = open('weights'+str(iteration)+'.txt', 'w')
#     for i in range(31):
#         adjustedWeights[i] = adjustedWeights[i]/len(boardsx)
#
#         print(adjustedWeights[i], file=f)
#     f.close()
#     return adjustedWeights

# def rref(table):
#     m = Matrix(table)
#     print(m)
#     arr = m.rref()
#     print(arr)
#     weights = []
#     if len(arr[1]) == 7:
#         r = arr[0].tolist()
#         for i in r:
#             weights.append(i)
#         print(weights)
#         return weights
#     return []



def startGame(boardState, bGUI):
    boardState[3][3]= "white"
    boardState[4][4] = "white"
    boardState[4][3] = "black"
    boardState[3][4] = "black"
    bGUI.draw(boardState)
    #return bGUI.startGame()
    return 0


main()
