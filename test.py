from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import shader as shader

# glutInit()
# window = glutCreateWindow("test")
# print(glGetString(GL_SHADING_LANGUAGE_VERSION))
# print(glGetString(GL_VERSION))
# glutDestroyWindow(window)

shaders_program = None
shaders_template_location = None
shaders_position_location = None
shaders_color_location = None

template_buffer = None
template_data = np.array([-1.0, -1.0, 0.0, 1.0, -1.0, 0.0, 0.0, 1.0, 0.0], dtype=np.float32)
position_buffer = None
position_data = np.array([0.0, 0.0, 0.0], dtype=np.float32)
color_buffer = None
color_data = np.array([0.0, 0.0, 1.0], dtype=np.float32)


def initShaders():
	global shaders_program, shaders_template_location, shaders_position_location, shaders_color_location
	vertex_shader   = shader.compile_shader("vertex")
	fragment_shader = shader.compile_shader("fragment")
	shaders_program = shader.link_shader_program(vertex_shader, fragment_shader)

	shaders_template_location = glGetAttribLocation(shaders_program, "vertex_template")
	shaders_position_location = glGetAttribLocation(shaders_program, "vertex_position")
	shaders_color_location = glGetAttribLocation(shaders_program, "vertex_color_in")

def initVBO():
	global template_buffer, template_data, position_buffer, position_data, color_buffer, color_data
	template_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, template_buffer)
	glBufferData(GL_ARRAY_BUFFER, template_data, GL_STATIC_DRAW)

	position_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, position_buffer)
	glBufferData(GL_ARRAY_BUFFER, position_data, GL_STATIC_DRAW)

	color_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
	glBufferData(GL_ARRAY_BUFFER, color_data, GL_STATIC_DRAW)


def draw():
	global shaders_program, shaders_position_location, shaders_color_location
	global vertex_buffer, vertex_data, color_buffer, color_data 
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	glUseProgram(shaders_program)

	glEnableVertexAttribArray(shaders_template_location)
	glBindBuffer(GL_ARRAY_BUFFER, template_buffer)
	glVertexAttribPointer(shaders_template_location, 3, GL_FLOAT, False, 0, None)

	glEnableVertexAttribArray(shaders_position_location)
	glBindBuffer(GL_ARRAY_BUFFER, position_buffer)
	glVertexAttribPointer(shaders_position_location, 3, GL_FLOAT, False, 0, None)

	glEnableVertexAttribArray(shaders_color_location)
	glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
	glVertexAttribPointer(shaders_color_location, 3, GL_FLOAT, False, 0, None)

	glVertexAttribDivisor(0, 0)
	glVertexAttribDivisor(1, 1)
	glVertexAttribDivisor(2, 1)

	glDrawArraysInstanced(GL_TRIANGLES, 0, 3, 1)
	
	glDisableVertexAttribArray(shaders_template_location)
	glDisableVertexAttribArray(shaders_position_location)
	glDisableVertexAttribArray(shaders_color_location)

	glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutInitWindowPosition(0, 0)
window = glutCreateWindow("Test")
glClearColor(0.0, 0.0, 0.0, 1.0)
glutDisplayFunc(draw)

initShaders()
initVBO()

glutMainLoop()
