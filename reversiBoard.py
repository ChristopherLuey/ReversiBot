from graphics import *

def createGUI():

	win = GraphWin("window",1500,900)

	win.setCoords(0,0,15,9)
	win.setBackground("grey")

	tiles = []

	#creates the board
	for i in range(1,9):
		tempList = []
		for j in range(1,9):
			tempList.append(Tile(i,j,(i+j)%2,win))
		tiles.append(tempList)



class Tile:
	def __init__(self,xCoord,yCoord,color,win):
		self.Tile = Rectangle(Point(xCoord-0.45, yCoord-0.45),Point(xCoord+0.45, yCoord+0.45))

		self.color = "darkgreen"
		if color:
			self.color = "White"

		self.Tile.setOutline(self.color)
		self.Tile.setWidth(10)
		self.Tile.setFill(self.color)

		self.Tile.draw(win)

		self.xCoord,self.yCoord = xCoord,yCoord

		self.piece = ""

	def highlight(self):
		self.Tile.setOutline("Yellow")

	def redHighlight(self):
		self.Tile.setOutline("red")

	def clear(self):
		self.Tile.setOutline(self.color)

	def isClicked(self,pt):
		return self.xCoord-0.5 < pt.getX() < self.xCoord+0.5 and self.yCoord-0.5 < pt.getY() < self.yCoord+0.5

	def setPiece(self,piece):
		self.piece = piece

	def getPiece(self):
		return self.piece