# archlinux: certain opengl functions won't work on Windows without extensive tinkering
# python 3.5.1
# pyopengl 3.0 Mesa 11.1.2
# glsl 1.30

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import random as rand
import graphics as g
import htm as htm

import time

colors_dict = {"inactive": [0.5, 0.5, 0.5], # Neuron inactive state
               "active":   [0.0, 1.0, 0.0], # Neuron active (feed forward)
               "predict":  [1.0, 0.0, 1.0]} # Neuron predictive state

# Cortex Global Variables
num_columns   = 20 # Number of columns per region
num_neurons   = 4  # Number of neurons per column
num_dendrites = 10 # Number of dendrites per neuron
num_synapses  = 5  # Number of synapses per dendrite

# Input Setup
num_inputs = 20
inputs = [None] * 2
for i in range(2):
	inputs[i] = [0] * num_inputs
for i in range(5):
	inputs[0][ i  ] = 1
	inputs[1][-i-1] = 1

flag = 0

in_colors  = None
l3b_colors = None
region_colors = None
active_columns = None

layer3b = htm.Layer3b(num_inputs, num_columns, num_neurons)

def loop():
	global flag
	global region_colors

	# reset all neuron color data to inactive
	in_colors  = np.full(num_inputs * 3, 0.5, dtype=np.float16)
	l3b_colors = np.full(num_columns * num_neurons * 3, 0.5, dtype=np.float16)

	l3b_inputs = []
	if flag == 0:
		l3b_inputs = inputs[0]
#		flag = 1
	else:
		l3b_inputs = inputs[1]
		flag = 0

	layer3b.runSpatialPooler(l3b_inputs)
	active_columns = layer3b.getActiveColumnAddresses()
	layer3b.runTemporalMemory()
	active_neurons = layer3b.getActiveNeuronAddresses()

	for i in range(num_inputs):
		if l3b_inputs[i] == 1:
			index = i * 3
			in_colors[index:index+3] = colors_dict["active"]

	for c, n in active_neurons:
		index = (c * num_neurons + n) * 3
		l3b_colors[index:index+3] = colors_dict["active"]

	region_colors = np.concatenate( (in_colors, l3b_colors), axis=0 )

	g.gUpdatePolygonColors(region_colors)
	g.gUpdateView()
	g.gUpdateScene(num_inputs + num_columns * num_neurons)

	time.sleep(1.0)

def main():
	global in_colors, l3b_colors
	global active_columns

#	layer3b = htm.Layer3b(num_inputs, num_columns, num_neurons)
#	layer3b.runSpatialPooler(inputs[0])
#	active_columns = layer3b.getActiveColumnAddresses()
#	print(active_columns)

	in_positions, l3b_positions, in_colors, l3b_colors = g.gInitNeuronGraphicsData(num_inputs, num_columns, num_neurons)

	region_positions = np.concatenate( (in_positions, l3b_positions), axis=0 )

	g.gInit()
	glutDisplayFunc(loop)
	glutIdleFunc(loop)
	g.gInitShaders()
	g.gInitView()
	g.gInitVBOs()
	g.gUpdatePolygonTemplate()
	g.gUpdatePolygonPositions(region_positions)
	g.gRunMainGLLoop()

main()
