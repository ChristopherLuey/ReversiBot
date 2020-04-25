# File: GUI.py
# Written By: Kyler Rosen
# Date: 4/28/20
# GUI for Reversi

from graphics import *
from Button import *
import time

class GUI:
    def __init__(self):

        self.win = GraphWin("window", 1500, 900)

        self.win.setCoords(0, 9, 15, 0)
        self.win.setBackground("grey")

        self.tiles = []
        self.tilesDraw = []

        # creates the board
        for i in range(1, 9):
            tempList = []
            tempListTilesDraw = []
            for j in range(1, 9):
                tempList.append("")
                tempListTilesDraw.append(Tile())
                tempListTilesDraw[j-1].draw(self.win, i, j)
            self.tiles.append(tempList)
            self.tilesDraw.append(tempListTilesDraw)

        # buttons and text
        self.quitButton = Button(Point(13, 1), 0.5, 1, "QUIT")
        self.quitButton.setColor("red", "maroon")
        self.quitButton.setActive()
        self.quitButton.draw(self.win)

        self.textBackground = Rectangle(Point(10, 3.5), Point(14, 5.5))
        self.textBackground.setFill("lightgrey")
        self.textBackground.setOutline("lightgrey")
        self.textBackground.draw(self.win)

        self.text = Text(Point(12, 4.5), "")
        self.text.setSize(16)
        self.text.setFace("courier")
        self.text.draw(self.win)

    def getBoard(self):
        return self.tiles

    def getTile(self, x, y):
        return self.tiles[x][y]

    def getClick(self):
        pt = self.win.getMouse()
        if self.quitButton.isClicked(pt): return [-1, -1]
        return [round(pt.getX()) - 1, round(pt.getY()) - 1]

    def setMessage(self, message):
        # setText of message, modifies message and adds new lines if message is too long to fit width of box
        if len(message) > 30:
            wordList = message.split()
            lineChrCount = 0
            message = ""
            for word in wordList:
                lineChrCount = len(word) + lineChrCount
                if lineChrCount > 30:
                    message = message + "\n" + word + " "
                    lineChrCount = len(word)
                else:
                    message = message + word + " "
        self.text.setText(message)

    def startGame(self):
        win = GraphWin("Decide Player", 500, 200)
        mover, moveg, moveb = 90, 117, 8

        for i in range(104, 0, -1):
            c = Circle(Point(650, 375), i * 10)
            c.setFill(color_rgb(int(9 + mover * i / 102), int(130 - moveg * i / 102), int(230 - moveb * i / 102)))
            c.setOutline(color_rgb(int(9 + mover * i / 102), int(130 - moveg * i / 102), int(230 - moveb * i / 102)))
            c.setWidth(10)
            c.draw(win)

        t = Text(Point(250, 40), "Would you like to play Black or White?").draw(win)
        t.setSize(25)
        t.setStyle("bold")

        b = Button(Point(150, 140), 50, 125, "Black")
        b.draw(win)
        b.setColor("dimgrey", "black")
        w = Button(Point(350, 140), 50, 125, "White")
        w.draw(win)
        w.setColor("white", "lightgrey")
        w.setTextColor("black")
        b.setActive()
        w.setActive()

        p = win.getMouse()
        while True:
            if b.isClicked(p):
                win.close()
                # 0: black
                return 0
            elif w.isClicked(p):
                win.close()
                # 1: white
                return 1
            p = win.getMouse()

    def highlightSquares(self, validMove, bool):
        for i in validMove:
            self.tilesDraw[i[0][0]][i[0][1]].highlight()

        if bool:
            while True:
                click = self.getClick()
                if click == [-1, -1]: return -1
                anchor = []
                for index in range(len(validMove)):
                    if click == validMove[index][0]:
                        anchor.append(index)
                if anchor:
                    for k in validMove:
                        self.tilesDraw[k[0][0]][k[0][1]].unhighlight()
                    return anchor
        else:
            time.sleep(1.0)
            for k in validMove:
                self.tilesDraw[k[0][0]][k[0][1]].unhighlight()


    def draw(self, boardState):
        for i in range(8):
            for j in range(8):
                if not boardState[i][j] == "":
                    self.tilesDraw[i][j].drawPiece(boardState[i][j])


class Tile:
    def __init__(self):
        self.occupied = ""


    def draw(self, win, xCoord, yCoord):
        self.xCoord, self.yCoord = xCoord, yCoord
        self.Tile = Rectangle(Point(self.xCoord - 0.49, self.yCoord - 0.49), Point(self.xCoord + 0.49, self.yCoord + 0.49))
        self.color = "black"
        self.fill = "darkgreen"

        self.Tile.setOutline(self.color)
        self.Tile.setWidth(2)
        self.Tile.setFill(self.fill)

        self.Tile.draw(win)

        self.occupied = ""

        self.piece = Circle(Point(self.xCoord, self.yCoord), 0.45)
        self.piece.setFill(self.fill)
        self.piece.setOutline(self.fill)

        self.piece.draw(win)

    def unhighlight(self):
        self.Tile.setOutline(self.color)
        self.Tile.setFill("darkgreen")

    def highlight(self):
        self.Tile.setOutline("red")
        self.Tile.setFill("green")

    def reset(self):
        self.unhighlight()
        self.setOccupied("")


    def isClicked(self, pt):
        return self.xCoord - 0.5 < pt.getX() < self.xCoord + 0.5 and self.yCoord - 0.5 < pt.getY() < self.yCoord + 0.5

    def setOccupied(self, color):
        self.occupied = color

    def drawPiece(self, color):
        if color == "":
            self.piece.setFill(self.fill)
            self.piece.setOutline(self.fill)
        else:
            self.piece.setFill(color)
            self.piece.setOutline(color)

    def getOccupied(self):
        return self.occupied
