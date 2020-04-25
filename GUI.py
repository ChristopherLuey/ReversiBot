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
        self.quitButton = Button(Point(13.5, 0.75), 0.5, 1, "QUIT")
        self.quitButton.setColor("red", "maroon")
        self.quitButton.setActive()
        self.quitButton.draw(self.win)

        self.textBackground = Rectangle(Point(10, 1.5), Point(14, 7.5))
        self.textBackground.setFill("lightgrey")
        self.textBackground.setOutline("lightgrey")
        self.textBackground.draw(self.win)

        self.text = Text(Point(12, 4.5), "")
        self.text.setSize(16)
        self.text.setFace("courier")
        self.text.draw(self.win)

        self.textBackground2 = Rectangle(Point(10, 7.75), Point(14, 8.75))
        self.textBackground2.setFill("lightgrey")
        self.textBackground2.setOutline("lightgrey")
        self.textBackground2.draw(self.win)

        self.text2 = Text(Point(12, 8.25), "")
        self.text2.setSize(16)
        self.text2.setFace("courier")
        self.text2.draw(self.win)

        self.textBackground3 = Rectangle(Point(10, 0.5), Point(12, 1.25))
        self.textBackground3.setFill("lightgrey")
        self.textBackground3.setOutline("lightgrey")
        self.textBackground3.draw(self.win)

        self.scoreboard = Text(Point(11, 0.875), "")
        self.scoreboard.setSize(16)
        self.scoreboard.setFace("courier")
        self.scoreboard.draw(self.win)

        self.message = []

        self.lineCount = 0


        for i in range(18):
            self.message.append("")
            self.lineCount += 2


        self.blackScore = 0
        self.whiteScore = 0

        self.updateScoreboard()

    def updateScoreboard(self):
        self.scoreboard.setText(("White Score: "+str(self.whiteScore)).ljust(15)+"\n"+("Black Score: "+str(self.blackScore)).ljust(15))


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
                    self.lineCount +=1
                else:
                    message = message + word + " "

        self.message.append(message)
        self.lineCount +=2
        
        while self.lineCount >=36:
            extraLines = self.message[0].count("\n")
            self.lineCount -= extraLines + 2
            self.message.pop(0)

        self.text.setText("\n\n".join(self.message))

    def setMessage2(self, message):
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

        self.text2.setText(message)

    self.messageClear(self):
        self.message = []

        for i in range(17):
            self.message.append("")
            self.lineCount += 2

        self.setMessage("")


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

    def unhighlightSquares(self, validMove):
        for k in validMove:
            self.tilesDraw[k[0][0]][k[0][1]].unhighlight()


    def draw(self, boardState):
        self.whiteScore,self.blackScore = 0,0
        for i in range(8):
            for j in range(8):
                if not boardState[i][j] == "":
                    self.tilesDraw[i][j].drawPiece(boardState[i][j])
                    if boardState[i][j] == "black":
                        self.blackScore += 1

                    elif boardState[i][j] == "white":
                        self.whiteScore += 1

        self.updateScoreboard()

    def reset(self):
        win = GraphWin("Play Again", 500, 200)
        mover, moveg, moveb = 90, 117, 8

        for i in range(104, 0, -1):
            c = Circle(Point(650, 375), i * 10)
            c.setFill(color_rgb(int(9 + mover * i / 102), int(130 - moveg * i / 102), int(230 - moveb * i / 102)))
            c.setOutline(color_rgb(int(9 + mover * i / 102), int(130 - moveg * i / 102), int(230 - moveb * i / 102)))
            c.setWidth(10)
            c.draw(win)

        t = Text(Point(250, 40), "Would you like to play again?").draw(win)
        t.setSize(25)
        t.setStyle("bold")

        b = Button(Point(150, 140), 50, 125, "Yes")
        b.draw(win)
        b.setColor("dimgrey", "black")
        w = Button(Point(350, 140), 50, 125, "No")
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
                for i in range(8):
                    for j in range(8):
                        self.tilesDraw[i][j].drawPiece("")
                        self.tiles[i][j] = ""
                return True
            elif w.isClicked(p):
                win.close()
                # 1: white
                return False
            p = win.getMouse()
        # for i in range(8):
        #     for j in range(8):
        #         self.tilesDraw[i][j].drawPiece("")
        #         self.tiles[i][j] = ""
        # return True



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
