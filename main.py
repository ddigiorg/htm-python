# archlinux: certain opengl functions won't work on Windows without extensive tinkering
# python 3.5.1
# pyopengl 3.0 Mesa 11.1.2
# glsl 1.30

"""
TODO

+ Make origin top left of screen
+ Put Camera() and Scene() into OpenGLRenderer() or make seperate Renderer() class
+ Standardize OpenGLRenderer() methods
+ Consider making template a uniform matrix
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

import graphics
import cortex
import spatial_pooler
import temporal_memory

import numpy as np
import time

# Application variables
window_width  = 800
window_height = 600

# Cortex variables
num_inputs  = 2048
num_columns = 2048
num_neurons_per_column = 32

# Input state setup
inputs = np.zeros((5, num_inputs), dtype=np.int8)
inputs[0,  0: 5] = 1
inputs[1,  5:10] = 1
inputs[2, 10:15] = 1
inputs[3, 15:20] = 1
inputs[4, 20:25] = 1

# Class initializations
#gRender = graphics.Renderer()
gScene  = graphics.Scene(num_inputs, num_columns, num_neurons_per_column)
gCamera = graphics.Camera(window_width, window_height)
gRender = graphics.OpenGLRenderer(gCamera)

start = time.time()
layer3b = cortex.Layer3b(num_inputs, num_columns, num_neurons_per_column)
print("Layer3b Init Time: {}".format(time.time() - start))

sp = spatial_pooler.SpatialPooler()
tm = temporal_memory.TemporalMemory()

flag = 0

def loop():
	global flag

	l3b_inputs = inputs[flag]

	if gRender.flag == 1:
		start = time.time()
		sp.compute(layer3b, l3b_inputs)
		print("Spatial Pooler Time:  {}".format(time.time() - start))

		start = time.time()
		tm.compute(layer3b)
		print("Temporal Memory Time: {}".format(time.time() - start))

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
	color_list = gScene.polygonColors(l3b_inputs, layer3b)
	gRender.updateColorVBO(color_list)

	view_matrix = gCamera.updateView()
	gRender.updateViewMatrix(view_matrix)

	gRender.drawScene( int(len(color_list)/3) )

#	print("Graphics Update Time: {}".format(time.time() - start))

	gRender.flag = 0

def main():
	glutDisplayFunc(loop)
	glutIdleFunc(loop)

	proj_matrix = gCamera.initOrthographicProjection()
	gRender.updateProjectionMatrix(proj_matrix)

	template_list = gScene.polygonTemplate()
	gRender.updateTemplateVBO(template_list)

	position_list = gScene.polygonPositions()
	gRender.updatePositionVBO(position_list)

	glutMainLoop()

main()
