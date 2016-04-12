from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

glutInit()
window = glutCreateWindow("test")
print(glGetString(GL_SHADING_LANGUAGE_VERSION))
print(glGetString(GL_VERSION))
glutDestroyWindow(window)
