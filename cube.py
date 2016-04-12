# http://www.paridebroggi.com/2015/06/optimized-cube-opengl-triangle-strip.html

from OpenGL.GL import *
from OpenGL.GLU import * # *

def getVertexTemplate():
	vertex_template = [
		 1.0,  1.0,  1.0,  1.0,  1.0, -1.0, -1.0,  1.0, -1.0,
		 1.0,  1.0,  1.0, -1.0,  1.0, -1.0, -1.0,  1.0,  1.0,
		-1.0,  1.0,  1.0, -1.0, -1.0,  1.0,  1.0, -1.0,  1.0,
		 1.0,  1.0,  1.0, -1.0,  1.0,  1.0,  1.0, -1.0,  1.0,
		-1.0, -1.0, -1.0, -1.0, -1.0,  1.0, -1.0,  1.0,  1.0,
		-1.0, -1.0, -1.0, -1.0,  1.0,  1.0, -1.0,  1.0, -1.0,
		 1.0,  1.0, -1.0, -1.0, -1.0, -1.0, -1.0,  1.0, -1.0,
    	 1.0,  1.0, -1.0,  1.0, -1.0, -1.0, -1.0, -1.0, -1.0,
		 1.0,  1.0,  1.0,  1.0, -1.0, -1.0,  1.0,  1.0, -1.0,
		 1.0, -1.0, -1.0,  1.0,  1.0,  1.0,  1.0, -1.0,  1.0,
		 1.0, -1.0,  1.0, -1.0, -1.0, -1.0,  1.0, -1.0, -1.0,
		 1.0, -1.0,  1.0, -1.0, -1.0,  1.0, -1.0, -1.0, -1.0] 
	
	return vertex_template

class Cube:
	def __init__(self):
		# xyz
		self.position = (0, 0, 0)

		# rgba
		self.color = (1, 1, 1, 1)
      
	def setPosition(self, x, y, z):
		self.position = (x, y, z)

	def setColor(self, r, g, b, a):
		self.color = (r, g, b, a)

	def getPosition(self):
		return self.position

	def getColor(self):
		return self.color
