# g_scene.py

from graphics.g_global import ViewParams, SceneParams
import graphics.g_model as g_model

MAX_NUM_X = 25
MAX_NUM_Y = 25

def initScene( layerIn, layer ):
	numAssemblies = 3

	dataType = [""] * numAssemblies
	x = [0] * numAssemblies
	y = [0] * numAssemblies
	numX = [0] * numAssemblies
	numY = [0] * numAssemblies
	spacingX = [0] * numAssemblies
	spacingY = [0] * numAssemblies
	data = [None] * numAssemblies

	size = 10

	dataType[0] = "inputs"
	x[0] = 10
	y[0] = 10
	numX[0] = layerIn.numInputsX
	numY[0] = layerIn.numInputsY
	spacingX[0] = 1
	spacingY[0] = 1
	data[0] = layerIn.neurons

	dataType[1] = "columns"
	x[1] = int( ViewParams.viewportWidth / 2 + 10 )
	y[1] = 10
	numX[1] = layer.numColumnsX
	numY[1] = layer.numColumnsY
	spacingX[1] = 1
	spacingY[1] = 1
	data[1] = layer.columns

	# Neurons
	dataType[2] = "neurons"
	x[2] = 10
	y[2] = int( ViewParams.viewportHeight / 2 + 10 )
	numX[2] = 50
	numY[2] = layer.numNeuronsPerColumn
	spacingX[2] = 5
	spacingY[2] = 1
	data[2] = [layer.columns[c].neurons[n]
               for n in range( numY[2] )
               for c in range( numX[2] ) ]

	for i in range( numAssemblies ):
#		if numX[i] > MAX_NUM_X:
#			numX[i] = MAX_NUM_X
#		if numY[i] > MAX_NUM_Y:
#			numY[i] = MAX_NUM_Y

		polygons = [ g_model.Square( idxX,
                                     idxY,
                                     x[i],
                                     y[i],
                                     spacingX[i],
                                     spacingY[i],
                                     size,
                                     data[i][idxX + numX[i] * idxY] )
                     for idxY in range( numY[i] )
                     for idxX in range( numX[i] ) ]

		SceneParams.assemblies.append( g_model.Assembly( polygons, dataType[i] ) )

def updateScene( layerIn, layer ):
	for assembly in SceneParams.assemblies:
		if assembly.dataType == "inputs":
			for polygon in assembly.polygons:
				if polygon.data.isActive:
					polygon.color = [0.0, 0.6, 0.0] # Active (Green)
				else:
					polygon.color = [0.3, 0.3, 0.3] # Inactive (Grey)

		elif assembly.dataType == "columns":
			for polygon in assembly.polygons:
				if polygon.data.isActive:
					polygon.color = [0.0, 0.6, 0.0] # Active (Green)
				else:
					polygon.color = [0.3, 0.3, 0.3] # Inactive (Grey)

		elif assembly.dataType == "neurons":
			for polygon in assembly.polygons:
				if polygon.data.isPredict:
					polygon.color = [0.6, 0.0, 0.6] # Predict (Violet)
				elif polygon.data.isWinner:
					polygon.color = [0.0, 0.0, 0.6] # Winner (Blue)
				elif polygon.data.isActive:
					polygon.color = [0.0, 0.6, 0.0] # Active (Green)
				else:
					polygon.color = [0.3, 0.3, 0.3] # Inactive (Grey)

	selectedPolygon = SceneParams.selectedPolygon
	if selectedPolygon:
		updateColors = [ 0.4, 0.4, 0.4 ]
		selectedPolygon.color = [ sum(i) for i in zip( selectedPolygon.color, updateColors ) ]

		selectedAssembly = SceneParams.selectedAssembly
		if selectedAssembly.dataType == "columns":
			synapses = selectedPolygon.data.dendrites[-1].synapses
			assembly = SceneParams.assemblies[0]
			for synapse in synapses:
				idxN = synapse.connection.idx
				assembly.polygons[idxN].color = [ sum(i) for i in zip( assembly.polygons[idxN].color, updateColors ) ]
