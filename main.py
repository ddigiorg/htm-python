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
import cortex as cortex

colors_dict = {0: [0.5, 0.5, 0.5], # Neuron inactive state
			   1: [0.0, 1.0, 0.0], # Neuron active (feed forward)
			   2: [1.0, 0.0, 1.0]} # Neuron predictive state

# Cortex Global Variables
n_regions   = 1 # Number of regions per cortex
n_columns   = 10 # Number of columns per region
n_neurons   = 5 # Number of neurons per column
n_dendrites = 1 # Number of dendrites per neuron
n_synapses  = 5 # Number of synapses per dendrite
region   = None

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

inputs[1][1] = 1 
inputs[1][2] = 1
inputs[1][3] = 1
inputs[1][4] = 1
inputs[1][5] = 1

# OpenGL Global Variables
n_x = n_columns # x axis for opengl
n_y = n_neurons # y axis for opengl
n_z = 1         # z axis for opengl

region_colors = np.array([[[ colors_dict[0] ]*n_z]*n_y]*n_x, dtype=np.float16)

flag = 0

def loop():
	global inputs, region, n_regions, n_columns, n_neurons, n_dendrites, n_synapses
	global n_x, n_y, n_z, region_colors
	global colors_dict
	global flag

	if flag == 0:
		temp = inputs[0]
		flag = 1
	elif flag == 1:
		temp = inputs[1]
		flag = 0

	active_columns_addresses = cortex.runSpatialPooler(temp, region)
	cortex.runTemporalPooler(active_columns_addresses, region)

	for c in range(n_columns):
		for n in range(n_neurons):
			axon = region.getColumns()[c].getNeurons()[n].getAxon()
			region_colors[c][n][0] = colors_dict[axon]
		
	draw.updateCubes(region_colors)
	draw.updateCamera()
	draw.updateScene()

def main():
	global inputs, region, n_regions, n_columns, n_neurons, n_dendrites, n_synapses
	global n_x, n_y, n_z
	
	# Initialize cortex
	region = cortex.initRegion(inputs[0], n_columns, n_neurons, n_dendrites, n_synapses)
	region = cortex.initConnections(inputs[0], region)


	'''	
	print("inputs: {}".format(inputs))
	for i in range(5):
		print("ITERATION: {}".format(i))
		cortex.runSpatialPooler(inputs, neocortex)
	'''

	# Initialize opengl drawing
	draw.initGL()
	glutDisplayFunc(loop) # Register the drawing function with glut
	glutIdleFunc(loop)    # When doing nothing redraw scene
	draw.initCubes(n_x, n_y, n_z)
	draw.initShaders()
	draw.initCamera()
	draw.initVBOs()
	draw.runMainGLLoop()

main()
