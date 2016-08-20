# archlinux: certain opengl functions won't work on Windows without extensive tinkering
# python 3.5.1
# pyopengl 3.0 Mesa 11.1.2
# glsl 1.30

"""
TODO

+ Add better timing??? maybe in graphics.py?
+ Address issues and comments

+ Update README.md

+ For all files choose naming convention for size or number of items in a list
+ For all files change "neuron" to "cell"
+ For all files change tabs to spaces
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
#from OpenGL.GLU import * # <-- uneeded so delete when finished

import graphics
import cortex
import spatial_pooler
import temporal_memory

import numpy as np
import time

# Cortex global variables
num_inputs  = 50
num_columns = 50
num_neurons_per_column = 4

# Input state setup
inputs = np.zeros((3, num_inputs), dtype=np.int8)
inputs[0,  0: 5] = 1
inputs[1,  5:10] = 1
inputs[2, 10:15] = 1

# Class initializations
display = graphics.Display(800, 600, num_inputs, num_columns, num_neurons_per_column)

#start = time.time()
layer3b = cortex.Layer3b(num_inputs, num_columns, num_neurons_per_column)
#print("Layer3b Init Time: {}".format(time.time() - start))

sp = spatial_pooler.SpatialPooler()
tm = temporal_memory.TemporalMemory()

flag = 0

def loop():
	global flag

	l3b_inputs = inputs[flag]

#	start = time.time()
	sp.compute(layer3b, l3b_inputs)
#	print("Spatial Pooler Time:  {}".format(time.time() - start))

#	start = time.time()
	tm.compute(layer3b)
#	print("Temporal Memory Time: {}".format(time.time() - start))

#	start = time.time()
	display.updatePolygonColors(l3b_inputs, layer3b)
	display.updateViewProjection()
	display.updateScene()
#	print("Graphics Update Time: {}".format(time.time() - start))

	time.sleep(1.0)

	if flag == 0:
		flag = 1
#	elif flag == 1:
#		flag = 2
	else:
		flag = 0


def main():
	glutDisplayFunc(loop)
	glutIdleFunc(loop)
 
	display.initOrthographicProjection()
	display.initPolygonGraphicsData()
	display.updatePolygonTemplate()
	display.updatePolygonPositions()
	display.runOpenglMainLoop()

main()
