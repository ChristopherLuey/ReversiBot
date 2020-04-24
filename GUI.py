# File: GUI.py
# Written By: Kyler Rosen
# Date: 4/28/20
# GUI for Reversi

from graphics import *
from Button import *


class GUI:
    def __init__(self):

        self.win = GraphWin("window", 1500, 900)

        self.win.setCoords(0, 9, 15, 0)
        self.win.setBackground("grey")

        self.tiles = []

        # creates the board
        for i in range(1, 9):
            tempList = []
            for j in range(1, 9):
                tempList.append(Tile(i, j, self.win))
            self.tiles.append(tempList)

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

    def highlightSquares(self, validMove):
        for i in validMove:
            self.tiles[i[0][0]][i[0][1]].highlight()

        while True:
            click = self.getClick()
            if click == [-1, -1]: return -1
            anchor = []
            for index in range(len(validMove)):
                if click == validMove[index][0]:
                    anchor.append(index)
            if anchor:
                for k in validMove:
                    self.tiles[k[0][0]][k[0][1]].unhighlight()
                return anchor


class Tile:
    def __init__(self, xCoord, yCoord, win):
        self.Tile = Rectangle(Point(xCoord - 0.49, yCoord - 0.49), Point(xCoord + 0.49, yCoord + 0.49))

        self.color = "black"
        self.fill = "darkgreen"

        self.Tile.setOutline(self.color)
        self.Tile.setWidth(2)
        self.Tile.setFill(self.fill)

        self.Tile.draw(win)

        self.xCoord, self.yCoord = xCoord, yCoord

        self.occupied = ""

        self.piece = Circle(Point(xCoord, yCoord), 0.45)
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
        if color == "":
            self.occupied = ""
            self.piece.setFill(self.fill)
            self.piece.setOutline(self.fill)
        else:
            self.piece.setFill(color)
            self.piece.setOutline(color)
            self.occupied = color

    def getOccupied(self):
        return self.occupied