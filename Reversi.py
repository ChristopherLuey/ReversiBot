# File: Reversi.py
# Written By: Chrisotpher Luey
# Date: 04/21/20

from reversiBoard import *

def main():
    b = Board()
    bArr = b.getBoard()
    player = startGame(bArr, b)

    while True:
        if player == "black"




def startGame(bArr, b):
    b.startGame()
    bArr[3][3].setOccupied("white")
    bArr[4][4].setOccupied("white")
    bArr[4][3].setOccupied("black")
    bArr[3][4].setOccupied("black")


<<<<<<< HEAD
=======
    b.setMessage("Hello there my name is Kyler and I really like to mess things up because this is fun but right now I need a really long message to make sure that the text box works as expected.")

    pt = Point(-1,-1)
    while True:
    	pt = b.getClick()
    	bArr[pt[0]][pt[1]].highlight()


>>>>>>> 1bc5d233be4f57098eaf012cd2da6b9020fd470c
main()
