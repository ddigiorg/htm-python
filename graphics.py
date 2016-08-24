# graphics.py
# http://stackoverflow.com/questions/166356/what-are-some-best-practices-for-opengl-coding-esp-w-r-t-object-orientation

from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import shader as shader

class Square(object):
	def __init__(self, idx_x, idx_y, size):
		self.idx_x = idx_x
		self.idx_y = idx_y
		self.template = [0, size, 0, 0, size, 0, size, size, 0, size, size, 0]
		self.position = [0.0, 0.0] #xy
		self.color    = [0.0, 0.0, 0.0] #rgb


class Scene(object):
	def __init__(self, num_inputs, num_columns, num_neurons_per_column):
		MAX_NUM_POLYS_X = 70

		if num_inputs > MAX_NUM_POLYS_X:
			self.num_inputs = MAX_NUM_POLYS_X
		else:
			self.num_inputs = num_inputs

		if num_columns > MAX_NUM_POLYS_X:
			self.num_columns = MAX_NUM_POLYS_X
		else:
			self.num_columns = num_columns

		self.num_neurons = self.num_columns * num_neurons_per_column
		self.num_polygons = self.num_inputs + self.num_neurons

		self.SIZE = 10  # Pixels

		self.squares0 = [Square(x_idx, 0, self.SIZE)
                         for x_idx in range(self.num_inputs)]

		self.squares1 = [Square(x_idx, y_idx, self.SIZE)
                         for x_idx in range(self.num_columns)
                         for y_idx in range(num_neurons_per_column)]

	def polygonTemplate(self):
		return self.squares0[0].template

	def polygonPositions(self):
		PADDING_X = 10  # Pixels
		PADDING_Y = 100 # Pixels
		SPACING   = 1   # Pixel

		position_list = []
		for square in self.squares0:
			square.position = [PADDING_X + square.idx_x * (self.SIZE + SPACING),  
                               PADDING_Y + square.idx_y * (self.SIZE + SPACING)]
			position_list += square.position

		for square in self.squares1:
			square.position = [PADDING_X      + square.idx_x * (self.SIZE + SPACING),  
                               PADDING_Y + 30 + square.idx_y * (self.SIZE + SPACING)]
			position_list += square.position

		return position_list

	def polygonColors(self, inputs, layer):
		active_neurons  = [active_neuron  for active_neuron  in layer.active_neurons  if active_neuron.idx  < self.num_neurons]
		winner_neurons  = [winner_neuron  for winner_neuron  in layer.winner_neurons  if winner_neuron.idx  < self.num_neurons]
		predict_neurons = [predict_neuron for predict_neuron in layer.predict_neurons if predict_neuron.idx < self.num_neurons]

		color_list = []

		for square in self.squares0:
			if inputs[square.idx_x] == 1:
				square.color = [0.0, 0.8, 0.0] # Active (Green)
			else:
				square.color = [0.2, 0.2, 0.2] # Inactive (Grey)
			color_list += square.color

		for square in self.squares1:
			square.color = [0.2, 0.2, 0.2]
		
		for active_neuron in active_neurons:
			self.squares1[active_neuron.idx].color = [0.0, 0.8, 0.0] # Active (Green)

		for winner_neuron in winner_neurons:
			self.squares1[winner_neuron.idx].color = [0.0, 0.0, 0.8] # Winner (Blue) 

		for predict_neuron in predict_neurons:
			self.squares1[predict_neuron.idx].color = [0.8, 0.0, 0.8] # Predict (Violet) 

		for square in self.squares1:
			color_list += square.color

		return color_list


class Camera(object):
	def __init__(self, window_width, window_height):

		self.window_width = window_width
		self.window_height = window_height

		self.view_x     = 0  # Pixels
		self.view_y     = 0  # Pixels
		self.view_z     = 1  # Unit
		self.view_speed = 10 # Pixels per move

		self.proj_matrix = None
		self.view_matrix = None

	def initOrthographicProjection(self):
		l =  0.0
		r =  self.window_width
		b =  0.0
		t =  self.window_height
		f = -1.0
		n =  1.0

		self.proj_matrix = [2.0/(r-l),    0.0,          0.0,          0.0,
                            0.0,          2.0/(t-b),    0.0,          0.0,
                            0.0,          0.0,          -2.0/(f-n),   0.0,
                            -(r+l)/(r-l), -(t+b)/(t-b), -(f+n)/(f-n), 1.0]

		return self.proj_matrix

	def updateView(self):
		self.view_matrix = [1.0,         0.0,         0.0,         0.0,
                            0.0,         1.0,         0.0,         0.0,
                            0.0,         0.0,         1.0,         0.0,
                            self.view_x, self.view_y, self.view_z, 1.0]

		return self.view_matrix


class OpenGLRenderer(object):
	ESCAPE = '\x1b'

	def __init__(self, camera_instance):
		self.flag = 1

		camera = camera_instance
		window_width  = camera.window_width
		window_height = camera.window_height

		# Opengl Initilization
		glutInit()                                      # Initialize opengl
		glutInitDisplayMode(GLUT_RGBA)                  # RGBA color
		glutInitWindowSize(window_width, window_height) # Initialize window size
		glutInitWindowPosition(0, 0)                    # Application window placed at upper left corner of monitor screen
		self.windowID = glutCreateWindow("HTM Test")    # Create windowID with name
		glutMouseFunc(self.mouseFunc)                   # Register function when mouse input recieved
		glutKeyboardFunc(self.keyboardFunc)             # Register function when keyboard pressed
		glutSpecialFunc(self.keyboardFunc)              # Register function when keyboard pressed
		glClearColor(0.0, 0.0, 0.0, 1.0)                # Black background

		# Shader variables
		vertex_shader   = shader.compile_shader("VS")
		fragment_shader = shader.compile_shader("FS")

		self.shaders_programID = shader.link_shader_program(vertex_shader, fragment_shader)     
		glUseProgram(self.shaders_programID)

		self.shaders_template_loc = glGetAttribLocation( self.shaders_programID, "polygon_template")
		self.shaders_position_loc = glGetAttribLocation( self.shaders_programID, "polygon_position")
		self.shaders_color_loc    = glGetAttribLocation( self.shaders_programID, "polygon_color"   )
		self.shaders_scale_loc    = glGetUniformLocation(self.shaders_programID, "polygon_scale"   )
		self.shaders_proj_loc     = glGetUniformLocation(self.shaders_programID, "projection"      )
		self.shaders_view_loc     = glGetUniformLocation(self.shaders_programID, "view"            )

		# VBO variables
		self.template_buffer = glGenBuffers(1)
		self.position_buffer = glGenBuffers(1)
		self.color_buffer    = glGenBuffers(1)

		# User Input Variables
		self.mouse_x = 0
		self.mouse_y = 0

	def updateTemplateVBO(self, template_list):
		# Opengl VBO polygon template buffer bound, filled with data, and shader variable updated
		template_data = np.array(template_list, dtype=np.float16)
		glBindBuffer(GL_ARRAY_BUFFER, self.template_buffer)
		glBufferData(GL_ARRAY_BUFFER, template_data, GL_STATIC_DRAW)
		glEnableVertexAttribArray(self.shaders_template_loc)
		glVertexAttribPointer(self.shaders_template_loc, 2, GL_HALF_FLOAT, False, 0, None)

	def updatePositionVBO(self, position_list):
		# Opengl VBO polygon position buffer bound, filled with data, and shader variable updated
		position_data = np.array(position_list, dtype=np.float16)
		glBindBuffer(GL_ARRAY_BUFFER, self.position_buffer)
		glBufferData(GL_ARRAY_BUFFER, position_data, GL_STATIC_DRAW)
		glEnableVertexAttribArray(self.shaders_position_loc)
		glVertexAttribPointer(self.shaders_position_loc, 2, GL_HALF_FLOAT, False, 0, None)

	def updateColorVBO(self, color_list):
		# Opengl VBO polygon color buffer bound, filled with data, and shader variable updated
		color_data = np.array(color_list, dtype=np.float16)
		glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
		glBufferData(GL_ARRAY_BUFFER, color_data, GL_STREAM_DRAW)
		glEnableVertexAttribArray(self.shaders_color_loc)
		glVertexAttribPointer(self.shaders_color_loc, 3, GL_HALF_FLOAT, True, 0, None) # normalized for unsigned char

	def updateViewMatrix(self, view_matrix):
 		glUniformMatrix4fv(self.shaders_view_loc, 1, False, view_matrix)

	def updateProjectionMatrix(self, proj_matrix):
		glUniformMatrix4fv(self.shaders_proj_loc, 1, False, proj_matrix)

	def drawScene(self, num_polygons):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		# Update shader with polygon scale value, orthographic matrix, and view matrix
		glUniform1f(self.shaders_scale_loc, 1.0)

		# * ?????????? For instancing... figure out what this does
		glVertexAttribDivisor(0, 0)
		glVertexAttribDivisor(1, 1)
		glVertexAttribDivisor(2, 1)

		# make a variable for the vertices (probably from template)
		# Draw cells: 6 vertices per triangle, 2 triangles per square
		glDrawArraysInstanced(GL_TRIANGLES, 0, 6*2, num_polygons) 

		# Flush the opengl rendering pipeline	
		glutSwapBuffers()	

	def mouseFunc(self, button, state, x, y):
		if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
			self.mouse_x = x
			self.mouse_y = y

			print(x, y)

	def keyboardFunc(self, key, x, y):
		if key == self.ESCAPE.encode():
			self.cleanUp()
		if key == 'a'.encode():
			self.camera.view_x += self.camera.view_speed
		if key == 'd'.encode():
			self.camera.view_x -= self.camera.view_speed
		if key == 's'.encode():
			self.camera.view_y += self.camera.view_speed
		if key == 'w'.encode():
			self.camera.view_y -= self.camera.view_speed
		if key == 'p'.encode():
			self.flag = 1

		glutPostRedisplay()

	def cleanUp(self):
		glDisableVertexAttribArray(self.shaders_template_loc)
		glDisableVertexAttribArray(self.shaders_position_loc)
		glDisableVertexAttribArray(self.shaders_color_loc)

		glDeleteBuffers(1, GLfloat(self.template_buffer))
		glDeleteBuffers(1, GLfloat(self.position_buffer))
		glDeleteBuffers(1, GLfloat(self.color_buffer))
		glDeleteProgram(self.shaders_programID)
		glutDestroyWindow(self.windowID)
		exit(0)
