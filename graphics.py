# graphics.py
"""
TODO

+ Work on method for only displaying active columns in opengl window
+ Work on adding text capabilities in opengl windows
+ Work on adding mouse capabilities
+ Address issues and comments
+ Add docstring comments for class and methods

"""
from OpenGL.GL import *
from OpenGL.GLUT import *
#from OpenGL.GLU import * # <-- uneeded so delete when finished 
import numpy as np
import shader as shader


class Polygon(object):
	template = [-0.5,  0.5, -0.5, -0.5, 0.5, -0.5, 0.5,  0.5, -0.5,  0.5, 0.5, -0.5]
	SPACING = 0.1

	def __init__(self, x_idx, y_idx, x_offset, y_offset):
		self.x_idx = x_idx
		self.y_idx = y_idx

		self.x_offset = x_offset
		self.y_offset = y_offset

		self.position = [0.0, 0.0]
		self.position[0] = x_offset + x_idx * (1.0 + self.SPACING) # x world position
		self.position[1] = y_offset + y_idx * (1.0 + self.SPACING) # y world position

		self.color = [0.5, 0.5, 0.5]

class Display(object):
	ESCAPE = '\x1b'

	def __init__(self, window_width, window_height, num_inputs, num_columns, num_neurons_per_column):
		# OpenGL application variables
		self.window_width = window_width
		self.window_height = window_height

		# Opengl Initilization
		glutInit()                                   # Initialize opengl
		glutInitDisplayMode(GLUT_RGBA)               # RGBA color
		glutInitWindowSize(self.window_width,        # Initialize window size
                           self.window_height)
		glutInitWindowPosition(0, 0)                 # Application window placed at upper left corner of monitor screen
		self.windowID = glutCreateWindow("HTM Test") # Create windowID with name "HTM"
		glutKeyboardFunc(self.keyPressed)            # Register function when keyboard pressed
		glutSpecialFunc(self.keyPressed)             # Register function when keyboard pressed
		glClearColor(0.0, 0.0, 0.0, 1.0)             # Black background

		# Polygon variables
		if num_inputs > 70:
			self.num_inputs = 70
		else:
			self.num_inputs = num_inputs

		if num_columns > 70:
			self.num_columns = 70
		else:
			self.num_columns = num_columns

		self.num_neurons_per_column = num_neurons_per_column

		self.num_polygons = self.num_inputs + self.num_columns * self.num_neurons_per_column

		if num_columns > 50:
			num_c = 50
		else:
			num_c = num_columns

		self.num_neurons = self.num_columns * num_neurons_per_column

		self.polygons0 = [Polygon(x_idx, 0, 0, 0) for x_idx in range(self.num_inputs)]
		self.polygons1 = [Polygon(x_idx, y_idx, 0, 3) for x_idx in range(self.num_columns) for y_idx in range(num_neurons_per_column)]

		# View projection  variables
		self.ortho_matrix = None
		self.view_matrix  = None
		self.view_x     = -38.0
		self.view_y     = -10.0
		self.view_z     = 10.0
		self.view_speed = 0.5

		# Shader variables
		vertex_shader   = shader.compile_shader("VS")
		fragment_shader = shader.compile_shader("FS")

		self.shaders_programID      = shader.link_shader_program(vertex_shader, fragment_shader)     
		self.shaders_template_loc   = glGetAttribLocation( self.shaders_programID, "polygon_template")
		self.shaders_position_loc   = glGetAttribLocation( self.shaders_programID, "polygon_position")
		self.shaders_color_loc      = glGetAttribLocation( self.shaders_programID, "polygon_color"   )
		self.shaders_scale_loc      = glGetUniformLocation(self.shaders_programID, "polygon_scale"   )
		self.shaders_projection_loc = glGetUniformLocation(self.shaders_programID, "projection"      )
		self.shaders_view_loc       = glGetUniformLocation(self.shaders_programID, "view"            )

		# VBO variables
		self.template_buffer = glGenBuffers(1)
		self.position_buffer = glGenBuffers(1)
		self.color_buffer    = glGenBuffers(1)

		# Get shader ID
		glUseProgram(self.shaders_programID)
   
		# Opengl VBO polygon template buffer bound and left empty
		glBindBuffer(GL_ARRAY_BUFFER, self.template_buffer)
		glBufferData(GL_ARRAY_BUFFER, None, GL_STATIC_DRAW)

		# Opengl VBO polygon position buffer bound and left empty
		glBindBuffer(GL_ARRAY_BUFFER, self.position_buffer)
		glBufferData(GL_ARRAY_BUFFER, None, GL_STATIC_DRAW)

		# Opengl VBO polygon color buffer bound and left empty
		glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
		glBufferData(GL_ARRAY_BUFFER, None, GL_STREAM_DRAW)


	def initOrthographicProjection(self):
		l = 0.0
		r = self.window_width  / 100
		t = self.window_height / 100
		b = 0.0
		f = -1.0
		n = 1.0

		self.ortho_matrix = [2.0/(r-l),    0.0,          0.0,          0.0,
                             0.0,          2.0/(t-b),    0.0,          0.0,
                             0,0,          0.0,          -2.0/(f-n),   0.0,
                             -(r+l)/(r-l), -(t+b)/(t-b), -(f+n)/(f-n), 1.0]


	def updateViewProjection(self):
		self.view_matrix = [1.0,         0.0,         0.0,         0.0,
                            0.0,         1.0,         0.0,         0.0,
                            0.0,         0.0,         1.0,         0.0,
                            self.view_x, self.view_y, self.view_z, 1.0]


	def updatePolygonTemplate(self):
		# Vertex locations for square polygon template
		template_data = np.array(self.polygons0[0].template, dtype=np.float16)

		# Opengl VBO polygon template buffer bound, filled with data, and shader variable updated
		glBindBuffer(GL_ARRAY_BUFFER, self.template_buffer)
		glBufferData(GL_ARRAY_BUFFER, template_data, GL_STATIC_DRAW)
		glEnableVertexAttribArray(self.shaders_template_loc)
		glVertexAttribPointer(self.shaders_template_loc, 2, GL_HALF_FLOAT, False, 0, None)


	def updatePolygonPositions(self):
		# Opengl VBO polygon position buffer bound, filled with data, and shader variable updated
		position_list = []
		for polygon in self.polygons0:
			position_list += polygon.position

		for polygon in self.polygons1:
			position_list += polygon.position

		position_data = np.array(position_list, dtype=np.float16)

		glBindBuffer(GL_ARRAY_BUFFER, self.position_buffer)
		glBufferData(GL_ARRAY_BUFFER, position_data, GL_STATIC_DRAW)
		glEnableVertexAttribArray(self.shaders_position_loc)
		glVertexAttribPointer(self.shaders_position_loc, 2, GL_HALF_FLOAT, False, 0, None)


	# MAKE MORE EFFICIENT
	def updatePolygonColors(self, inputs, layer):
		
		active_neurons  = [active_neuron  for active_neuron  in layer.active_neurons  if active_neuron.idx  < self.num_neurons]
		winner_neurons  = [winner_neuron  for winner_neuron  in layer.winner_neurons  if winner_neuron.idx  < self.num_neurons]
		predict_neurons = [predict_neuron for predict_neuron in layer.predict_neurons if predict_neuron.idx < self.num_neurons]

		color_list = []

		for polygon in self.polygons0:
			if inputs[polygon.x_idx] == 1:
				polygon.color = [0.0, 1.0, 0.0] # Active (Green)
			else:
				polygon.color = [0.5, 0.5, 0.5] # Inactive (Grey)
			color_list += polygon.color

		for polygon in self.polygons1: polygon.color = [0.5, 0.5, 0.5]
		
		for active_neuron in active_neurons:
			self.polygons1[active_neuron.idx].color = [0.0, 1.0, 0.0] # Active (Green)

		for winner_neuron in winner_neurons:
			self.polygons1[winner_neuron.idx].color = [0.0, 0.0, 1.0] # Winner (Blue) 

		for predict_neuron in predict_neurons:
			self.polygons1[predict_neuron.idx].color = [1.0, 0.0, 1.0] # Predictr (Violet) 

		for polygon in self.polygons1: color_list += polygon.color

		color_data = np.array(color_list, dtype=np.float16)

		# Opengl VBO polygon color buffer bound, filled with data, and shader variable updated
		glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
		glBufferData(GL_ARRAY_BUFFER, color_data, GL_STREAM_DRAW)
		glEnableVertexAttribArray(self.shaders_color_loc)
		glVertexAttribPointer(self.shaders_color_loc, 3, GL_HALF_FLOAT, True, 0, None) # normalized for unsigned char


	def updateScene(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		# Update shader with polygon scale value, orthographic matrix, and view matrix
		glUniform1f(self.shaders_scale_loc, 1.0)
		glUniformMatrix4fv(self.shaders_projection_loc, 1, False, self.ortho_matrix)
		glUniformMatrix4fv(self.shaders_view_loc,       1, False, self.view_matrix)

		# * ?????????? For instancing... figure out what this does
		glVertexAttribDivisor(0, 0)
		glVertexAttribDivisor(1, 1)
		glVertexAttribDivisor(2, 1)

		# Draw cells: 6 vertices per triangle, 2 triangles per square
		glDrawArraysInstanced(GL_TRIANGLES, 0, 6*2, self.num_polygons) 

#		glDrawArraysInstanced(GL_POINTS, 0, 1, num_polys) 
#		glUniform1f(shaders_scale_loc, 2.0)
#		glDrawArraysInstanced(GL_TRIANGLES, 0, 6*2, num_polys) # 6 vertices per triangle, 2 triangles per square 

		# Flush the opengl rendering pipeline	
		glutSwapBuffers()	

	def keyPressed(self, key, x, y):
		if key == self.ESCAPE.encode():
			self.cleanup()
		if key == 'a'.encode():
			self.view_x += self.view_speed
		if key == 'd'.encode():
			self.view_x -= self.view_speed
		if key == 'q'.encode():
			self.view_y += self.view_speed
		if key == 'e'.encode():
			self.view_y -= self.view_speed
		if key == 's'.encode():
			self.view_z += self.view_speed
		if key == 'w'.encode():
			self.view_z -= self.view_speed
		glutPostRedisplay()

	def cleanup(self):
		glDisableVertexAttribArray(self.shaders_template_loc)
		glDisableVertexAttribArray(self.shaders_position_loc)
		glDisableVertexAttribArray(self.shaders_color_loc)

		glDeleteBuffers(1, GLfloat(self.template_buffer))
		glDeleteBuffers(1, GLfloat(self.position_buffer))
		glDeleteBuffers(1, GLfloat(self.color_buffer))
		glDeleteProgram(self.shaders_programID)
		glutDestroyWindow(self.windowID)
		exit(0)

	def runOpenglMainLoop(self):
		glutMainLoop()
