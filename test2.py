#archlinux: certain opengl functions won't work on Windows without extensive tinkering
#python 3.5.1
#pyopengl 3.1


#http://noobtuts.com/python/opengl-introduction
#http://relativity.net.au/gaming/java/Frustum.html
#http://nehe.gamedev.net/article/replacement_for_gluperspective/21002/
#http://carloluchessa.blogspot.com/2012/09/simple-viewer-in-pyopengl.html

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import cube as c

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
z_camera_pos = 20.0
CAMERA_SPEED = 2.0


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


def display():
	global width, height

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glFrustum(-aspect_ratio, aspect_ratio, -1.0, 1.0, 10.0, 200.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()	

	view()
	drawCubes()
	
	glutSwapBuffers()	


def keyboard(key, x, y):
	global x_camera_pos, y_camera_pos, z_camera_pos
	if key == '\x1b'.encode():
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


# opengl initialization
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
window = glutCreateWindow("HTM")
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()
