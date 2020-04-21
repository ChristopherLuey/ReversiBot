# File: Reversi.py
# Written By: Chrisotpher Luey
# Date: 04/21/20

from reversiBoard import *

def main():
    b = Board()
    bArr = b.getBoard()
    player = startGame(bArr, b)




def startGame(bArr, b):
    b.startGame()
    bArr[3][3].setOccupied("white")
    bArr[4][4].setOccupied("white")
    bArr[4][3].setOccupied("black")
    bArr[3][4].setOccupied("black")

    b.getClick()



main()
