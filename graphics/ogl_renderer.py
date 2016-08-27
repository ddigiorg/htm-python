# ogl_renderer.py

from OpenGL.GL import *   # !REMOVE STAR!
from OpenGL.GLUT import * # !REMOVE STAR!
import numpy as np

from graphics.g_global import OpenGLParams, ViewParams
import graphics.g_input as g_input
import graphics.g_shader as g_shader

def init():
	"""Opengl Initilization"""
	glutInit()
	glutInitDisplayMode( GLUT_RGBA )

	glutInitWindowSize( ViewParams.viewportWidth,
                        ViewParams.viewportHeight )

	glutInitWindowPosition( ViewParams.viewportX,
                            ViewParams.viewportY )

	OpenGLParams.windowID = glutCreateWindow( OpenGLParams.windowName )

	glClearColor( 0.0, 0.0, 0.0, 1.0 ) # Black background

	glutMouseFunc(g_input.mouseFunc)
	glutKeyboardFunc(g_input.keyboardFunc)
	glutSpecialFunc(g_input.keyboardFunc)

	# VBO variables
	OpenGLParams.meshBuffer = glGenBuffers( 1 )
	OpenGLParams.positionBuffer = glGenBuffers( 1 )
	OpenGLParams.colorBuffer = glGenBuffers( 1 )

	# Shader variables
	vertexShader = g_shader.compile_shader( "VS" )   
	fragmentShader = g_shader.compile_shader( "FS" )
	OpenGLParams.vertexShader = vertexShader   
	OpenGLParams.fragmentShader = fragmentShader

	shaderID = g_shader.link_shader_program(vertexShader, fragmentShader)
	OpenGLParams.shaderID = shaderID
	glUseProgram( shaderID )

	OpenGLParams.shaderMeshLocation = glGetAttribLocation( shaderID, "mesh" )
	OpenGLParams.shaderPositionLocation = glGetAttribLocation( shaderID, "position" )
	OpenGLParams.shaderColorLocation = glGetAttribLocation( shaderID, "color" )
	OpenGLParams.shaderProjectionMatrixLocation = glGetUniformLocation( shaderID, "projection" )
	OpenGLParams.shaderViewMatrixLocation = glGetUniformLocation( shaderID, "view" )

def updateVBO( shaderLocation, vboBuffer, vboList, size, usageType ):
	if usageType == "stream": vboUsage = GL_STREAM_DRAW
	elif usageType == "static": vboUsage = GL_STATIC_DRAW

	vboData = np.array(vboList, dtype=np.float16)
	glBindBuffer(GL_ARRAY_BUFFER, vboBuffer)
	glBufferData(GL_ARRAY_BUFFER, vboData, vboUsage)
	glEnableVertexAttribArray( shaderLocation )
	glVertexAttribPointer( shaderLocation, size, GL_HALF_FLOAT, False, 0, None)
	
def updateUniformMatrix( shaderLocation, matrix ):
	glUniformMatrix4fv( shaderLocation, 1, False, matrix )

def draw( num_polygons ):
	glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

	# * ?????????? For instancing... figure out what this does
	glVertexAttribDivisor( 0, 0 )
	glVertexAttribDivisor( 1, 1 )
	glVertexAttribDivisor( 2, 1 )

	# make a variable for the vertices (probably from template)
	# Draw cells: 6 vertices per triangle, 2 triangles per square
	glDrawArraysInstanced( GL_TRIANGLES, 0, 6*2, num_polygons )

	# Flush the opengl rendering pipeline   
	glutSwapBuffers()

def cleanup( shaderLocation, vboBuffer ):
	glDisableVertexAttribArray( shaderLocation )
	glDeleteBuffers(1, GLfloat( vboBuffer ) )

def exit( shaderID, windowID ):
	glDeleteProgram( shaderID )
	glutDestroyWindow( windowID )
