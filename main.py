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
n_inputs = 20
inputs0 = [0]*n_inputs
inputs0[0] = 1
inputs0[1] = 1
inputs0[2] = 1
inputs0[3] = 1
inputs0[4] = 1

inputs1 = [0]*n_inputs
inputs1[1] = 1 
inputs1[2] = 1
inputs1[3] = 1
inputs1[4] = 1
inputs1[5] = 1

inputs = inputs0

# OpenGL Global Variables
n_x = n_columns # x axis for opengl
n_y = n_neurons # y axis for opengl
n_z = 1         # z axis for opengl

region_colors = np.array([[[ colors_dict[0] ]*n_z]*n_y]*n_x, dtype=np.float16)

flag = 0

def loop():
	global inputs, inputs0, inputs1, region, n_regions, n_columns, n_neurons, n_dendrites, n_synapses
	global n_x, n_y, n_z, region_colors
	global colors_dict
	global flag

	if flag == 0:
		inputs = inputs0
		flag = 1
	elif flag == 1:
		inputs = inputs1
		flag = 0

	cortex.runSpatialPooler(inputs, region)

	for c in range(n_columns):
		for n in range(n_neurons):
			state = region.getColumns()[c].getNeurons()[n].getAxonOutput()
			region_colors[c][n][0] = colors_dict[state]
		
	draw.updateCubes(region_colors)
	draw.updateCamera()
	draw.updateScene()

def main():
	global inputs, region, n_regions, n_columns, n_neurons, n_dendrites, n_synapses
	global n_x, n_y, n_z
	
	# Initialize cortex
	region = cortex.initRegion(inputs0, n_columns, n_neurons, n_dendrites, n_synapses)
	region = cortex.initConnections(inputs0, region)


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
