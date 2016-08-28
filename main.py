"""
TODO
+ Clean g_scene code
+ Graphics: some indicator for connected synapses
+ Fix and finish Temporal Memory
+ Consider re-adding Synapse class to cortex.py
+ Update README.md
+ Add learning to spatial pooler
+ Add better timing maybe in graphics?
+ Clean entire code!  Make standardize class, function, and variable names to a convention
+ For all files change tabs to spaces
+ Clean up repository (pycache)
"""

from OpenGL.GL import *   # TODO: Remove stars
from OpenGL.GLUT import * # TODO: Remove stars

import graphics.g_main as g_main
import htm.encoder as encoder
import htm.cortex as cortex
import htm.spatial_pooler as sp
import htm.temporal_memory as tm

import numpy as np
import time

# Cortex variables
numInputsX = 25
numInputsY = 25 
numColumnsX = numInputsX
numColumnsY = numInputsY
numNeuronsPerColumn = 32

dimensions = ( numInputsX, numInputsY, numColumnsX, numColumnsY, numNeuronsPerColumn )

# Class initializations
encode = encoder.Encoder( dimensions[0], dimensions[1] )
layer3b = cortex.Layer3b( dimensions )

flag = 0
inputs = None

def loop():
	global flag, inputs
	pause = g_main.getPauseFlag()

	if pause == False:
		inputs = encode.inputs[flag]
		sp.computeSpatialPooler( inputs, layer3b )
		tm.computeTemporalMemory( layer3b )
	
		if flag == 0:
			flag = 1
		else:
			flag = 0

	#time.sleep(0.05)
	g_main.updateGraphics( inputs, layer3b )

def main():
	g_main.initGraphics( encode, layer3b )
	glutDisplayFunc( loop )
	glutIdleFunc( loop )
	glutMainLoop()

main()
