from graphics import *
from Button import *


class Board:
	def __init__(self):

		self.win = GraphWin("window",1500,900)

		self.win.setCoords(0,9,15,0)
		self.win.setBackground("grey")

		self.tiles = []

		#creates the board
		for i in range(1,9):
			tempList = []
			for j in range(1,9):
				tempList.append(Tile(i,j,self.win))
			self.tiles.append(tempList)

	def getBoard(self):
		return self.tiles

	def getTile(self,x,y):
		return self.tiles[x][y].getOccupied()

	def getClick(self):
		pt = self.win.getMouse()
		return [round(pt.getX())-1,round(pt.getY())-1]

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
		b.setColor("black", "darkgoldenrod")
		w = Button(Point(350, 140), 50, 125, "White")
		w.draw(win)
		w.setColor("white", "darkgoldenrod")
		w.setTextColor("black")
		b.setActive()
		w.setActive()
		p = win.getMouse()
		while True:
			if b.isClicked(p):
				return 'black'
			elif w.isClicked(p):
				return 'white'
			p = win.getMouse()


class Tile:
	def __init__(self,xCoord,yCoord,win):
		self.Tile = Rectangle(Point(xCoord-0.49, yCoord-0.49),Point(xCoord+0.49, yCoord+0.49))

		self.color = "black"
		self.fill = "darkgreen"

		self.Tile.setOutline(self.color)
		self.Tile.setWidth(5)
		self.Tile.setFill(self.fill)

		self.Tile.draw(win)

		self.xCoord,self.yCoord = xCoord,yCoord

		self.occupied = ""

		self.piece = Circle(Point(xCoord,yCoord),0.45)
		self.piece.setFill(self.fill)
		self.piece.setOutline(self.fill)

		self.piece.draw(win)

	def highlight(self):
		self.Tile.setWidth(10)
		self.Tile.setOutline("Yellow")

	def redHighlight(self):
		self.Tile.setOutline("red")

	def clear(self):
		self.Tile.setWidth(2)
		self.Tile.setOutline(self.color)

	def isClicked(self,pt):
		return self.xCoord-0.5 < pt.getX() < self.xCoord+0.5 and self.yCoord-0.5 < pt.getY() < self.yCoord+0.5

	def setOccupied(self,color):
		self.piece.setFill(color)
		self.piece.setOutline(color)
		self.occupied = color

	def getOccupied(self):
		return self.occupied

if __name__ == '__main__':
	Board = Board()

	while True:
		pt = Board.getClick()
		Board.setOccupied(pt[0],pt[1],"black")

