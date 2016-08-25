# graphics.py
# http://stackoverflow.com/questions/166356/what-are-some-best-practices-for-opengl-coding-esp-w-r-t-object-orientation

from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import shader as shader

class Render(object):
	def __init__(self, window_width, window_height, arrays):
		self.scene = Scene(arrays)
		self.camera = Camera(window_width, window_height)
		self.oglRenderer = OpenGLRenderer(window_width, window_height)

		self.ESCAPE = '\x1b'
		self.flag = 1
		glutMouseFunc(self.mouseFunc)       # Register function when mouse input recieved
		glutKeyboardFunc(self.keyboardFunc) # Register function when keyboard pressed
		glutSpecialFunc(self.keyboardFunc)  # Register function when keyboard pressed

	def mouseFunc(self, button, state, x, y):
		if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
			camera   = self.camera
			scene    = self.scene
			polygons = scene.polygons[1]

			selected = False
			for polygon in polygons:
				lower_x = polygon.position[0] + camera.view_x
				upper_x = lower_x + polygon.size
				lower_y = polygon.position[1] + camera.view_y
				upper_y = lower_y + polygon.size

				if lower_x <= x <= upper_x and lower_y <= y <= upper_y:
					scene.selected_polygon = polygon
					selected = True

			if not selected:
				scene.selected_polygon = None

	def keyboardFunc(self, key, x, y):
		camera = self.camera
		oglRenderer = self.oglRenderer

		if key == self.ESCAPE.encode():
			oglRenderer.cleanUp()
		if key == 'a'.encode():
			camera.view_x += camera.view_speed
		if key == 'd'.encode():
			camera.view_x -= camera.view_speed
		if key == 'w'.encode():
			camera.view_y += camera.view_speed
		if key == 's'.encode():
			camera.view_y -= camera.view_speed
		if key == 'p'.encode():
			self.flag = 1

		glutPostRedisplay()

	def load(self):
		camera = self.camera
		scene  = self.scene
		oglRenderer = self.oglRenderer

		proj_matrix   = camera.initOrthographicProjection()
		template_list = scene.polygonTemplate()
		position_list = scene.polygonPositions()

		oglRenderer.updateProjectionMatrix(proj_matrix)
		oglRenderer.updateTemplateVBO(template_list)
		oglRenderer.updatePositionVBO(position_list)
		 
	def load2(self, stuff):
		camera = self.camera
		scene  = self.scene
		oglRenderer = self.oglRenderer

		view_matrix = camera.updateView()
		color_list  = scene.polygonColors(stuff) # MAKE BETTER

		oglRenderer.updateViewMatrix(view_matrix)
		oglRenderer.updateColorVBO(color_list)

		oglRenderer.drawScene( int(len(color_list)/3) )


class Square(object):
	def __init__(self, start_x, start_y, idx_x, idx_y, size, spacing):
		self.idx_x = idx_x
		self.idx_y = idx_y
		self.start_x = start_x
		self.start_y = start_y
		self.size = size

		self.shape = [0, size, 0, 0, size, 0, size, size, 0, size, size, 0]

		self.position = [start_x + idx_x * (size + spacing), # x in pixels
                         start_y + idx_y * (size + spacing)] # y in pixels

		self.color = [0.0, 0.0, 0.0] #rgb


class Scene(object):
	def __init__(self, arrays):
		MAX_NUM_POLYS_X = 70

		self.polygons = []

		self.selected_polygon = None

		for array in arrays:
			start_x = array[0]
			start_y = array[1]
			num_x   = array[2]
			num_y   = array[3]
			size    = array[4]
			spacing = array[5]

			if num_x > MAX_NUM_POLYS_X:
				num_x = MAX_NUM_POLYS_X

			self.polygons.append([Square(start_x, start_y, idx_x, idx_y, size, spacing)
                                  for idx_x in range(num_x)
                                  for idx_y in range(num_y)])

	def polygonTemplate(self):
		return self.polygons[0][0].shape

	def polygonPositions(self):
		position_list = []
		for polygons in self.polygons:
			for polygon in polygons:
				position_list += polygon.position

		return position_list

	def polygonColors(self, stuff):
		inputs = stuff[0]
		layer = stuff[1]

		active_neurons  = [active_neuron  for active_neuron  in layer.active_neurons  if active_neuron.idx  < len(self.polygons[1]) ]
		winner_neurons  = [winner_neuron  for winner_neuron  in layer.winner_neurons  if winner_neuron.idx  < len(self.polygons[1]) ]
		predict_neurons = [predict_neuron for predict_neuron in layer.predict_neurons if predict_neuron.idx < len(self.polygons[1]) ]

		color_list = []

		for polygon in self.polygons[0]:
			if inputs[polygon.idx_x] == 1:
				polygon.color = [0.0, 0.8, 0.0] # Active (Green)
			else:
				polygon.color = [0.2, 0.2, 0.2] # Inactive (Grey)
			color_list += polygon.color

		for polygon in self.polygons[1]:
			polygon.color = [0.2, 0.2, 0.2]
		
		for active_neuron in active_neurons:
			self.polygons[1][active_neuron.idx].color = [0.0, 0.8, 0.0] # Active (Green)

		for winner_neuron in winner_neurons:
			self.polygons[1][winner_neuron.idx].color = [0.0, 0.0, 0.8] # Winner (Blue) 

		for predict_neuron in predict_neurons:
			self.polygons[1][predict_neuron.idx].color = [0.8, 0.0, 0.8] # Predict (Violet) 

		selected_polygon = self.selected_polygon
		if selected_polygon:
			#selected_polygon.color[0] += 0.2
			#selected_polygon.color[1] += 0.2
			#selected_polygon.color[2] += 0.2
			idx_x = selected_polygon.idx_x
			idx_y = selected_polygon.idx_y
			neuron = layer.columns[idx_x].neurons[idx_y]
			synapses = [basal_dendrite.synapse_addresses for basal_dendrite in neuron.basal_dendrites]
			print(synapses)
			self.selected_polygon = None

		for polygon in self.polygons[1]:
			color_list += polygon.color

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
		"""Initialize 2D projection with top left pixel as origin"""

		l =  0.0
		r =  self.window_width
		b =  self.window_height
		t =  0.0
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
	def __init__(self, window_width, window_height):
		# Opengl Initilization
		glutInit()                                      # Initialize opengl
		glutInitDisplayMode(GLUT_RGBA)                  # RGBA color
		glutInitWindowSize(window_width, window_height) # Initialize window size
		glutInitWindowPosition(0, 0)                    # Application window placed at upper left corner of monitor screen
		self.windowID = glutCreateWindow("HTM Test")    # Create windowID with name
		glClearColor(0.0, 0.0, 0.0, 1.0)                # Black background

		# VBO variables
		self.template_buffer = glGenBuffers(1)
		self.position_buffer = glGenBuffers(1)
		self.color_buffer    = glGenBuffers(1)

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
