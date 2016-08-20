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

#import graphics as graphics
import cortex
import spatial_pooler

import numpy as np
import time

# Cortex global variables
num_inputs  = 2048
num_columns = 2048
num_neurons_per_column = 32

# Input state setup
inputs = np.zeros((3, num_inputs), dtype=np.int8)
inputs[0,  0: 5] = 1
inputs[1,  5:10] = 1
inputs[2, 10:15] = 1

# Class initializations
#display = graphics.Display(800, 600, in_size, c_size, npc_size)
start = time.time()
layer3b = cortex.Layer3b(num_inputs, num_columns, num_neurons_per_column)
stop = time.time()
print(stop - start)

sp = spatial_pooler.SpatialPooler()

start = time.time()
sp.compute(layer3b, inputs[0])
stop = time.time()
print(stop - start)





#flag = 0
#
#def loop():
#	global flag
#
#	l3b_inputs = inputs[flag]
#
#	start = time.time()
#	layer3b.runSpatialPooler(l3b_inputs)
#	stop = time.time()
#	print("Spatial Pooler Time:  {}".format(stop - start))
#
#	start = time.time()
#	layer3b.runTemporalMemory()
#	stop = time.time()
#	print("Temporal Memory Time: {}".format(stop - start))
#
#	print( layer3b.active_columns )
#	wn = layer3b.winner_neurons[0]
#	print( layer3b.neurons[wn].bs_addresses )
#	print( layer3b.neurons[wn].bs_permanences )
#
#	start = time.time()
#	display.updatePolygonColors(l3b_inputs, layer3b)
#	display.updateViewProjection()
#	display.updateScene()
#	stop = time.time()
#	print("Graphics Update Time: {}".format(stop - start))
#
#	time.sleep(1.0)
#
#	if flag == 0:
#		flag = 1
#	elif flag == 1:
#		flag = 2
#	else:
#		flag = 0
#
#def main():
#	glutDisplayFunc(loop)
#	glutIdleFunc(loop)
# 
#	display.initOrthographicProjection()
#	display.initPolygonGraphicsData()
#	display.updatePolygonTemplate()
#	display.updatePolygonPositions()
#	display.runOpenglMainLoop()
#
#main()
