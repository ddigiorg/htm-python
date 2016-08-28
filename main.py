"""
TODO
+ Graphics: highlight receptive fields when hovering over 2d column matrix (like in Matt's video)
+ Fix and finish Temporal Memory
+ Complete 2d column topology
+ Consider re-adding Synapse class to cortex.py
+ Update README.md
+ Add learning to spatial pooler
+ Add better timing maybe in graphics?
+ Clean entire code!  Make standardize class, function, and variable names to a convention
+ For all files change tabs to spaces
+ Clean up repository (pycache)
"""

from OpenGL.GL import *   # !REMOVE STARS!
from OpenGL.GLUT import * # !REMOVE STARS!

import graphics.g_main as g_main
import htm.encoder as encoder
import htm.cortex as cortex
import htm.spatial_pooler as spatial_pooler
import htm.temporal_memory as temporal_memory

import numpy as np
import time

# Cortex variables
numInputsX = 25 #2048
numInputsY = 25
numColumnsX = numInputsX
numColumnsY = numInputsY
numNeuronsPerColumn = 3 #32

dimensions = ( numInputsX, numInputsY, numColumnsX, numColumnsY, numNeuronsPerColumn )

# Class initializations
encode = encoder.Encoder( dimensions[0], dimensions[1] )
layer3b = cortex.Layer3b( dimensions )
sp = spatial_pooler.SpatialPooler()
#tm = temporal_memory.TemporalMemory()

flag = 0

layer = None

def loop():
	global flag

	sp.compute(encode.inputs, layer3b)
#	tm.compute(layer3b)
	time.sleep(0.05)

	if flag == 0:
		flag = 1
	else:
		flag = 0

	g_main.updateGraphics()

def main():
	g_main.initGraphics( dimensions, encode, layer3b )
	glutDisplayFunc( loop )
	glutIdleFunc( loop )
	glutMainLoop()

main()
