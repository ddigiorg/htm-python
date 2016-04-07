from OpenGL.GL import *
from OpenGL.GLU import *

color_dict = {
	'r': (1,0,0),
	'g': (0,1,0),
	'b': (0,0,1),
	'w': (1,1,1)
	}

class Cube:
	def __init__(self):    
		self.position = (0, 0, 0)
      
		self.vertex_positions = [  1.0,  1.0,  1.0,  1.0,  1.0, -1.0, -1.0,  1.0, -1.0, 
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

		self.color = color_dict['w']
      
		self.vertex_colors    = [  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,
								   1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,
								   0.8,  0.8,  0.8,  0.8,  0.8,  0.8,  0.8,  0.8,  0.8,
								   0.8,  0.8,  0.8,  0.8,  0.8,  0.8,  0.8,  0.8,  0.8,
								   0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,
								   0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,  0.6,
								   0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,
								   0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,  0.4,
								   0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2,
								   0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2,  0.2,
								   0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1,
								   0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1]


	def setPosition(self, x, y, z):
		self.position = (x, y, z)
		new_vertex_positions = []
		for i in range(0, len(self.vertex_positions), 3):
			new_vertex_positions.append(self.vertex_positions[i  ] + x)
			new_vertex_positions.append(self.vertex_positions[i+1] + y)
			new_vertex_positions.append(self.vertex_positions[i+2] + z)

		self.vertex_positions = new_vertex_positions


	def setColor(self, color):
		self.color = color_dict[color]
		new_vertex_colors = []
		for i in range(0, len(self.vertex_colors), 3):
			new_vertex_colors.append(0.0)
			new_vertex_colors.append(0.0)
			new_vertex_colors.append(1.0)

		self.vertex_colors = new_vertex_colors


	def getPosition(self):
		return self.position


	def getColor(self):
		return self.color


	def getVertexPositions(self):
		return self.vertex_positions


	def getVertexColors(self):
		return self.vertex_colors
