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
import layers as l
import spatial_pooler as sp

# Cortex Global Variables
num_columns   = 8  # Number of columns per region
num_neurons   = 4  # Number of neurons per column
num_dendrites = 10 # Number of dendrites per neuron
num_synapses  = 5  # Number of synapses per dendrite

# Input Setup
num_inputs = 20
inputs = [None] * 2
for i in range(2):
	inputs[i] = [0] * num_inputs
for i in range(5):
	inputs[0][i] = 1
	inputs[1][i] = 1

layer3b = l.Layer3b(num_inputs, num_columns, num_neurons)
active_columns = layer3b.runSpatialPooler(inputs[0])
print(active_columns)

# neuron positions for graphics
NEURON_SPACING = 0.5

n_in_positions  = np.array( [0.0, 0.0] * num_inputs, dtype=np.float16)
n_l3b_positions = np.array( [ [0.0, 0.0] ] * num_neurons * num_columns, dtype=np.float16)

print(n_l3b_positions)

#for i in range(num_inputs):
#	n_in_positions[i] = [0.0 + i * (1.0 + NEURON_SPACING), # x world position
 #                        0.0                             ] # y world position

for c in range(num_columns):
	for n in range(num_neurons):
		n_l3b_positions[c+n][0] = 0.0 + c * (1.0 + NEURON_SPACING) # x world position
		n_l3b_positions[c+n][1] = 2.0 + n * (1.0 + NEURON_SPACING) # y world position

print(n_l3b_positions)

# neuron colors for graphics
colors_dict = {"inactive": [0.5, 0.5, 0.5], # Neuron inactive state
			   "active":   [0.0, 1.0, 0.0], # Neuron active (feed forward)
			   "predict":  [1.0, 0.0, 1.0]} # Neuron predictive state

neuron_colors = np.array([ [ colors_dict["inactive"] ]*num_neurons ]*num_columns, dtype=np.float16)

flag = 0

def loop():
	global flag

	if flag == 0: 
		for ac in active_columns:
			for n in range(num_neurons):
				neuron_colors[ac][n] = colors_dict["active"]
		flag = 1

#	else:
#		cell_colors[0][0] = colors_dict["inactive"]
#		flag = 0
	
	g.gUpdatePolygonColors(neuron_colors)
	g.gUpdateView()
	g.gUpdateScene(num_columns, num_neurons)

def main():
	g.gInit()
	glutDisplayFunc(loop) # Register the ging function with glut
	glutIdleFunc(loop)    # When doing nothing reg scene
	g.gInitShaders()
	g.gInitView()
	g.gInitPolygons(num_columns, num_neurons)
	g.gInitVBOs()
	g.gUpdatePolygonPositions(n_l3b_positions)
	g.gRunMainGLLoop()

main()
