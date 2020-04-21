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
		return [round(self.win.getMouse().getX())-1,round(self.win.getMouse().getY())-1]



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
		self.occupied = color

	def getOccupied(self):
		return self.occupied

if __name__ == '__main__':
	Board = Board()

	while True:
		print(Board.getClick())