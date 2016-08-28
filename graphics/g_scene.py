# g_scene.py

from graphics.g_global import ViewParams, SceneParams
import graphics.g_model as g_model

MAX_NUM_X = 25
MAX_NUM_Y = 25

def initScene( dimensions, encoder, layer ):
	numAssemblies = 2

	dataType = [""] * numAssemblies
	data = [None] * numAssemblies
	x = [0] * numAssemblies
	y = [0] * numAssemblies
	numX = [0] * numAssemblies
	numY = [0] * numAssemblies

	size = 10
	spacing = 1

	dataType[0] = "inputs"
	data[0] = encoder.inputs
	x[0] = 10
	y[0] = 10
	numX[0] = dimensions[0] # numInputsX
	numY[0] = dimensions[1] # numInputsY

	dataType[1] = "columns"
	data[1] = layer.columns
	x[1] = int( ViewParams.viewportWidth / 2 + 10 )
	y[1] = 10
	numX[1] = dimensions[2] # numColumnsX
	numY[1] = dimensions[3] # numColumnsY

	# Neurons
#	dataType[2] = "neurons"
#	x[2] = 10
#	y[2] = int( ViewParams.viewportHeight / 2 + 10 )
#	numX[2] = 
#	numy[2] = 

	for i in range( numAssemblies ):
#		if numX[i] > MAX_NUM_X:
#			numX[i] = MAX_NUM_X
#		if numY[i] > MAX_NUM_Y:
#			numY[i] = MAX_NUM_Y

		polygons = [ g_model.Square( idxX,
                                     idxY,
                                     x[i],
                                     y[i],
                                     size,
                                     spacing,
                                     data[i][idxX + numX[i] * idxY] )
                     for idxX in range(numX[i])
                     for idxY in range(numY[i]) ]

		SceneParams.assemblies.append( g_model.Assembly( polygons, dataType[i] ) )

def updateScene():
#	activeNeurons  = [ activeNeuron  for activeNeuron  in layer.activeNeurons  if activeNeuron.idx  < MAX_NUM_X ]
#	winnerNeurons  = [ winnerNeuron  for winnerNeuron  in layer.winnerNeurons  if winnerNeuron.idx  < MAX_NUM_X ]
#	predictNeurons = [ predictNeuron for predictNeuron in layer.predictNeurons if predictNeuron.idx < MAX_NUM_X ]

	for assembly in SceneParams.assemblies:
		if assembly.dataType == "inputs":
			for polygon in assembly.polygons:
				if polygon.data == 1:
					polygon.color = [0.0, 0.8, 0.0] # Active (Green)
				else:
					polygon.color = [0.3, 0.3, 0.3] # Inactive (Grey)

		elif assembly.dataType == "columns":
			for polygon in assembly.polygons:
				if polygon.data.isActive == True:
					polygon.color = [0.0, 0.8, 0.0] # Active (Green)
				else:
					polygon.color = [0.3, 0.3, 0.3] # Inactive (Grey)


#		elif assembly.dataType == "neurons":
#			for polygon in assembly.polygons:
#				polygon.color = [0.2, 0.2, 0.2]
#
#			for activeNeuron in activeNeurons:
#				assembly.polygons[activeNeuron.idx].color = [0.0, 0.8, 0.0] # Active (Green)
#
#			for winnerNeuron in winnerNeurons:
#				assembly.polygons[winnerNeuron.idx].color = [0.0, 0.0, 0.8] # Winner (Blue) 
#
#			for predictNeuron in predictNeurons:
#				assembly.polygons[predictNeuron.idx].color = [0.8, 0.0, 0.8] # Predict (Violet) 

	selectedPolygon = SceneParams.selectedPolygon
	if selectedPolygon:
		updateColors = [ 0.2, 0.2, 0.2 ]
		selectedPolygon.color = [ sum(i) for i in zip( selectedPolygon.color, updateColors ) ]

		selectedAssembly = SceneParams.selectedAssembly
		if selectedAssembly.dataType == "columns":
			synAddresses = selectedPolygon.data.dendrite.synAddresses
			assembly = SceneParams.assemblies[0]
			for synAddress in synAddresses:
				updateColors = [ 0.2, 0.2, 0.2 ]
				assembly.polygons[synAddress].color = [ sum(i) for i in zip( assembly.polygons[synAddress].color, updateColors ) ]

#		idx_x = selected_polygon.idx_x
#		idx_y = selected_polygon.idx_y
#		neuron = layer.columns[idx_x].neurons[idx_y]
#		synapses = [basal_dendrite.synapse_addresses for basal_dendrite in neuron.basal_dendrites]
#		print(synapses)
#		self.selected_polygon = None
 
