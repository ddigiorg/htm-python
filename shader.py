# archlinux: certain opengl functions won't work on Windows without extensive tinkering
# python 3.5.1
# pyopengl 3.0 Mesa 11.1.2
# glsl 1.30

# http://cyrille.rossant.net/shaders-opengl/

from OpenGL.GL import *

# Vertex shader
VertexShader = """
#version 130

in vec3 vertex_template;
in vec3 vertex_position;
in vec3 vertex_color_in;

out vec3 vertex_color_out;

void main()
{
	// Output position of the vertex
	// gl_Position.xyz = vertex_template * vertex_position;
	// gl_Position.w = 1.0;
	// gl_Position = vec4(vertex_in_cube_position, 1.0f);

	vec3 shit = vertex_template.xyz + vertex_position.xyz;
	gl_Position = vec4(shit, 1.0f);

	// Output color
	// vertex_out_cube_color = vertex_in_cube_color;
	vertex_color_out = vertex_color_in;
}
"""

# Fragment shader
FragmentShader = """
#version 130

// 4D vector containing RGBA components of pixel color
//in vec4 vertex_out_cube_color;

in vec3 vertex_color_out;

// 4D vector containing RGBA components of pixel color
//out vec4 fragment_out_cube_color;

out vec3 color;

void main(){
	// Output color = color of the texture at the specified UV
	// fragment_out_cube_color = vertex_out_cube_color;

	color = vertex_color_out;
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
