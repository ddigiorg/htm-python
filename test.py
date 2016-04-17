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

shaders_programID = None
shaders_frustumID  = None
shaders_template_location = None
shaders_position_location = None
shaders_color_location = None

frustum_matrix = None

template_buffer = None
template_data = np.array([-1.0, -1.0, 5.0, 1.0, -1.0, 5.0, 0.0, 1.0, 5.0], dtype=np.float32)
position_buffer = None
position_data = np.array([0.0, 0.0, 0.0], dtype=np.float32)
color_buffer = None
color_data = np.array([0.0, 0.0, 1.0], dtype=np.float32)


def initShaders():
	global shaders_programID, shaders_frustumID, shaders_template_location, shaders_position_location, shaders_color_location
	vertex_shader   = shader.compile_shader("VS")
	fragment_shader = shader.compile_shader("FS")
	shaders_programID = shader.link_shader_program(vertex_shader, fragment_shader)

	shaders_template_location = glGetAttribLocation(shaders_programID, "templateVS")
	shaders_position_location = glGetAttribLocation(shaders_programID, "positionVS")
	shaders_color_location = glGetAttribLocation(shaders_programID, "colorVS_in")

	shaders_frustumID = glGetUniformLocation(shaders_programID, "frustum")

def initView():
	global frustum_matrix
	view_angle = 45.0
	aspect_ratio = 4.0/3.0
	z_near = 0.5
	z_far  = 5.0

	frustum_matrix = [1.0/np.tan(view_angle), 0.0,                             0.0,                              0.0,
					  0.0,                    aspect_ratio/np.tan(view_angle), 0.0,                              0.0,
					  0,0,                    0.0,                             (z_far+z_near)/(z_far-z_near),    0.0,
					  0.0,                    0.0,                             -2.0*z_far*z_near/(z_far-z_near), 0.0]


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
	global shaders_programID, shaders_frustumID, shaders_position_location, shaders_color_location
	global frustum_matrix
	global vertex_buffer, vertex_data, color_buffer, color_data 
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	glUseProgram(shaders_programID)
	glUniformMatrix4fv(shaders_frustumID, 1, False, frustum_matrix)

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

def keyPressed(key, x, y):
	if key == '\x1b'.encode():
		cleanup()
	if key == 'd'.encode():
		x_camera_pos += CAMERA_SPEED
	if key == 'a'.encode():
		x_camera_pos -= CAMERA_SPEED
	if key == 'e'.encode():
		y_camera_pos += CAMERA_SPEED
	if key == 'q'.encode():
		y_camera_pos -= CAMERA_SPEED
	if key == 's'.encode():
		z_camera_pos += CAMERA_SPEED
	if key == 'w'.encode():
		z_camera_pos -= CAMERA_SPEED

def cleanup():
	global window
	global template_buffer, position_buffer, color_buffer
	global shaders_programID

	glDeleteBuffers(1, GLfloat(template_buffer))
	glDeleteBuffers(1, GLfloat(position_buffer))
	glDeleteBuffers(1, GLfloat(color_buffer))
	glDeleteProgram(shaders_programID)
	glutDestroyWindow(window)
	exit(0)

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutInitWindowPosition(0, 0)
window = glutCreateWindow("Test")
glutDisplayFunc(draw)
glutKeyboardFunc(keyPressed)
glClearColor(0.0, 0.0, 0.0, 1.0)


initShaders()
initView()
initVBO()

glutMainLoop()
