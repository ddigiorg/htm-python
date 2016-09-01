# g_global.py

class Flags(object):
	pause = False
	cleanGraphics = False

class ViewParams(object):
	viewportX = 0
	viewportY = 0
	viewportWidth = 800
	viewportHeight = 800

	viewX = 0.0
	viewY = 0.0
	viewZ = 0.0
	viewSpeed = 10.0

	viewMatrix = [1.0, 0.0, 0.0, 0.0,
                  0.0, 1.0, 0.0, 0.0,
                  0.0, 0.0, 1.0, 0.0,
                  0.0, 0.0, 0.0, 1.0]

	projectionMatrix = [0.0] * 16

class SceneParams(object):
	assemblies = []
	selectedAssembly = None
	selectedPolygon = None

class OpenGLParams(object):
	windowID = None
	windowName = "Test"

	meshBuffer = None
	positionBuffer = None
	colorBuffer = None

	vertexShader = None
	fragmentShader = None
	shaderID = None
	shaderMeshLocation = None
	shaderPositionLocation = None
	shaderColorLocation = None
	shaderProjectionMatrixLocation = None
	shaderViewMatrixLocation = None

