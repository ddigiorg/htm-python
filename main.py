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

colors_dict = {"inactive": [0.5, 0.5, 0.5], # Neuron inactive state
			   "active":   [0.0, 1.0, 0.0], # Neuron active (feed forward)
			   "predict":  [1.0, 0.0, 1.0]} # Neuron predictive state

# Cortex Global Variables
n_columns   = 2 # Number of columns per region
n_neurons   = 2 # Number of neurons per column
n_dendrites = 10 # Number of dendrites per neuron
n_synapses  = 5 # Number of synapses per dendrite

# Input Setup
n_inputs = 2
n_bits = 20
inputs = [None] * n_inputs
for i in range(2):
	inputs[i] = [0] * n_bits
inputs[0][0] = 1
inputs[0][1] = 1
inputs[0][2] = 1
inputs[0][3] = 1
inputs[0][4] = 1

inputs[1][5] = 1 
inputs[1][6] = 1
inputs[1][7] = 1
inputs[1][8] = 1
inputs[1][9] = 1

# OpenGL Global Variables
n_cells_x = n_columns # x axis for opengl
n_cells_y = n_neurons # y axis for opengl
n_cells_z = 1         # z axis for opengl

region_colors = np.array([[[ colors_dict["inactive"] ]*n_cells_z]*n_cells_y]*n_cells_x, dtype=np.float16)

def loop():
	global inputs, region, n_regions, n_columns, n_neurons, n_dendrites, n_synapses
	global n_cells_x, n_cells_y, n_cells_z, region_colors
	global colors_dict

#	for c in range(n_columns):
#		for n in range(n_neurons):
#			region_colors[c][n][0] = colors_dict["inactive"]
		
	draw.updatePolygons(region_colors, n_cells_x, n_cells_y, n_cells_z)
	draw.updateCamera()
	draw.updateScene(n_cells_x, n_cells_y, n_cells_z)

def main():
	global n_cells_x, n_cells_y, n_cells_z
	
	# Initialize opengl drawing
	draw.initGL()
	glutDisplayFunc(loop) # Register the drawing function with glut
	glutIdleFunc(loop)    # When doing nothing redraw scene
	draw.initDrawPolygons(n_cells_x, n_cells_y, n_cells_z)
	draw.initShaders()
	draw.initCamera()
	draw.initVBOs()
	draw.runMainGLLoop()

main()
