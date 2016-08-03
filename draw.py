# draw.py

# http://www.opengl-tutorial.org/intermediate-tutorials/billboards-particles/particles-instancing/
# https://github.com/opengl-tutorials/ogl/blob/master/tutorial18_billboards_and_particles/tutorial18_particles.cpp
# http://www.paridebroggi.com/2015/06/optimized-cell-opengl-triangle-strip.html
# http://duriansoftware.com/joe/An-intro-to-modern-OpenGL.-Chapter-3:-3D-transformation-and-projection.html

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import shader as shader

# Main global variables
window = 0
width, height = 800, 600

# Cube global variables
n_polys_x = None 
n_polys_y = None
n_polys_z = None
n_polys   = None
polys_world_positions = None
polys_world_colors    = None
POLY_SPACING = 2.0

# Camera global variables
orthographic_matrix     = None
view_matrix        = None
x_camera_pos       = 0.0
y_camera_pos       = 0.0
z_camera_pos       = 10.0
yaw_camera_angle   = 0.0
pitch_camera_angle = 0.0
CAMERA_SPEED       = 4.0
CAMERA_ANGLE       = 10.0

# Shader global variables
shaders_programID         = None
shaders_projectionID      = None
shaders_viewID            = None
shaders_template_location = None
shaders_position_location = None
shaders_color_location    = None

# VBO global variables
template_buffer  = None
position_buffer  = None
color_buffer     = None
template_data    = None
position_data    = None
color_data       = None
VERTEX_SIZE      = 3 # 3 vertices per triangle
POSITION_SIZE    = 3 # xyz
COLOR_SIZE       = 3 # rgb

# Keyboard global variables
ESCAPE = '\x1b'

def initGL():
	global window

	glutInit()								# Initialize opengl
	glutInitDisplayMode(GLUT_RGBA   |		# RGBA color
						GLUT_DOUBLE |		# *Double Buffer
						GLUT_ALPHA) 		# Alpha Components
	glutInitWindowSize(width, height)		# Initialize window size
	glutInitWindowPosition(0, 0)			# Window at upper left corner of screen
	window = glutCreateWindow("HTM")		# Create window with name "HTM"
	glutKeyboardFunc(keyPressed)			# Register function when keyboard pressed
	glutSpecialFunc(keyPressed)				# Register function when keyboard pressed
	glClearColor(0.0, 0.0, 0.0, 1.0)		# Black background
	glShadeModel(GL_SMOOTH)					# Select Smooth Shading
	glHint(GL_PERSPECTIVE_CORRECTION_HINT,
               GL_NICEST)	                # *Set Perspective Calculations to most accurate
	glColor4f(1.0, 6.0, 6.0, 1.0)			# *FIGURE OUT WHAT THIS DOES

def runMainGLLoop():
	glutMainLoop()                          # Start event processing engine


def initDrawPolygons(n_polys_x, n_polys_y, n_polys_z):
	global template_data, position_data, color_data

	n_polys = n_polys_x * n_polys_y * n_polys_z
	polys_world_positions = np.array([[[None]*n_polys_z]*n_polys_y]*n_polys_x)
	polys_world_colors    = np.array([[[None]*n_polys_z]*n_polys_y]*n_polys_x)

	template_list = [
		-0.5,  0.5,  0.0, -0.5, -0.5,  0.0,  0.5, -0.5,  0.0,
		 0.5,  0.5,  0.0, -0.5,  0.5,  0.0,  0.5, -0.5,  0.0,]

	position_list = [0] * n_polys * POSITION_SIZE
	
	i = 0
	for z in range(n_polys_z):
		for y in range(n_polys_y):
			for x in range(n_polys_x):	
				position_list[i*POSITION_SIZE  ] = 0.0 + x * POLY_SPACING # cell x world position
				position_list[i*POSITION_SIZE+1] = 0.0 + y * POLY_SPACING # cell y world position
				position_list[i*POSITION_SIZE+2] = 0.0 + z * POLY_SPACING # cell z world position

				polys_world_colors[x][y][z] = [0.5, 0.5, 0.5]
				i += 1

	template_data = np.array(template_list, dtype=np.float16)
	position_data = np.array(position_list, dtype=np.float16)
	print(position_data)

def initShaders():
	global shaders_programID, shaders_projectionID, shaders_viewID, shaders_template_location, shaders_position_location, shaders_color_location
	vertex_shader   = shader.compile_shader("VS")
	fragment_shader = shader.compile_shader("FS")
	shaders_programID = shader.link_shader_program(vertex_shader, fragment_shader)     

	shaders_template_location = glGetAttribLocation(shaders_programID, "templateVS")
	shaders_position_location = glGetAttribLocation(shaders_programID, "positionVS")
	shaders_color_location    = glGetAttribLocation(shaders_programID, "colorVS_in")

	shaders_projectionID = glGetUniformLocation(shaders_programID, "projection")
	shaders_viewID = glGetUniformLocation(shaders_programID, "view" )

def initCamera():
	global width, height
	global orthographic_matrix
	view_angle = 60.0
	aspect_ratio = width/height
	z_near = 1.0
	z_far  = 10.0
	
	orthographic_matrix = [1.0/np.tan(view_angle), 0.0,                             0.0,                              0.0,
                           0.0,                    aspect_ratio/np.tan(view_angle), 0.0,                              0.0,
                           0,0,                    0.0,                             (z_far+z_near)/(z_far-z_near),    0.0,
                           0.0,                    0.0,                             -2.0*z_far*z_near/(z_far-z_near), 0.0]

	l = 0.0
	r = width
	t = height
	b = 0.0
	f = -1.0
	n = 1.0

#	orthographic_matrix = [2.0/(r-l), 0.0,       0.0,        -(r+l)/(r-l),
#				  	 	   0.0,       2.0/(t-b), 0.0,        -(t+b)/(t-b),
#                          0,0,       0.0,       -2.0/(f-n), -(f+n)/(f-n),
#                          0.0,       0.0,       0.0,        1.0]

def initVBOs():
	global template_buffer, position_buffer, color_buffer, template_data, position_data
      
	# Opengl VBO vertex template buffer created, bound, and filled with vertex template data
	template_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, template_buffer)
	glBufferData(GL_ARRAY_BUFFER, template_data, GL_STATIC_DRAW)

	# Opengl VBO cell position buffer created, bound, and filled with cell position data
	position_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, position_buffer)
	glBufferData(GL_ARRAY_BUFFER, position_data, GL_STATIC_DRAW)

	# Opengl VBO cell color buffer created, bound, and left empty
	color_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
	glBufferData(GL_ARRAY_BUFFER, None, GL_STREAM_DRAW)

def updatePolygons(array_3d, n_polys_x, n_polys_y, n_polys_z):
	global color_data

	n_polys = n_polys_x * n_polys_y * n_polys_z
	color_list = [0] * n_polys * COLOR_SIZE

	i = 0
	for z in range(n_polys_z):
		for y in range(n_polys_y):
			for x in range(n_polys_x):	
				color_list[i*COLOR_SIZE  ] = array_3d[x][y][z][0] # cell r color
				color_list[i*COLOR_SIZE+1] = array_3d[x][y][z][1] # cell g color
				color_list[i*COLOR_SIZE+2] = array_3d[x][y][z][2] # cell b color
				i += 1
	
	color_data = np.array(color_list, dtype=np.float16)

def updateCamera():
	global view_matrix
	view_matrix = [1.0,          0.0,          0.0,          0.0,
				   0.0,          1.0,          0.0,          0.0,
				   0.0,          0.0,          1.0,          0.0,
				   x_camera_pos, y_camera_pos, z_camera_pos, 1.0]

#	view_matrix = [1.0, 0.0, 0.0, 1.0,
#				   0.0, 1.0, 0.0, 1.0,
#				   0.0, 0.0, 1.0, 1.0,
#				   1.0, 1.0, 1.0, 1.0]



def updateScene(n_polys_x, n_polys_y, n_polys_z):
	global position_buffer, color_buffer, position_data, color_data
	global shaders_programID, shaders_projectionID, shaders_viewID, shaders_template_location, shaders_position_location, shaders_color_location
	global orthographic_matrix, view_matrix

	n_polys = n_polys_x * n_polys_y * n_polys_z

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	# Opengl VBO cell color buffer bound, "orphaned", and filled with data
	glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
	glBufferData(GL_ARRAY_BUFFER, color_data, GL_STREAM_DRAW)
	#glBufferSubData(GL_ARRAY_BUFFER, 0, n_polys * sys.getsizeof(GLfloat) * 4, color_data)  <-- try to get working! orphaning not working

	# Get shader ID
	glUseProgram(shaders_programID)
	
	# Update shader with orthographic and view matrix
	glUniformMatrix4fv(shaders_projectionID, 1, False, orthographic_matrix)
	glUniformMatrix4fv(shaders_viewID, 1, False, view_matrix)

	# Shader attribute buffer: vertices template
	glEnableVertexAttribArray(shaders_template_location)
	glBindBuffer(GL_ARRAY_BUFFER, template_buffer)
	glVertexAttribPointer(shaders_template_location, VERTEX_SIZE, GL_HALF_FLOAT, False, 0, None)

	# Shader attribute buffer: cell positions
	glEnableVertexAttribArray(shaders_position_location)
	glBindBuffer(GL_ARRAY_BUFFER, position_buffer)
	glVertexAttribPointer(shaders_position_location, POSITION_SIZE, GL_HALF_FLOAT, False, 0, None)

	# Shader attribute buffer: cell colors
	glEnableVertexAttribArray(shaders_color_location)
	glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
	glVertexAttribPointer(shaders_color_location, COLOR_SIZE, GL_HALF_FLOAT, True, 0, None) # normalized for unsigned char

	# * ?????????? For instancing... figure out what this does
	glVertexAttribDivisor(0, 0)
	glVertexAttribDivisor(1, 1)
	glVertexAttribDivisor(2, 1)

	# Draw cells
	glDrawArraysInstanced(GL_TRIANGLES, 0, 9*12, n_polys) # try GL_TRIANGLE_STRIP with elements, make 9*12 more explicit!
	

	glDisableVertexAttribArray(shaders_template_location)
	glDisableVertexAttribArray(shaders_position_location)
	glDisableVertexAttribArray(shaders_color_location)

	# Flush the opengl rendering pipeline	
	glutSwapBuffers()	

def keyPressed(key, x, y):
	global x_camera_pos, y_camera_pos, z_camera_pos, yaw_camera_angle, pitch_camera_angle
	if key == ESCAPE.encode():
		cleanup()
	if key == 'a'.encode():
		x_camera_pos += CAMERA_SPEED
	if key == 'd'.encode():
		x_camera_pos -= CAMERA_SPEED
	if key == 'q'.encode():
		y_camera_pos += CAMERA_SPEED
	if key == 'e'.encode():
		y_camera_pos -= CAMERA_SPEED
	if key == 's'.encode():
		z_camera_pos += CAMERA_SPEED
	if key == 'w'.encode():
		z_camera_pos -= CAMERA_SPEED
	if key == GLUT_KEY_LEFT:
		yaw_camera_angle += CAMERA_ANGLE
	if key == GLUT_KEY_RIGHT:
		yaw_camera_angle -= CAMERA_ANGLE
	if key == GLUT_KEY_UP:
		pitch_camera_angle += CAMERA_ANGLE
	if key == GLUT_KEY_DOWN:
		pitch_camera_angle -= CAMERA_ANGLE
	glutPostRedisplay()

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
