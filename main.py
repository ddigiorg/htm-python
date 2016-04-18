# archlinux: certain opengl functions won't work on Windows without extensive tinkering
# python 3.5.1
# pyopengl 3.0 Mesa 11.1.2
# glsl 1.30

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import draw as draw

neurons_matrix = None
n_neurons_x = 2
n_neurons_y = 2
n_neurons_z = 2

colors_dict = {'inactive': [0.5, 0.5, 0.5],
			   'active'  : [0.0, 1.0, 0.0]}

flag = 0

def mainGL():
	global colors_dict
	global flag

	if flag == 0:
		neurons_matrix[0][0][0] = colors_dict['inactive']
		flag = 1
	else:	
		neurons_matrix[0][0][0] = colors_dict['active']
		flag = 0

	draw.updateCubes(neurons_matrix)
	draw.updateCamera()
	draw.updateScene()	

def main():
	global neurons_matrix, n_neurons_x, n_neurons_y, n_neurons_z
	draw.initGL()
	glutDisplayFunc(mainGL) # Register the drawing function with glut
	glutIdleFunc(mainGL)    # When doing nothing redraw scene
	neurons_matrix = draw.initCubes(n_neurons_x, n_neurons_y, n_neurons_z) #!!!make neurons_matrix the input
	draw.initShaders()
	draw.initCamera()
	draw.initVBOs()

	draw.runMainGLLoop()

main()
