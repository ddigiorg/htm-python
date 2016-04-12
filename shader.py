# archlinux: certain opengl functions won't work on Windows without extensive tinkering
# python 3.5.1
# pyopengl 3.1

# http://cyrille.rossant.net/shaders-opengl/

from OpenGL.GL import *
#from OpenGL.GLUT import *
#from OpenGL.GLU import *

# Vertex shader
VertexShader = """
#version 130 core

// Input vertex data
layout(location = 0) in vec3 squareVertices; //* UPDATE WITH TEMPLATE STUFF
layout(location = 1) in vec3 xyz;
layout(location = 2) in vec4 in_color;

// Output data
out vec4 out_color;

void main()
{
	float particleSize = xyz.w; // because we encoded it this way.
	vec3 particleCenter_wordspace = xyz.xyz;
	
	vec3 vertexPosition_worldspace = particleCenter_wordspace + squareVertices.x + squareVertices.y;

	// Output position of the vertex
	gl_Position = vec4(vertexPosition_worldspace, 1.0f);

	// Output color
	out_color = in_color;
}
"""

# Fragment shader
FragmentShader = """
#version 130 core

// 4D vector containing RGBA components of pixel color
in vec4 in_color;

// 4D vector containing RGBA components of pixel color
out vec4 out_color;

void main(){
	// Output color = color of the texture at the specified UV
	out_color = in_color;
}
"""

# Compile a vertex or fragment shader from source
def compile_shader(name):
	global VertexShader, FragmentShader
	if name == "vertex":
		source = VertexShader
		shader_type = GL_VERTEX_SHADER
	elif name == "fragment":
		source = FragmentShader
		shader_type = GL_FRAGMENT_SHADER        
	shader = glCreateShader(shader_type)
	glShaderSource(shader, source)
	glCompileShader(shader)
	# check compilation error
	result = glGetShaderiv(shader, GL_COMPILE_STATUS)
	if not(result):
		raise RuntimeError(glGetShaderInfoLog(shader))
	return shader

# Create a shader program with from compiled shaders
def link_shader_program(vertex_shader, fragment_shader):
	program = glCreateProgram()
	glAttachShader(program, vertex_shader)
	glAttachShader(program, fragment_shader)
	glLinkProgram(program)
	# check linking error
	result = glGetProgramiv(program, GL_LINK_STATUS)
	if not(result):
		raise RuntimeError(glGetProgramInfoLog(program))
	return program
