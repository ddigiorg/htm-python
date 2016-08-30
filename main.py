"""
TODO
+ Fix and finish Temporal Memory
+ Consider re-adding Synapse class to cortex.py
+ Update README.md
+ Add learning to spatial pooler
+ Add better timing maybe in graphics?
+ Clean g_scene code
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
layerIn = encoder.InputLayer( dimensions )
layer3b = cortex.Layer3b( dimensions )
cortex.initReceptiveFields( layerIn, layer3b )

flag = 0

def loop():
	global flag
	pause = g_main.getPauseFlag()

	if pause == False:
		if flag == 0:
			layerIn.activeateInputs( 0, 4 )
			flag = 1
		else:
			layerIn.activeateInputs( 5, 9 )
			flag = 0

		sp.computeSpatialPooler( layerIn, layer3b )
		tm.computeTemporalMemory( layer3b )

	#time.sleep(0.05)
	g_main.updateGraphics( layerIn, layer3b )

def main():
	g_main.initGraphics( layerIn, layer3b )
	glutDisplayFunc( loop )
	glutIdleFunc( loop )
	glutMainLoop()

main()
