# archlinux: certain opengl functions won't work on Windows without extensive tinkering
# python 3.5.1
# pyopengl 3.1 (3.0 Mesa 11.1.2)
# glsl 1.30

# *NOTE: CHECK IF APPLICABLE
# http://www.opengl-tutorial.org/intermediate-tutorials/billboards-particles/particles-instancing/
# https://github.com/opengl-tutorials/ogl/blob/master/tutorial18_billboards_and_particles/tutorial18_particles.cpp

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import cube as cube
import shader as shader

# Main global variables
window = 0
width, height = 800, 600
aspect_ratio = width/height

# Cube global variables
n_cubes_x    = None
n_cubes_y    = None
n_cubes_z    = None
n_cubes      = None
cubes_region = None

# Camera global variables
CAMERA_SPEED       = 5.0
CAMERA_ANGLE       = 10.0
x_camera_pos       = 0.0
y_camera_pos       = 0.0
z_camera_pos       = 10.0
yaw_camera_angle   = 0.0
pitch_camera_angle = 0.0

# Shader global variables
shaders_program        = None

# VBO global variables
vertex_template_buffer = None
cubes_position_buffer  = None
cubes_color_buffer     = None
cubes_template_data    = None
cubes_position_data    = None
cubes_color_data       = None

# Keyboard global variables
ESCAPE = '\x1b'
color_flag = 0

def initShaders():
	global shaders_program
	vertex_shader   = shader.compile_shader("vertex")
	fragment_shader = shader.compile_shader("fragment")
	shaders_program = shader.link_shader_program(vertex_shader, fragment_shader)     

def initCubes():
	global n_cubes_x, n_cubes_y, n_cubes_z, n_cubes, cubes_region, vertex_template_data, cubes_position_data, cubes_color_data

	CUBE_POSITION_DATA_SIZE = 3
	CUBE_COLOR_DATA_SIZE = 4
	CUBE_SPACING = 4
	n_cubes_x = 20 # Typically 40 in HTM region
	n_cubes_y = 10 # Typically 10 in HTM region
	n_cubes_z = 20 # Typically 40 in HTM region
	n_cubes   = n_cubes_x * n_cubes_y * n_cubes_z
	cubes_region = [[[None]*n_cubes_z]*n_cubes_y]*n_cubes_x

	position_list = [0] * n_cubes * CUBE_POSITION_DATA_SIZE
	color_list = [0] * n_cubes * CUBE_COLOR_DATA_SIZE

	for x, y, z in np.nindex(n_cubes_x, n_cubes_y, n_cubes_z):
		i = ((x * n_cubes_y * n_cubes_z) + (y * n_cubes_z) + z)
		cubes[x][y][z] = cube.Cube()
		cubes[x][y][z].setPosition(0 + x * -CUBE_SPACING, 0 + y * -CUBE_SPACING, 0 + z * -CUBE_SPACING)
		position_list[i  ] = cubes[x][y][z].getPosition()[0] # x position
		position_list[i+1] = cubes[x][y][z].getPosition()[1] # y position
		position_list[i+2] = cubes[x][y][z].getPosition()[2] # z position
		color_list[i  ] = cubes[x][y][z].getColor()[0] # r color
		color_list[i+1] = cubes[x][y][z].getColor()[1] # g color
		color_list[i+2] = cubes[x][y][z].getColor()[2] # b color
		color_list[i+3] = cubes[x][y][z].getColor()[3] # a color

	vertex_template_data = np.array(cube.getVertexTemplate(), dtype='f')
	cubes_position_data = np.array(position_list, dtype='f')
	cubes_color_data = np.array(position_list, dtype='f')

def initVBOs():
	global vertex_template_buffer, cubes_position_buffer, cubes_color_buffer, cubes_template_data
      
	# Opengl VBO vertex template buffer created, bound, and filled with data
	vertex_template_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vertex_template_buffer)
	glBufferData(GL_ARRAY_BUFFER, vertex_template_data, GL_STATIC_DRAW)

	# Opengl VBO cube position buffer created, bound, and left empty
	cubes_position_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, cubes_position_buffer)
	glBufferData(GL_ARRAY_BUFFER, None, GL_STREAM_DRAW) # cubes_position_data   GL_STATIC_DRAW

	# Opengl VBO cube color buffer created, bound, and left empty
	cubes_color_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, cubes_color_buffer)
	glBufferData(GL_ARRAY_BUFFER, None, GL_STREAM_DRAW) #cubes_color_data

def updateCubes():
	global cubes
	global color_flag

	if color_flag > 0:
		cubes[0][0][0].setColor(0, 0, 1, 1)
                
def updateVBOs():
	global n_cubes, shaders_program, cubes_position_buffer, cubes_color_buffer, cubes_position_data, cubes_color_data

	# Opengl VBO cube position buffer bound, "orphaned", and filled with data
	glBindBuffer(GL_ARRAY_BUFFER, cubes_position_buffer)
	glBufferData(GL_ARRAY_BUFFER, None, GL_STREAM_DRAW)
	glBufferSubData(GL_ARRAY_BUFFER, 0, n_cubes * len(GLfloat) * 4, cubes_position_data)

	# Opengl VBO cube color buffer bound, "orphaned", and filled with data
	glBindBuffer(GL_ARRAY_BUFFER, cubes_color_buffer)
	glBufferData(GL_ARRAY_BUFFER, None, GL_STREAM_DRAW)
	glBufferSubData(GL_ARRAY_BUFFER, 0, n_cubes * len(GLfloat) * 4, cubes_color_data)

	glUseProgram(shaders_program)

	# 1st attribute buffer: vertices template
	glEnableVertexAttribArray(0)
	glBindBuffer(GL_ARRAY_BUFFER, vertex_template_buffer) # *
	glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

	# 2nd attribute buffer: cube positions
	glEnableVertexAttribArray(1)
	glBindBuffer(GL_ARRAY_BUFFER, cubes_position_buffer) # *
	glVertexAttribPointer(1, 3, GL_FLOAT, False, 0, None) # xyz

	# 3rd attribute buffer: cube colors
	glEnableVertexAttribArray(2)
	glBindBuffer(GL_ARRAY_BUFFER, cubes_color_buffer) # *
	glVertexAttribPointer(2, 4, GL_FLOAT, True, 0, None) # rgba, normalized for unsigned char

	# * ??????????
	glVertexAttribDivisor(0, 0)
	glVertexAttribDivisor(1, 1)
	glVertexAttribDivisor(2, 1)

	# Draw cubes
	glDrawArraysInstanced(GL_TRIANGLES, 0, 4, n_cubes) # GL_TRIANGLE_STRIP

	glDisableVertexAttribArray(0)
	glDisableVertexAttribArray(1)
	glDisableVertexAttribArray(2)

def view():
	global x_camera_pos, y_camera_pos
	glTranslate(-x_camera_pos, -y_camera_pos, -z_camera_pos)
	glRotate(yaw_camera_angle, 0, 1, 0)
	glRotate(pitch_camera_angle, 1, 0, 0)

def drawScene():
	global width, height

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glFrustum(-aspect_ratio, aspect_ratio, -1.0, 1.0, 1.0, 100.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()	

	view()
	#updateCubes()
	updateVBOs()

	# Flush the opengl rendering pipeline	
	glutSwapBuffers()	

def keyPressed(key, x, y):
	global x_camera_pos, y_camera_pos, z_camera_pos, yaw_camera_angle, pitch_camera_angle
	global color_flag
	if key == ESCAPE.encode():
		cleanup()
	if key == 'd'.encode():
		x_camera_pos += CAMERA_SPEED
	if key == 'a'.encode():
		x_camera_pos -= CAMERA_SPEED
	if key == 'e'.encode():
		y_camera_pos += CAMERA_SPEED
	if key == 'q'.encode():
		y_camera_pos -= CAMERA_SPEED
	if key == 's'.encode():
		z_camera_pos += CAMERA_SPEED
	if key == 'w'.encode():
		z_camera_pos -= CAMERA_SPEED
	if key == GLUT_KEY_LEFT:
		yaw_camera_angle += CAMERA_ANGLE
	if key == GLUT_KEY_RIGHT:
		yaw_camera_angle -= CAMERA_ANGLE
	if key == GLUT_KEY_UP:
		pitch_camera_angle += CAMERA_ANGLE
	if key == GLUT_KEY_DOWN:
		pitch_camera_angle -= CAMERA_ANGLE
	if key == 'p'.encode():
		color_flag = 1
	glutPostRedisplay()

def cleanup():
	global shaders_program, vertex_template_buffer, cubes_position_buffer, cubes_color_buffer
	glDeleteBuffers(1, cubes_color_buffer)
	glDeleteBuffers(1, cubes_position_buffer)
	glDeleteBuffers(1, vertex_template_buffer)
	glDeleteProgram(shaders_program)
# *	glDeleteVertexArrays(1, &VertexArrayID)
	glutDestroyWindow(window)
	exit(0)

def main():
	global window
	
	glutInit()								# Initialize opengl
	glutInitDisplayMode(GLUT_RGBA   |		# RGBA color
						GLUT_DOUBLE |		# *Double Buffer
						GLUT_ALPHA  |		# Alpha Components
						GLUT_DEPTH)  		# Depth Buffer
	glutInitWindowSize(width, height)		# Initialize window size
	glutInitWindowPosition(0, 0)			# Window at upper left corner of screen
	window = glutCreateWindow("HTM")		# Create window with name "HTM"
	glutDisplayFunc(drawScene)				# Register the drawing function with glut
	glutIdleFunc(drawScene)					# *When doing nothing redraw scene
	glutKeyboardFunc(keyPressed)			# Register function when keyboard pressed
	glutSpecialFunc(keyPressed)				# Register function when keyboard pressed
	glClearColor(0.0, 0.0, 0.0, 1.0)		# Black background
	glClearDepth(1.0)						# Depth Buffer setup
	glDepthFunc(GL_LESS)					# The type of Depth Testing
	glEnable (GL_DEPTH_TEST)				# Enable Depth Testing
	glShadeModel(GL_SMOOTH)					# Select Smooth Shading
	glHint(GL_PERSPECTIVE_CORRECTION_HINT,
               GL_NICEST)	                # *Set Perspective Calculations to most accurate
	glColor4f(1.0, 6.0, 6.0, 1.0)			# *FIGURE OUT WHAT THIS DOES
	initShaders()
	initCubes()
	initVBOs()
	glutMainLoop()                          # Start event processing engine

main()
