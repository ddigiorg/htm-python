# archlinux: certain opengl functions won't work on Windows without extensive tinkering
# python 3.5.1
# pyopengl 3.0 Mesa 11.1.2
# glsl 1.30

"""
TODO

+ Make origin top left of screen
+ Finish cleaning up graphics.py
+ Fix and finish Temporal Memory
+ Consider re-adding Synapse class to cortex.py
+ Add mouse support for graphics
+ Update README.md
+ Add better timing maybe in graphics.py?
+ For all files change tabs to spaces
+ Clean up repository (pycache)

+ Once Temporal Memory is complete work on 2d column topology
+ Graphics: highlight receptive fields when hovering over 2d column matrix (like in Matt's video)
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
num_inputs  = 2048#50
num_columns = 2048#50
num_neurons_per_column = 32#8

# Input state setup
inputs = np.zeros((5, num_inputs), dtype=np.int8)
inputs[0,  0: 5] = 1
inputs[1,  5:10] = 1
inputs[2, 10:15] = 1
inputs[3, 15:20] = 1
inputs[4, 20:25] = 1

# Class initializations
display = graphics.Display(800, 600, num_inputs, num_columns, num_neurons_per_column)

start = time.time()
layer3b = cortex.Layer3b(num_inputs, num_columns, num_neurons_per_column)
print("Layer3b Init Time: {}".format(time.time() - start))

sp = spatial_pooler.SpatialPooler()
tm = temporal_memory.TemporalMemory()

flag = 0

def loop():
	global flag

	l3b_inputs = inputs[flag]

	if display.flag == 1:
		start = time.time()
		sp.compute(layer3b, l3b_inputs)
	#	print("Spatial Pooler Time:  {}".format(time.time() - start))

		start = time.time()
		tm.compute(layer3b)
	#	print("Temporal Memory Time: {}".format(time.time() - start))

	#	time.sleep(1.0)

		if flag == 0:
			flag = 1
	#	elif flag == 1:
	#		flag = 2
	#	elif flag == 2:
	#		flag = 3
	#	elif flag == 3:
	#		flag = 4
		else:
			flag = 0

	start = time.time()
	display.updatePolygonColors(l3b_inputs, layer3b)
	display.updateViewProjection()
	display.updateScene()
#	print("Graphics Update Time: {}".format(time.time() - start))

	display.flag = 0

def main():
	glutDisplayFunc(loop)
	glutIdleFunc(loop)
	display.initOrthographicProjection()
	display.updatePolygonTemplate()
	display.updatePolygonPositions()
	display.runOpenglMainLoop()

main()
