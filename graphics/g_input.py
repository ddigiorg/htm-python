# g_input.py

from OpenGL.GL import *
from OpenGL.GLUT import *
from graphics.g_global import Flags, ViewParams

ESCAPE = '\x1b'

def mouseFunc(button, state, x, y):
	if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
		print(x, y)

# 22         if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
# 23             camera   = self.camera
# 24             scene    = self.scene
# 25             polygons = scene.polygons[1]
# 26 
# 27             selected = False
# 28             for polygon in polygons:
# 29                 lower_x = polygon.position[0] + camera.view_x
# 30                 upper_x = lower_x + polygon.size
# 31                 lower_y = polygon.position[1] + camera.view_y
# 32                 upper_y = lower_y + polygon.size
# 33 
# 34                 if lower_x <= x <= upper_x and lower_y <= y <= upper_y:
# 35                     scene.selected_polygon = polygon
# 36                     selected = True
# 37 
# 38             if not selected:
# 39                 scene.selected_polygon = None


def keyboardFunc(key, x, y):
	if key == ESCAPE.encode(): Flags.cleanGraphics = True
	if key == 'a'.encode(): ViewParams.viewUpdateX += ViewParams.viewUpdatesSpeed
	if key == 'd'.encode(): ViewParams.viewUpdateX -= ViewParams.viewUpdatesSpeed
	if key == 'w'.encode(): ViewParams.viewUpdateY += ViewParams.viewUpdatesSpeed
	if key == 's'.encode(): ViewParams.viewUpdateY -= ViewParams.viewUpdatesSpeed
	if key == 'p'.encode(): print("put continue flag here")

	glutPostRedisplay()
