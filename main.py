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
import layers as l
import spatial_pooler as sp

colors_dict = {"inactive": [0.5, 0.5, 0.5], # Neuron inactive state
			   "active":   [0.0, 1.0, 0.0], # Neuron active (feed forward)
			   "predict":  [1.0, 0.0, 1.0]} # Neuron predictive state

# Cortex Global Variables
n_columns   = 8  # Number of columns per region
n_neurons   = 4  # Number of neurons per column
n_dendrites = 10 # Number of dendrites per neuron
n_synapses  = 5  # Number of synapses per dendrite

# Input Setup
num_inputs = 20
inputs = [None] * 2
for i in range(2):
	inputs[i] = [0] * num_inputs
for i in range(5):
	inputs[0][i] = 1
	inputs[1][i] = 1

# OpenGL Global Variables
n_cells_x = n_columns # x axis for opengl
n_cells_y = n_neurons # y axis for opengl

layer3b = l.Layer3b(num_inputs, n_columns, n_neurons)
active_columns = layer3b.runSpatialPooler(inputs[0])
print(active_columns)

region_colors = np.array([[ colors_dict["inactive"] ]*n_cells_y]*n_cells_x, dtype=np.float16)

flag = 0

def loop():
	global inputs, region, n_regions, n_columns, n_neurons, n_dendrites, n_synapses
	global n_cells_x, n_cells_y, region_colors
	global colors_dict
	global active_columns
	global flag

	if flag == 0: 
		for ac in active_columns:
			for n in range(n_neurons):
				region_colors[ac][n] = colors_dict["active"]
		flag = 1
#	else:
#		region_colors[0][0] = colors_dict["inactive"]
#		flag = 0
	
	draw.updatePolygons(region_colors, n_cells_x, n_cells_y)
	draw.updateView()
	draw.updateScene(n_cells_x, n_cells_y)

def main():
	global n_cells_x, n_cells_y
	
	# Initialize opengl drawing
	draw.initGL()
	glutDisplayFunc(loop) # Register the drawing function with glut
	glutIdleFunc(loop)    # When doing nothing redraw scene
	draw.initShaders()
	draw.initView()
	draw.initPolygons(n_cells_x, n_cells_y)
	draw.initVBOs()
	draw.runMainGLLoop()

main()
