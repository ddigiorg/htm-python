# graphics.py

#MAKE THIS ENTIRE CODE A CLASS INSTEAD OF USING GLOBAL VARIABLES

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import shader as shader

# openGL application global variables
windowID = 0
width, height = 800, 600

# Shader global variables
shaders_programID      = None
shaders_projection_loc = None
shaders_view_loc       = None
shaders_template_loc   = None
shaders_position_loc   = None
shaders_color_loc      = None

# View global variables
ortho_matrix = None
view_matrix  = None
view_x = -4.0
view_y = 0.0
view_z = 2.0
VIEW_SPEED = 0.5

# Polygon global variables
POLY_SPACING = 0.5

# VBO global variables
template_buffer  = None
position_buffer  = None
color_buffer     = None
template_data    = None
position_data    = None
VERTEX_SIZE      = 2 # xy value per vertex for template
POSITION_SIZE    = 2 # xy value per vertex for position
COLOR_SIZE       = 3 # rgb value per vertex for color

# Keyboard global variables
ESCAPE = '\x1b'

def gInit():
	global windowID

	glutInit()								# Initialize opengl
	glutInitDisplayMode(GLUT_RGBA)          # RGBA color
	glutInitWindowSize(width, height)		# Initialize windowID size
	glutInitWindowPosition(0, 0)			# Application windowID placed at upper left corner of monitor screen
	windowID = glutCreateWindow("HTM")		# Create windowID with name "HTM"
	glutKeyboardFunc(gKeyPressed)			# Register function when keyboard pressed
	glutSpecialFunc(gKeyPressed)				# Register function when keyboard pressed
	glClearColor(0.0, 0.0, 0.0, 1.0)		# Black background


def gInitShaders():
	global shaders_programID, shaders_template_loc, shaders_position_loc, shaders_color_loc, shaders_projection_loc, shaders_view_loc

	vertex_shader   = shader.compile_shader("VS")
	fragment_shader = shader.compile_shader("FS")
	shaders_programID = shader.link_shader_program(vertex_shader, fragment_shader)     

	shaders_template_loc   = glGetAttribLocation(shaders_programID, "templateVS")
	shaders_position_loc   = glGetAttribLocation(shaders_programID, "positionVS")
	shaders_color_loc      = glGetAttribLocation(shaders_programID, "colorVS")
	shaders_projection_loc = glGetUniformLocation(shaders_programID, "projection")
	shaders_view_loc       = glGetUniformLocation(shaders_programID, "view" )


def gInitView():
	global width, height, ortho_matrix

	l = 0.0
	r = width/100
	t = height/100
	b = 0.0
	f = -1.0
	n = 1.0

	ortho_matrix = [2.0/(r-l),    0.0,          0.0,          0.0,
                    0.0,          2.0/(t-b),    0.0,          0.0,
                    0,0,          0.0,          -2.0/(f-n),   0.0,
                    -(r+l)/(r-l), -(t+b)/(t-b), -(f+n)/(f-n), 1.0]


def gInitPolygons(n_polys_x, n_polys_y):
	global template_data, position_data

	n_polys = n_polys_x * n_polys_y

	template_list = [
		-0.5,  0.5, 
		-0.5, -0.5, 
		 0.5, -0.5,

		 0.5,  0.5,
		-0.5,  0.5, 
		 0.5, -0.5]

#	position_list = [0] * n_polys * POSITION_SIZE
#	
#	i = 0
#	for x in range(n_polys_x):
#		for y in range(n_polys_y):	
#			position_list[i*POSITION_SIZE  ] = 0.0 + x * (1.0 + POLY_SPACING) # vertex x world position
#			position_list[i*POSITION_SIZE+1] = 0.0 + y * (1.0 + POLY_SPACING) # vertex y world position
#			i += 1
#
	template_data = np.array(template_list, dtype=np.float16)
#	position_data = np.array(position_list, dtype=np.float16)


def gInitVBOs():
	global template_buffer, position_buffer, color_buffer, template_data, position_data
	global shaders_programID, shaders_template_loc, shaders_position_loc
   
	# Get shader ID
	glUseProgram(shaders_programID)
   
	# Opengl VBO vertex template buffer created, bound, filled with vertex template data, and updated
	template_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, template_buffer)
	glBufferData(GL_ARRAY_BUFFER, template_data, GL_STATIC_DRAW)
	glEnableVertexAttribArray(shaders_template_loc)
	glVertexAttribPointer(shaders_template_loc, VERTEX_SIZE, GL_HALF_FLOAT, False, 0, None)

	# Opengl VBO polygon position buffer created, bound, and left empty
	position_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, position_buffer)
	glBufferData(GL_ARRAY_BUFFER, None, GL_STATIC_DRAW)

	# Opengl VBO polygon color buffer created, bound, and left empty
	color_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
	glBufferData(GL_ARRAY_BUFFER, None, GL_STREAM_DRAW)


def gUpdateView():
	global view_matrix

	view_matrix = [1.0,    0.0,    0.0,    0.0,
				   0.0,    1.0,    0.0,    0.0,
				   0.0,    0.0,    1.0,    0.0,
				   view_x, view_y, view_z, 1.0]

def gUpdatePolygonPositions(in_positions):
	n_polys_x = len(in_positions)
	n_polys_y = len(in_positions[0])

	position_list = [0] * n_polys_x * n_polys_y * POSITION_SIZE
	
	i = 0
	for x in range(n_polys_x):
		for y in range(n_polys_y):	
			position_list[i*POSITION_SIZE  ] = in_positions[x][y][0] # polygon x world position
			position_list[i*POSITION_SIZE+1] = in_positions[x][y][1] # polygon y world position
			i += 1

	position_data = np.array(position_list, dtype=np.float16)

	# Opengl VBO polygon position buffer bound, and filled with cell position data, and updated
	glBindBuffer(GL_ARRAY_BUFFER, position_buffer)
	glBufferData(GL_ARRAY_BUFFER, position_data, GL_STATIC_DRAW)
	glEnableVertexAttribArray(shaders_position_loc)
	glVertexAttribPointer(shaders_position_loc, POSITION_SIZE, GL_HALF_FLOAT, False, 0, None)


def gUpdatePolygonColors(in_colors):
	n_polys_x = len(in_colors)
	n_polys_y = len(in_colors[0])

	color_list = [0] * n_polys_x * n_polys_y * COLOR_SIZE

	i = 0
	for x in range(n_polys_x):
		for y in range(n_polys_y):	
			color_list[i*COLOR_SIZE  ] = in_colors[x][y][0] # polygon r color
			color_list[i*COLOR_SIZE+1] = in_colors[x][y][1] # polygon g color
			color_list[i*COLOR_SIZE+2] = in_colors[x][y][2] # polygon b color
			i += 1
	
	color_data = np.array(color_list, dtype=np.float16)

	# Opengl VBO cell color buffer bound, filled with data, and shader variable updated
	glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
	glBufferData(GL_ARRAY_BUFFER, color_data, GL_STREAM_DRAW)
	glEnableVertexAttribArray(shaders_color_loc)
	glVertexAttribPointer(shaders_color_loc, COLOR_SIZE, GL_HALF_FLOAT, True, 0, None) # normalized for unsigned char


def gUpdateScene(n_polys_x, n_polys_y):
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	# Update shader with orthographic and view matrix
	glUniformMatrix4fv(shaders_projection_loc, 1, False, ortho_matrix)
	glUniformMatrix4fv(shaders_view_loc, 1, False, view_matrix)

	# * ?????????? For instancing... figure out what this does
	glVertexAttribDivisor(0, 0)
	glVertexAttribDivisor(1, 1)
	glVertexAttribDivisor(2, 1)

	# Draw cells
	n_polys = n_polys_x * n_polys_y
	glDrawArraysInstanced(GL_TRIANGLES, 0, 6*2, n_polys) # 6 vertices per triangle, 2 triangles per square 
	
	# Flush the opengl rendering pipeline	
	glutSwapBuffers()	

def gKeyPressed(key, x, y):
	global view_x, view_y, view_z 
	if key == ESCAPE.encode():
		gCleanup()
	if key == 'a'.encode():
		view_x += VIEW_SPEED
	if key == 'd'.encode():
		view_x -= VIEW_SPEED
	if key == 'q'.encode():
		view_y += VIEW_SPEED
	if key == 'e'.encode():
		view_y -= VIEW_SPEED
	if key == 's'.encode():
		view_z += VIEW_SPEED
	if key == 'w'.encode():
		view_z -= VIEW_SPEED
	glutPostRedisplay()

def gCleanup():
	global windowID
	global template_buffer, position_buffer, color_buffer
	global shaders_programID, shaders_template_loc, shaders_position_loc

	glDisableVertexAttribArray(shaders_template_loc)
	glDisableVertexAttribArray(shaders_position_loc)
	glDisableVertexAttribArray(shaders_color_loc)

	glDeleteBuffers(1, GLfloat(template_buffer))
	glDeleteBuffers(1, GLfloat(position_buffer))
	glDeleteBuffers(1, GLfloat(color_buffer))
	glDeleteProgram(shaders_programID)
	glutDestroyWindow(windowID)
	exit(0)

def gRunMainGLLoop():
	glutMainLoop() # Start event processing engine
