# archlinux: certain opengl functions won't work on Windows without extensive tinkering
# python 3.5.1
# pyopengl 3.0 Mesa 11.1.2
# glsl 1.30

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import random as rand
import draw as draw

colors_dict = {'inactive': [0.5, 0.5, 0.5],
			   'active'  : [0.0, 1.0, 0.0],
			   'predict' : [1.0, 0.0, 1.0]}

# Input Setup
n_inputs_x = 5
n_inputs_z = 5
n_inputs = n_inputs_x * n_inputs_z
inputs = np.array([0]*n_inputs, dtype=np.int8)

# HTM Region Setup
n_neurons_x = 20
n_neurons_y = 5
n_neurons_z = 20
region_colors = np.array([[[ colors_dict['inactive'] ]*n_neurons_z]*n_neurons_y]*n_neurons_x, dtype=np.float16)

flag = 0

columns_potential_pool = np.array([[0]*n_neurons_z]*n_neurons_x)

#for x in range(n_neurons_x):
#	for z in range(n_neurons_z):
#print(list(range(n_inputs)))
#for i in rand.sample(range(n_inputs), int(n_inputs*0.5)):
#	print(i)
		#columns_potential_pool[x][z] = rand.sample

def mainGL():
	global n_neurons_x, n_neurons_y, n_neurons_z, region_colors
	global colors_dict
	global flag

	if flag == 0:
		for y in range(n_neurons_y):
			region_colors[0][y][0] = colors_dict['inactive']
			region_colors[1][y][0] = colors_dict['inactive']
		flag = 1
	else:	
		for y in range(n_neurons_y):
			region_colors[0][y][0] = colors_dict['active']
			region_colors[1][y][0] = colors_dict['predict']
		flag = 0

	draw.updateCubes(region_colors)
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
