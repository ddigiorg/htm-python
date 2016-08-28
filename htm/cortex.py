# cortex.py

import numpy as np

class Dendrite( object ):
#	__slots__ = [ 'synAddresses', 'synPermanences' ]
	def __init__( self, idx, parent, addresses, permanences ):
		self.idx = idx
		self.parent = parent
		self.synAddresses = addresses
		self.synPermanences = permanences

class Neuron( object ):
	def __init__( self, idx, column ):
		self.idx = idx
		self.column = column
		self.dendrites = []

	def createDendrite( self, addresses, permanences ):
		idx = len( self.dendrites )
		self.dendrites.append( Dendrite( idx, self, addresses, permanences ) )

class Column( object ):
	def __init__( self, idxX, idxY, numColumnsX, numColumnsY, numNeuronsPerColumn ):
		self.idxX = idxX
		self.idxY = idxY
		
		self.neurons = [ Neuron( idxN + numColumnsX * ( idxX + numColumnsY * idxY ),
                                 self )
                         for idxN in range( numNeuronsPerColumn ) ]

		self.dendrite = None

		self.isActive = False
		self.hasActiveBasalDendrites = False

	def createDendrite( self, addresses, permanences ):
		self.dendrite = Dendrite( 0, self, addresses, permanences )

class Layer3b( object ):
	def __init__( self, dimensions ):
		self.numInputsX = dimensions[0]
		self.numInputsY = dimensions[1]
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

		self.activeColumns = []

		self.activeNeurons  = []
		self.winnerNeurons  = []
		self.predictNeurons = []

		self.activeDendrites   = []
		self.matchingDendrites = []

		receptFieldX = int( self.numInputsX / 5 )
		receptFieldY = int( self.numInputsY / 5 )
		self.initTopologicalReceptiveFields( receptFieldX, receptFieldY )

	def initTopologicalReceptiveFields(self, sizeX, sizeY):
		for column in self.columns:
			originX = column.idxX
			originY = column.idxY

			startX = originX - sizeX 
			startY = originY - sizeX

			if startX < 0: startX = 0
			if startY < 0: startY = 0

			endX = originX + sizeX + 1
			endY = originY + sizeY + 1

			if endX > self.numInputsX: endX = self.numInputsX
			if endY > self.numInputsY: endY = self.numInputsY

			synAddresses = [ idxX + self.numColumnsX * idxY
                             for idxY in range( startY, endY )
                             for idxX in range( startX, endX ) ]

			synPermanences = np.random.random_integers( 20, 21, len( synAddresses ) )
			column.createDendrite( synAddresses, synPermanences )

	# Finish coding
	# Figure out how this is implemented by Numenta
	# Move this over to temporal memory?
	# Make more efficient
	def computeBasalDendriteActivity( self ):
		self.activeDendrites = []

		inputs = np.zeros( self.numColumnsX * 
                           self.numColumnsY *
                           self.numNeuronsPerColumn,
                           dtype=np.int8)

		activeNeuronIndices = [ neuron.idx for neuron in self.activeNeurons ]
		inputs[activeNeuronIndices] = 1

		for column in self.columns:
			column.hasActiveBasalDendrites = False
			for neuron in column.neurons:
				for dendrite in neuron.dendrites:
					bSynAddresses = dendrite.synAddresses
					bSynPermanences = dendrite.synPermanences

					if_connected = bSynPermanences > self.bSynThreshold
					values = np.logical_and( inputs[bSynAddresses], if_connected )
					overlap = np.sum( values )

					if overlap > 10: # Segment activation threshold.  Find a home for it
						self.activeDendrites.append( dendrite )
						self.predictNeurons.append( neuron )
						column.hasActiveBasalDendrites = True
