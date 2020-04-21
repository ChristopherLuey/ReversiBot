# File: Reversi.py
# Written By: Chrisotpher Luey
# Date: 04/21/20

from reversiBoard import *

def main():
    b = Board()
    bArr = b.getBoard()
    startGame()



def startGame():
    bArr[3][3].setOccupied("white")
    bArr[4][4].setOccupied("white")
    bArr[4][3].setOccupied("white")
    bArr[3][4].setOccupied("white")

main()
