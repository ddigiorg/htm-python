#archlinux: certain opengl functions won't work on Windows without extensive tinkering
#python 3.5.1
#pyopengl 3.1

# http://nehe.gamedev.net/tutorial/vertex_buffer_objects/22002/
# http://antongerdelan.net/opengl/vertexbuffers.html
# http://www.opengl-tutorial.org/beginners-tutorials/tutorial-4-a-colored-cube/
# https://www.opengl.org/wiki/Vertex_Specification_Best_Practices

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import cube as c

ESCAPE = '\x1b'

n_cubes_x = 20 # Typically 40 in HTM region
n_cubes_y = 10 # Typically 10 in HTM region
n_cubes_z = 20 # Typically 40 in HTM region
n_cubes   = n_cubes_x * n_cubes_y * n_cubes_z 
cubes = [[[None]*n_cubes_z]*n_cubes_y]*n_cubes_x
CUBE_SPACING = 4
CUBE_DATA_SIZE = 108*4

window = 0
width, height = 800, 600
aspect_ratio = width/height

x_camera_pos       = 0.0
y_camera_pos       = 0.0
z_camera_pos       = 10.0
yaw_camera_angle   = 0.0
pitch_camera_angle = 0.0
CAMERA_SPEED = 5.0
CAMERA_ANGLE = 10.0

vertex_position_buffer = None
vertex_position_data   = None
vertex_color_buffer    = None
vertex_color_data      = None
vertex_count           = None

color_flag = 0

update_colors = ((0, 0, 0, 'b'),
				 (0, 1, 0, 'b'),
				 (0, 2, 0, 'b'),
				 (0, 3, 0, 'b'),
				 (0, 4, 0, 'b'))

def init():
	initCubes()
	buildVBOs()

	glClearColor(0.0, 0.0, 0.0, 0.5)					# Black background
	glClearDepth(1.0)									# Depth Buffer setup
	glDepthFunc(GL_LESS)								# The type of Depth Testing
	glEnable (GL_DEPTH_TEST)							# Enable Depth Testing
	glShadeModel(GL_SMOOTH)								# Select Smooth Shading
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)	# Set Perspective Calculations to most accurate
#	glEnable(GL_TEXTURE_2D)								# Enable Texture Mapping
	glColor4f(1.0, 6.0, 6.0, 1.0)


def initCubes():
	global cubes, n_cubes_x, n_cubes_y, n_cubes_z, n_cubes, vertex_position_data, vertex_color_data, vertex_count

	# Initialize cube positions, opengl position data, and opengl color data
	position_list = []
	color_list    = []	
	for x in range(n_cubes_x):
		for y in range(n_cubes_y):
			for z in range(n_cubes_z):
				cubes[x][y][z] = c.Cube()
				cubes[x][y][z].setPosition(0 + x * -CUBE_SPACING, 
										   0 + y * -CUBE_SPACING,
										   0 + z * -CUBE_SPACING)
				position_list = position_list + cubes[x][y][z].getVertexPositions()
				color_list    = color_list    + cubes[x][y][z].getVertexColors()
	vertex_position_data = np.array(position_list, dtype='f')
	vertex_color_data    = np.array(color_list   , dtype='f')

	#vertex_count is n_cubes times  n_triangles_per_cube times n_vertices_per_triangle
	vertex_count = n_cubes*12*3

def buildVBOs():
	global vertex_position_buffer, vertex_position_data, vertex_color_buffer, vertex_color_data

	# Opengl vertex position buffer created, bound, filled with data, and set pointers to data
	vertex_position_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vertex_position_buffer)
	glBufferData(GL_ARRAY_BUFFER, vertex_position_data, GL_STATIC_DRAW)
	glVertexPointer(3, GL_FLOAT, 0, None)

	# Opengl vertex color buffer created, bound, filled with data, and set pointers to data
	vertex_color_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vertex_color_buffer)
	glBufferData(GL_ARRAY_BUFFER, vertex_color_data, GL_DYNAMIC_DRAW)
	glColorPointer(3, GL_FLOAT, 0, None)

def view():
	global x_camera_pos, y_camera_pos
	glTranslate(-x_camera_pos, -y_camera_pos, -z_camera_pos)
	glRotate(yaw_camera_angle, 0, 1, 0)
	glRotate(pitch_camera_angle, 1, 0, 0)


def drawVBOs():
	global vertex_position_buffer, vertex_color_buffer, vertex_color_data, vertex_count
	global color_flag, shit
	# Enable Vertex Arrays and Color Arrays
	glEnableClientState(GL_VERTEX_ARRAY)
	glEnableClientState(GL_COLOR_ARRAY)
	
	# Opengl vertex color buffer bound, filled with data, and set pointers to the data
	glBindBuffer(GL_ARRAY_BUFFER, vertex_color_buffer)
	
	if color_flag ==  1:
		for x, y, z, color in update_colors:
			cubes[x][y][z].setColor(color)
			offset = CUBE_DATA_SIZE * ( (x * n_cubes_y * n_cubes_z) + (y * n_cubes_z) + z)
			data = np.array(cubes[x][y][z].getVertexColors(), dtype='f')
			glBufferSubData(GL_ARRAY_BUFFER, offset, CUBE_DATA_SIZE, data)
		glColorPointer(3, GL_FLOAT, 0, None)
	
	# Render
	glDrawArrays(GL_TRIANGLES, 0, vertex_count)

	# Disable Vertex Arrays and Color Arrays
	glDisableClientState(GL_VERTEX_ARRAY)
	glDisableClientState(GL_COLOR_ARRAY)


def drawScene():
	global width, height

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glFrustum(-aspect_ratio, aspect_ratio, -1.0, 1.0, 1.0, 100.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()	

	view()
#	updateCubes()
	drawVBOs()

	# Flush the opengl rendering pipeline	
	glutSwapBuffers()	


def keyPressed(key, x, y):
	global x_camera_pos, y_camera_pos, z_camera_pos, yaw_camera_angle, pitch_camera_angle
	global color_flag
	if key == ESCAPE.encode():
		glutDestroyWindow(window)
		exit(0)
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


def main():
	global window
	# Initialize opengl
	glutInit()
	
	# Type of Display mode: RGBA color, double buffer, alpha components, depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)

	# Initialize window size
	glutInitWindowSize(width, height)

	# Window starts at upper left corner of screen
	glutInitWindowPosition(0, 0)

	# Create window with name "HTM"
	window = glutCreateWindow("HTM")

	# Register the drawing function with glut
	glutDisplayFunc(drawScene)

	#glutFillScreen()

	# When doing nothing redraw scene
	glutIdleFunc(drawScene)

	# Register the function called when the keyboard is pressed
	glutKeyboardFunc(keyPressed)
	glutSpecialFunc(keyPressed)

	# opengl initial setups
	init()

	# Start event processing engine
	glutMainLoop()


main()
