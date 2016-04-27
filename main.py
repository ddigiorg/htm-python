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
neocortex   = None
n_regions   = 1 # Number of regions per cortex
n_columns   = 3 # Number of columns per region
n_neurons   = 5 # Number of neurons per column
n_dendrites = 1 # Number of dendrites per neuron
n_synapses  = 5 # Number of synapses per dendrite

# Input Setup
n_inputs = 10
inputs = [0]*n_inputs
inputs[1] = 1
inputs[2] = 1
inputs[3] = 1

# OpenGL Global Variables
n_x = n_columns # x axis for opengl
n_y = n_neurons # y axis for opengl
n_z = 1         # z axis for opengl

region_colors = np.array([[[ colors_dict[0] ]*n_z]*n_y]*n_x, dtype=np.float16)

flag = 0

def loop():
	global inputs, neocortex, n_regions, n_columns, n_neurons, n_dendrites, n_synapses
	global n_x, n_y, n_z, region_colors
	global colors_dict
	global flag

	temp = [[0, 0], [1, 1]]

	if flag == 0:
		for t in temp:
			neocortex.getRegions()[0].getColumns()[t[0]].getNeurons()[t[1]].setAxonOutput(0)
		flag = 1
	else:	
		for t in temp:
			neocortex.getRegions()[0].getColumns()[t[0]].getNeurons()[t[1]].setAxonOutput(2)
		flag = 0

	for c in range(n_columns):
		for n in range(n_neurons):
			state = neocortex.getRegions()[0].getColumns()[c].getNeurons()[n].getAxonOutput()
			region_colors[c][n][0] = colors_dict[state]
		
	draw.updateCubes(region_colors)
	draw.updateCamera()
	draw.updateScene()

def main():
	global inputs, neocortex, n_regions, n_columns, n_neurons, n_dendrites, n_synapses
	global n_x, n_y, n_z
	
	# Initialize cortex
	neocortex = cortex.initCortex(n_regions, n_columns, n_neurons, n_dendrites, n_synapses)
	neocortex = cortex.initSynapticConnections(inputs, neocortex)

	for c in range(n_columns):
		print("column {}".format(c))
		for s in range(n_synapses):
			print(neocortex.getRegions()[0].getColumns()[c].getProximalDendrite().getSynapses()[s].getConnectionAddress())

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
