# cortex.py

import numpy as np

class Synapse( object ):
	def __init__( self, idx, parent, connection, permanence ):
		self.idx = idx
		self.parent = parent

		self.connection = connection
		self.permanence = permanence

class Dendrite( object ):
	def __init__( self, idx, parent ):
		self.idx = idx
		self.parent = parent

		self.synapses = []

class Neuron( object ):
	def __init__( self, idx, column ):
		self.idx = idx
		self.column = column

		self.dendrites = []

		self.isActive = False
		self.isWinner = False
		self.isPredict = False

class Column( object ):
	def __init__( self, idxX, idxY, numColumnsX, numColumnsY, numNeuronsPerColumn ):
		self.idx = idxX + numColumnsY * idxY
		
		self.neurons = [ Neuron( idxN + numColumnsX * self.idx, self )
                         for idxN in range( numNeuronsPerColumn ) ]
		self.dendrites = []

		self.isActive = False
		self.hasActiveBasalDendrites = False

class Layer3b( object ):
	def __init__( self, dimensions ):
		self.numColumnsX = dimensions[2]
		self.numColumnsY = dimensions[3]
		self.numNeuronsPerColumn = dimensions[4]
		self.percentActiveColumns = 0.02
		self.numActiveColumns = int( self.numColumnsX *
                                     self.numColumnsY *
                                     self.percentActiveColumns )
		if self.numActiveColumns <= 0:
			self.numActiveColumns = 1
		self.pSynThreshold = 20
		self.bSynThreshold = 20

		self.columns = [ Column( idxX,
                                 idxY, 
                                 self.numColumnsX,
                                 self.numColumnsY,
                                 self.numNeuronsPerColumn )
                         for idxY in range( self.numColumnsY )
                         for idxX in range( self.numColumnsX ) ]

#		self.activeNeurons  = []
#		self.winnerNeurons  = []
		self.activeDendrites   = []
		self.matchingDendrites = []



# Functions

def initReceptiveFields( layerIn, layer ):
	inputNeurons = layerIn.neurons
	numInputsX = layerIn.numInputsX
	numInputsY = layerIn.numInputsY

	columns = layer.columns
	numColumnsX = layer.numColumnsX
	numColumnsY = layer.numColumnsY

	sizeX = int( numInputsX / 5 )
	sizeY = int( numInputsY / 5 )

	for column in columns:
		originX = int( column.idx % numColumnsY )
		originY = int( column.idx / numColumnsY )

		startX = originX - sizeX 
		startY = originY - sizeY

		if startX < 0: startX = 0
		if startY < 0: startY = 0

		endX = originX + sizeX + 1
		endY = originY + sizeY + 1

		if endX > numInputsX: endX = numInputsX
		if endY > numInputsY: endY = numInputsY

		synConnections = [ inputNeurons[idxX + numColumnsX * idxY]
                           for idxY in range( startY, endY )
                           for idxX in range( startX, endX ) ]

		numSynapses = len( synConnections )
		synPermanences = np.random.random_integers( 20, 21, numSynapses )

		createDendrite( column )
		dendrite = column.dendrites[-1]
		createSynapses( numSynapses, dendrite, synConnections, synPermanences )

def createDendrite( parent ):
	idxD = len( parent.dendrites )
	parent.dendrites.append( Dendrite( idxD, parent ) )

def createSynapse( dendrite, connection, permanence ):
	idxS = len( dendrite.synapses )
	dendrite.synapses.append( Synapse( idxS, dendrite, connection, permanence  ) )

def createSynapses( numSynapses, dendrite, synConnections, synPermanences):
	[ createSynapse( dendrite, synConnections[i], synPermanences[i] ) for i in range( numSynapses ) ]

def resetNeuronStates( layer ):
	prevWinnerNeurons = []

	for column in layer.columns:
		for neuron in column.neurons:
			if neuron.isWinner == True:
				prevWinnerNeurons.append( neuron )

			neuron.isActive = False
			neuron.isWinner = False
			neuron.isPredict = False

	return prevWinnerNeurons

def computeOverlap( dendrite, synThreshold ):
	overlap = 0
	for synapse in dendrite.synapses:
		if synapse.permanence > synThreshold and synapse.connection.isActive:
			overlap += 1

	return overlap

def computeDendriteActivity( layer ):
	columns = layer.columns

	for column in columns:
		column.hasActiveBasalDendrites = False
		for neuron in column.neurons:
			for dendrite in neuron.dendrites:
				overlap = computeOverlap( dendrite, layer.bSynThreshold )

				if overlap > 10: # Segment activation threshold.  Find a home for it
					layer.activeDendrites.append( dendrite )
					column.hasActiveBasalDendrites = True
					neuron.isPredict = True
