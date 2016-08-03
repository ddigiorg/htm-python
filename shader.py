# archlinux: certain opengl functions won't work on Windows without extensive tinkering
# python 3.5.1
# pyopengl 3.0 Mesa 11.1.2
# glsl 1.30

# http://cyrille.rossant.net/shaders-opengl/

from OpenGL.GL import *

# Vertex shader
VertexShader = """
#version 130

in vec3 templateVS;
in vec3 positionVS;
in vec3 colorVS_in;

out vec3 colorVS_out;

uniform mat4 projection;
uniform mat4 view;

void main()
{
	vec3 vertex_position = templateVS.xyz + positionVS.xyz;
	gl_Position = projection * view * vec4(vertex_position, 1.0f);

	colorVS_out = colorVS_in;
}
"""

# Fragment shader
FragmentShader = """
#version 130

in vec3 colorVS_out;

out vec3 colorFS_out;

void main()
{
	colorFS_out = colorVS_out;
}
"""

# Compile a vertex or fragment shader from source
def compile_shader(name):
	global VertexShader, FragmentShader
	if name == "VS":
		source = VertexShader
		shader_type = GL_VERTEX_SHADER
	elif name == "FS":
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
