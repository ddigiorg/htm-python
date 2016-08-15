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

class Display(object):
	ESCAPE = '\x1b'

	def __init__(self, window_width, window_height, in_size, c_size, npc_size):
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
		self.in_size  = in_size
		self.c_size   = c_size
		self.npc_size = npc_size

		self.polygon_size = self.in_size + self.c_size * self.npc_size
		self.POLYGON_SPACING = 0.5

		# View projection  variables
		self.ortho_matrix = None
		self.view_matrix  = None
		self.view_x     = -35.0
		self.view_y     = 0.0
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
		self.template_data = None
		self.position_data = None
		self.color_data    = None
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


	def initPolygonGraphicsData(self):
		self.position_data  = np.array( [0.0, 0.0] * self.polygon_size, dtype=np.float16)

		# Input neuron positions for graphics as 1D grid
		for i in range(self.in_size):
			index = i * 2
			self.position_data[index    ] = 0.0 + i * (1.0 + self.POLYGON_SPACING) # x world position
			self.position_data[index + 1] = 0.0                                    # y world position

		# Layer3b neuron positions for graphics as 2D grid
		for c in range(self.c_size):
			for npc in range(self.npc_size):
				index = ((c * self.npc_size + npc) + self.in_size) * 2
				self.position_data[index    ] = 0.0 + c   * (1.0 + self.POLYGON_SPACING) # x world position
				self.position_data[index + 1] = 3.0 + npc * (1.0 + self.POLYGON_SPACING) # y world position

		self.color_data =  np.array( [0.5, 0.5, 0.5] * self.polygon_size, dtype=np.float16)

	def updateViewProjection(self):
		self.view_matrix = [1.0,         0.0,         0.0,         0.0,
                            0.0,         1.0,         0.0,         0.0,
                            0.0,         0.0,         1.0,         0.0,
                            self.view_x, self.view_y, self.view_z, 1.0]


	def updatePolygonTemplate(self):
		# Vertex locations for square polygon template
		template_list = [-0.5,  0.5, -0.5, -0.5, 0.5, -0.5, 0.5,  0.5, -0.5,  0.5, 0.5, -0.5]
#		template_list = [-0.0,  0.0] # For GL_POINTS
		self.template_data = np.array(template_list, dtype=np.float16)

		# Opengl VBO polygon template buffer bound, filled with data, and shader variable updated
		glBindBuffer(GL_ARRAY_BUFFER, self.template_buffer)
		glBufferData(GL_ARRAY_BUFFER, self.template_data, GL_STATIC_DRAW)
		glEnableVertexAttribArray(self.shaders_template_loc)
		glVertexAttribPointer(self.shaders_template_loc, 2, GL_HALF_FLOAT, False, 0, None)


	def updatePolygonPositions(self):
		# Opengl VBO polygon position buffer bound, filled with data, and shader variable updated
		glBindBuffer(GL_ARRAY_BUFFER, self.position_buffer)
		glBufferData(GL_ARRAY_BUFFER, self.position_data, GL_STATIC_DRAW)
		glEnableVertexAttribArray(self.shaders_position_loc)
		glVertexAttribPointer(self.shaders_position_loc, 2, GL_HALF_FLOAT, False, 0, None)


	def updatePolygonColors(self, inputs, layer3b):

		# Set all input and layer3b neurons to Inactive (Grey)
		self.color_data =  np.array( [0.5, 0.5, 0.5] * self.polygon_size, dtype=np.float16)

		for i in range(self.in_size):
			index = i * 3
			if inputs[i] == 1:
				self.color_data[index:index + 3] = [0.0, 1.0, 0.0] # Active (Green)

		for n in layer3b.n_active_addresses:
			index = (self.in_size + n) * 3
			self.color_data[index:index + 3] = [0.0, 1.0, 0.0] # Active (Green)

		for n in layer3b.n_learn_addresses:
			index = (self.in_size + n) * 3
			self.color_data[index:index + 3] = [0.0, 0.0, 1.0] # Learn (Blue)

		for n in layer3b.n_predict_addresses:
			index = (self.in_size + n) * 3
			self.color_data[index:index + 3] = [1.0, 0.0, 1.0] # Predict (Violet)


		# Opengl VBO polygon color buffer bound, filled with data, and shader variable updated
		glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
		glBufferData(GL_ARRAY_BUFFER, self.color_data, GL_STREAM_DRAW)
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
		glDrawArraysInstanced(GL_TRIANGLES, 0, 6*2, self.polygon_size) 

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