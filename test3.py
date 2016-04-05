#archlinux: certain opengl functions won't work on Windows without extensive tinkering
#python 3.5.1
#pyopengl 3.1

# http://nehe.gamedev.net/tutorial/vertex_buffer_objects/22002/
# http://antongerdelan.net/opengl/vertexbuffers.html


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import cube as c

ESCAPE = '\x1b'

cubes = [c.Cube() for i in range(2)]
cubes[0].setPosition((0, 0, 0))
cubes[0].setColor('b')
cubes[1].setPosition((4, 0, 0))
cubes[1].setColor('g')

window = 0
width, height = 800, 600
aspect_ratio = width/height

x_camera_pos = 0.0
y_camera_pos = 0.0
z_camera_pos = 5.0
CAMERA_SPEED = 1.0

vbo_buffer = None
vertex_count = None

def init():
	buildVBOs()

	glClearColor(0.0, 0.0, 0.0, 0.5)					# Black background
	glClearDepth(1.0)									# Depth Buffer setup
	glDepthFunc(GL_LEQUAL)								# The type of Depth Testing
	glEnable (GL_DEPTH_TEST)							# Enable Depth Testing
	glShadeModel(GL_SMOOTH)								# Select Smooth Shading
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)	# Set Perspective Calculations to most accurate
#	glEnable(GL_TEXTURE_2D)								# Enable Texture Mapping
	glColor4f(1.0, 6.0, 6.0, 1.0)

def view():
	global x_camera_pos, y_camera_pos
	glTranslate(-x_camera_pos, -y_camera_pos, -z_camera_pos)


def drawCubes():
	global cubes
	glBegin(GL_QUADS)
	for cube in cubes:
		glColor3fv(cube.getColor())
		for surface in cube.getSurfaces():
			for vertex in surface:
				glVertex3fv(cube.getVertices()[vertex])
	glEnd()

def buildVBOs():
	global vbo_buffer, vertex_count
	vertices = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0], dtype='f')
	vertex_count = 3 

	vbo_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vbo_buffer)
	glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)


def drawVBOs():
	global vbo_buffer, vertex_count
	
	# Enable Vertex Arrays
	glEnableClientState(GL_VERTEX_ARRAY)
	
	# Set pointers to the data
	glBindBuffer(GL_ARRAY_BUFFER, vbo_buffer)
	glVertexPointer(3, GL_FLOAT, 0, None)
	
	# Render
	glDrawArrays(GL_TRIANGLES, 0, vertex_count)

	# Disable Vertex Arrays
	glDisableClientState(GL_VERTEX_ARRAY)


def drawScene():
	global width, height

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glFrustum(-aspect_ratio, aspect_ratio, -1.0, 1.0, 1.0, 100.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()	

	view()
#	drawCubes()
	drawVBOs()

	# Flush the opengl rendering pipeline	
	glutSwapBuffers()	


def keyPressed(key, x, y):
	global x_camera_pos, y_camera_pos, z_camera_pos
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
