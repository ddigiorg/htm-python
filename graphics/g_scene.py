# g_scene.py

from graphics.g_global import ViewParams, SceneParams
import graphics.g_model as g_model

MAX_NUM_X = 25
MAX_NUM_Y = 25

def initScene( encoder, layer ):
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
	numX[0] = encoder.numInputsX
	numY[0] = encoder.numInputsY
	spacingX[0] = 1
	spacingY[0] = 1
	data[0] = encoder.inputs[0] #TODO: Consider removing

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

def updateScene( inputs, layer ):
#	activeNeurons  = [ activeNeuron  for activeNeuron  in layer.activeNeurons  if activeNeuron.idx  < MAX_NUM_X ]
#	winnerNeurons  = [ winnerNeuron  for winnerNeuron  in layer.winnerNeurons  if winnerNeuron.idx  < MAX_NUM_X ]
#	predictNeurons = [ predictNeuron for predictNeuron in layer.predictNeurons if predictNeuron.idx < MAX_NUM_X ]

	for assembly in SceneParams.assemblies:
		if assembly.dataType == "inputs":
			for polygon in assembly.polygons:
				idx = polygon.idxX + layer.numInputsX * polygon.idxY # TODO: Clean this up
				if inputs[idx] == 1:
					polygon.color = [0.0, 0.6, 0.0] # Active (Green)
				else:
					polygon.color = [0.3, 0.3, 0.3] # Inactive (Grey)

		elif assembly.dataType == "columns":
			for polygon in assembly.polygons:
				if polygon.data in layer.activeColumns:
					polygon.color = [0.0, 0.6, 0.0] # Active (Green)
				else:
					polygon.color = [0.3, 0.3, 0.3] # Inactive (Grey)

		# TODO: Make more efficient
		elif assembly.dataType == "neurons":
			for polygon in assembly.polygons:
				if polygon.data in layer.predictNeurons:
					polygon.color = [0.6, 0.0, 0.6] # Predict (Violet)
				elif polygon.data in layer.winnerNeurons:
					polygon.color = [0.0, 0.0, 0.6] # Winner (Blue)
				elif polygon.data in layer.activeNeurons:
					polygon.color = [0.0, 0.6, 0.0] # Active (Green)
				else:
					polygon.color = [0.3, 0.3, 0.3] # Inactive (Grey)

	selectedPolygon = SceneParams.selectedPolygon
	if selectedPolygon:
		updateColors = [ 0.4, 0.4, 0.4 ]
		selectedPolygon.color = [ sum(i) for i in zip( selectedPolygon.color, updateColors ) ]

		selectedAssembly = SceneParams.selectedAssembly
		if selectedAssembly.dataType == "columns":
			synAddresses = selectedPolygon.data.dendrite.synAddresses
			assembly = SceneParams.assemblies[0]
			for synAddress in synAddresses:
				assembly.polygons[synAddress].color = [ sum(i) for i in zip( assembly.polygons[synAddress].color, updateColors ) ]

#		if selectedAssembly.dataType == "neurons":
#			dendrites = [dendrite.synAddresses for dendrite in selectedPolygon.data.dendrites]
#			for dendrite in dendrites:
#				for synapse in dendrite:
#					selectedAssembly.polygons[synapse].color = [ sum(i)
#                                                                 for i in zip( selectedAssembly.polygons[synapse].color,
#                                                                               updateColors ) ]	
