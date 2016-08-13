# archlinux: certain opengl functions won't work on Windows without extensive tinkering
# python 3.5.1
# pyopengl 3.0 Mesa 11.1.2
# glsl 1.30

"""
TODO

+ Add better timing??? maybe in graphics.py?
+ Address issues and comments

+ Update README.md
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
#from OpenGL.GLU import * # <-- uneeded so delete when finished
import graphics as graphics
import htm as htm
import numpy as np
import time

# Cortex global variables
in_size  = 20 # Number of input neurons
c_size   = 20 # Number of columns
npc_size = 4  # Number of neurons per column

# Input state setup
inputs = [None] * 2
for i in range(2):
	inputs[i] = [0] * in_size
for i in range(5):
	inputs[0][ i  ] = 1
	inputs[1][-i-1] = 1

# Class initializations
display = graphics.Display(800, 600, in_size, c_size, npc_size)
layer3b = htm.Layer3b(in_size, c_size, npc_size)

flag = 1

def loop():
	global flag

	if flag == 0:
		flag = 1
	else:
		flag = 0

	l3b_inputs = inputs[flag]

	layer3b.runSpatialPooler(l3b_inputs)
	layer3b.runTemporalMemory()

	display.updatePolygonColors(l3b_inputs, layer3b)
	display.updateViewProjection()
	display.updateScene()

#	time.sleep(3.0)

def main():
	glutDisplayFunc(loop)
	glutIdleFunc(loop)
 
	display.initOrthographicProjection()
	display.initPolygonGraphicsData()
	display.updatePolygonTemplate()
	display.updatePolygonPositions()
	display.runOpenglMainLoop()

main()
