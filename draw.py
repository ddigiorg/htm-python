# draw.py

# http://www.opengl-tutorial.org/intermediate-tutorials/billboards-particles/particles-instancing/
# https://github.com/opengl-tutorials/ogl/blob/master/tutorial18_billboards_and_particles/tutorial18_particles.cpp
# http://www.paridebroggi.com/2015/06/optimized-cube-opengl-triangle-strip.html
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
n_cubes_x = None 
n_cubes_y = None
n_cubes_z = None
n_cubes   = None
cubes_world_positions = None
cubes_world_colors    = None
CUBE_SPACING = 4

# Camera global variables
frustum_matrix     = None
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
shaders_frustumID         = None
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
						GLUT_ALPHA  |		# Alpha Components
						GLUT_DEPTH)  		# Depth Buffer
	glutInitWindowSize(width, height)		# Initialize window size
	glutInitWindowPosition(0, 0)			# Window at upper left corner of screen
	window = glutCreateWindow("HTM")		# Create window with name "HTM"
	glutKeyboardFunc(keyPressed)			# Register function when keyboard pressed
	glutSpecialFunc(keyPressed)				# Register function when keyboard pressed
	glClearColor(0.0, 0.0, 0.0, 1.0)		# Black background
	glClearDepth(1.0)						# Depth Buffer setup
	glDepthFunc(GL_LESS)					# The type of Depth Testing
	glEnable(GL_DEPTH_TEST)					# Enable Depth Testing
	glEnable(GL_CULL_FACE)					# Enable Culling
#	glDepthFunc(GL_LESS)					# Accept fragment if closer to the camera than the former one
	glShadeModel(GL_SMOOTH)					# Select Smooth Shading
	glHint(GL_PERSPECTIVE_CORRECTION_HINT,
               GL_NICEST)	                # *Set Perspective Calculations to most accurate
	glColor4f(1.0, 6.0, 6.0, 1.0)			# *FIGURE OUT WHAT THIS DOES

def runMainGLLoop():
	glutMainLoop()                          # Start event processing engine


def initCubes(nx, ny, nz):
	global n_cubes_x, n_cubes_y, n_cubes_z, n_cubes, cubes_world_positions, cubes_world_colors
	global template_data, position_data, color_data

	n_cubes_x = nx
	n_cubes_y = ny 
	n_cubes_z = nz
	n_cubes   = n_cubes_x * n_cubes_y * n_cubes_z
	cubes_world_positions = np.array([[[None]*n_cubes_z]*n_cubes_y]*n_cubes_x)
	cubes_world_colors    = np.array([[[None]*n_cubes_z]*n_cubes_y]*n_cubes_x)

	template_list = [
		 1,  1,  1,  1,  1, -1, -1,  1, -1,
		 1,  1,  1, -1,  1, -1, -1,  1,  1,
		-1,  1,  1, -1, -1,  1,  1, -1,  1,
		 1,  1,  1, -1,  1,  1,  1, -1,  1,
		-1, -1, -1, -1, -1,  1, -1,  1,  1,
		-1, -1, -1, -1,  1,  1, -1,  1, -1,
		 1,  1, -1, -1, -1, -1, -1,  1, -1,
		 1,  1, -1,  1, -1, -1, -1, -1, -1,
		 1,  1,  1,  1, -1, -1,  1,  1, -1,
		 1, -1, -1,  1,  1,  1,  1, -1,  1,
		 1, -1,  1, -1, -1, -1,  1, -1, -1,
		 1, -1,  1, -1, -1,  1, -1, -1, -1]
	
	position_list = [0] * n_cubes * POSITION_SIZE
	
	i = 0
	for z in range(n_cubes_z):
		for y in range(n_cubes_y):
			for x in range(n_cubes_x):	
				cubes_world_positions[x][y][z] = [0 + x * CUBE_SPACING, 0 + y * CUBE_SPACING, 0 + z * CUBE_SPACING]
				position_list[i*POSITION_SIZE  ] = cubes_world_positions[x][y][z][0] # cube x world position
				position_list[i*POSITION_SIZE+1] = cubes_world_positions[x][y][z][1] # cube y world position
				position_list[i*POSITION_SIZE+2] = cubes_world_positions[x][y][z][2] # cube z world position
				cubes_world_colors[x][y][z] = [0.5, 0.5, 0.5]
				i += 1

	template_data = np.array(template_list, dtype=np.int16)
	position_data = np.array(position_list, dtype=np.int16)

def initShaders():
	global shaders_programID, shaders_frustumID, shaders_viewID, shaders_template_location, shaders_position_location, shaders_color_location
	vertex_shader   = shader.compile_shader("VS")
	fragment_shader = shader.compile_shader("FS")
	shaders_programID = shader.link_shader_program(vertex_shader, fragment_shader)     

	shaders_template_location = glGetAttribLocation(shaders_programID, "templateVS")
	shaders_position_location = glGetAttribLocation(shaders_programID, "positionVS")
	shaders_color_location    = glGetAttribLocation(shaders_programID, "colorVS_in")

	shaders_frustumID = glGetUniformLocation(shaders_programID, "frustum")
	shaders_viewID = glGetUniformLocation(shaders_programID, "view" )

def initCamera():
	global width, height
	global frustum_matrix
	view_angle = 60.0
	aspect_ratio = width/height
	z_near = 1.0
	z_far  = 10.0
	
	frustum_matrix = [1.0/np.tan(view_angle), 0.0,                             0.0,                              0.0,
					  0.0,                    aspect_ratio/np.tan(view_angle), 0.0,                              0.0,
					  0,0,                    0.0,                             (z_far+z_near)/(z_far-z_near),    0.0,
					  0.0,                    0.0,                             -2.0*z_far*z_near/(z_far-z_near), 0.0]

def initVBOs():
	global template_buffer, position_buffer, color_buffer, template_data, position_data
      
	# Opengl VBO vertex template buffer created, bound, and filled with vertex template data
	template_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, template_buffer)
	glBufferData(GL_ARRAY_BUFFER, template_data, GL_STATIC_DRAW)

	# Opengl VBO cube position buffer created, bound, and filled with cube position data
	position_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, position_buffer)
	glBufferData(GL_ARRAY_BUFFER, position_data, GL_STATIC_DRAW)

	# Opengl VBO cube color buffer created, bound, and left empty
	color_buffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
	glBufferData(GL_ARRAY_BUFFER, None, GL_STREAM_DRAW)

def updateCubes(array_3d):
	global color_data

	color_list = [0] * n_cubes * COLOR_SIZE

	i = 0
	for z in range(n_cubes_z):
		for y in range(n_cubes_y):
			for x in range(n_cubes_x):	
				color_list[i*COLOR_SIZE  ] = array_3d[x][y][z][0] # cube r color
				color_list[i*COLOR_SIZE+1] = array_3d[x][y][z][1] # cube g color
				color_list[i*COLOR_SIZE+2] = array_3d[x][y][z][2] # cube b color
				i += 1
	
	color_data = np.array(color_list, dtype=np.float16)

def updateCamera():
	global view_matrix
	view_matrix = [1.0,          0.0,          0.0,          0.0,
				   0.0,          1.0,          0.0,          0.0,
				   0.0,          0.0,          1.0,          0.0,
				   x_camera_pos, y_camera_pos, z_camera_pos, 1.0]

def updateScene():
	global n_cubes, position_buffer, color_buffer, position_data, color_data
	global shaders_programID, shaders_frustumID, shaders_viewID, shaders_template_location, shaders_position_location, shaders_color_location
	global frustum_matrix, view_matrix

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	# Opengl VBO cube color buffer bound, "orphaned", and filled with data
	glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
	glBufferData(GL_ARRAY_BUFFER, color_data, GL_STREAM_DRAW)
	#glBufferSubData(GL_ARRAY_BUFFER, 0, n_cubes * sys.getsizeof(GLfloat) * 4, color_data)  <-- try to get working! orphaning not working

	# Get shader ID
	glUseProgram(shaders_programID)
	
	# Update shader with frustum and view matrix
	glUniformMatrix4fv(shaders_frustumID, 1, False, frustum_matrix)
	glUniformMatrix4fv(shaders_viewID, 1, False, view_matrix)

	# Shader attribute buffer: vertices template
	glEnableVertexAttribArray(shaders_template_location)
	glBindBuffer(GL_ARRAY_BUFFER, template_buffer)
	glVertexAttribPointer(shaders_template_location, VERTEX_SIZE, GL_SHORT, False, 0, None)

	# Shader attribute buffer: cube positions
	glEnableVertexAttribArray(shaders_position_location)
	glBindBuffer(GL_ARRAY_BUFFER, position_buffer)
	glVertexAttribPointer(shaders_position_location, POSITION_SIZE, GL_SHORT, False, 0, None)

	# Shader attribute buffer: cube colors
	glEnableVertexAttribArray(shaders_color_location)
	glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
	glVertexAttribPointer(shaders_color_location, COLOR_SIZE, GL_HALF_FLOAT, True, 0, None) # normalized for unsigned char

	# * ?????????? For instancing... figure out what this does
	glVertexAttribDivisor(0, 0)
	glVertexAttribDivisor(1, 1)
	glVertexAttribDivisor(2, 1)

	# Draw cubes
	glCullFace(GL_BACK)
	glDrawArraysInstanced(GL_TRIANGLES, 0, 9*12, n_cubes) # try GL_TRIANGLE_STRIP with elements, make 9*12 more explicit!
	

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
