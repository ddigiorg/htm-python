from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cube as c

cubes = [c.Cube()]
cubes[0].setPosition((0,0,0))
cubes[0].setColor('b')

window = 0                                             # glut window number
width, height = 800, 600                               # window size

def display():
	global cubes
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glTranslatef(0.0, 0.0, -3.0)

	glBegin(GL_QUADS)
	for cube in cubes:
		glColor3fv(cube.getColor())
		for surface in cube.getSurfaces():
			for vertex in surface:
				glVertex3fv(cube.getVertices()[vertex])
	glEnd()
	
	glutSwapBuffers()	

def keyboard(key, x, y):
	if key=='\033':
		sys.exit()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
window = glutCreateWindow("HTM")
glutDisplayFunc(display)
#glutIdleFunc(display)
glutKeyboardFunc(keyboard)

glClearDepth(1.0)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LEQUAL)


glutMainLoop()


