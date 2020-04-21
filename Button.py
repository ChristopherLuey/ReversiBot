#Program: button.py
#Written by: Kyler Rosen
#Date: 09/26/19
#Function: Creates a button object for general programs

from graphics import *

class Button:

	def __init__ (self, center, height, width, content):
		#builds the top right and bottom left coords from the information inputted
		self.x1 = center.getX() - (width/2)
		self.x2 = center.getX() + (width/2)
		self.y1 = center.getY() - (height/2)
		self.y2 = center.getY() + (height/2)

		#creates the button's box from coords above.
		self.box = Rectangle(Point(self.x1,self.y1),Point(self.x2,self.y2))
		self.shadow = Rectangle(Point(self.x1,self.y2),Point(self.x2,self.y2+(self.y1-self.y2)/10))
		self.text = Text(center,content)
		self.box.move(0,5)
		self.text.move(0,5)

		#sets the colors of the box to inactive
		self.box.setFill("grey")
		self.shadow.setFill("darkgrey")
		self.box.setOutline("grey")
		self.shadow.setOutline("darkgrey")
		self.text.setTextColor("White")
		self.text.setStyle("bold")
		self.text.setSize(27)

		#sets the default color of the box once active
		self.color = "goldenrod"
		self.shadowColor = "darkgoldenrod"

		#button defaults to inactive
		self.active = False
		self.isDrawn = False

	def flip(self):
		self.shadow.undraw()
		self.shadow = Rectangle(Point(self.x1,self.y1),Point(self.x2,self.y1-(self.y2-self.y1)/10))

	def draw(self,window):
		#draws in all aspects of button
		self.isDrawn = True
		self.win = window
		self.box.draw(self.win)
		self.text.draw(self.win)
		if self.active == True:
			self.shadow.draw(self.win)

	def undraw(self):
		#undraws all aspects of button
		self.shadow.undraw()
		self.box.undraw()
		self.text.undraw()
	
	#checks that button is active and click is inside of button rectangle
	def isClicked(self,click):
		return (self.active and self.x1<=click.getX()<=self.x2 and self.y1<=click.getY()<=self.y2) 


	def setColor(self,fill,darker):
		#allows the button to change from default colors
		self.color = fill
		self.shadowColor = darker
		#if the button is active, it will change to the new color specified
		if self.active == True:
			self.box.setFill(self.color)
			self.shadow.setFill(self.shadowColor)
			self.box.setOutline(self.color)
			self.shadow.setOutline(self.shadowColor)


	def setActive(self):
		#changes the color to the default/specified color, sets status to active
		if self.active == False:
			self.active = True
			self.box.setFill(self.color)
			self.shadow.setFill(self.shadowColor)
			self.box.setOutline(self.color)
			self.shadow.setOutline(self.shadowColor)
			if self.isDrawn == True:
				self.shadow.draw(self.win)
			self.box.move(0,-5)
			self.text.move(0,-5)


	def setInactive(self):
		#changes the color to the grey, sets status to active
		if self.active == True:
			self.active = False
			self.box.setFill("grey")
			self.box.setOutline("grey")
			self.shadow.undraw()
			self.box.move(0,5)
			self.text.move(0,5)

	def toTop(self,win):
		#undraws and redraws button to bring button to top
		#used if something needs to be drawn behind it
		self.box.undraw()
		self.shadow.undraw()
		self.text.undraw()
		self.shadow.draw(win)
		self.box.draw(win)
		self.text.draw(win)

	def toggleActive(self):
		#determines current state of button, flips it.
		if self.active == True:
			self.setInactive()
		elif self.active == False:
			self.setActive()

	def setText(self,text):
		self.text.setText(text)