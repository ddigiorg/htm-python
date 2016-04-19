# archlinux: certain opengl functions won't work on Windows without extensive tinkering
# python 3.5.1
# pyopengl 3.0 Mesa 11.1.2
# glsl 1.30

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import draw as draw

colors_dict = {'inactive': [0.5, 0.5, 0.5],
			   'active'  : [0.0, 1.0, 0.0],
			   'predict' : [1.0, 0.0, 1.0]}

n_neurons_x = 20
n_neurons_y = 5
n_neurons_z = 20
neurons_matrix = np.array([[[ colors_dict['inactive'] ]*n_neurons_z]*n_neurons_y]*n_neurons_x, dtype=np.float16)

flag = 0

def mainGL():
	global n_neurons_x, n_neurons_y, n_neurons_z, neurons_matrix
	global colors_dict
	global flag

	if flag == 0:
		for y in range(n_neurons_y):
			neurons_matrix[0][y][0] = colors_dict['inactive']
			neurons_matrix[1][y][0] = colors_dict['inactive']
		flag = 1
	else:	
		for y in range(n_neurons_y):
			neurons_matrix[0][y][0] = colors_dict['active']
			neurons_matrix[1][y][0] = colors_dict['predict']
		flag = 0

	draw.updateCubes(neurons_matrix)
	draw.updateCamera()
	draw.updateScene()

def main():
	global neurons_matrix, n_neurons_x, n_neurons_y, n_neurons_z
	draw.initGL()
	glutDisplayFunc(mainGL) # Register the drawing function with glut
	glutIdleFunc(mainGL)    # When doing nothing redraw scene
	draw.initCubes(n_neurons_x, n_neurons_y, n_neurons_z)
	draw.initShaders()
	draw.initCamera()
	draw.initVBOs()
	draw.runMainGLLoop()

main()
