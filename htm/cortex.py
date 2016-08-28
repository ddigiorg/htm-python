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
		
		self.neurons = [ Neuron( idxX + numColumnsX * ( idxY + numColumnsY * idxN ),
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

		self.columns = [ Column( idxX,
                                 idxY, 
                                 self.numColumnsX,
                                 self.numColumnsY,
                                 self.numNeuronsPerColumn )
                         for idxX in range( self.numColumnsX )
                         for idxY in range( self.numColumnsY ) ]

		self.activeNeurons  = []
		self.winnerNeurons  = []
		self.predictNeurons = []

		self.activeDendrites   = []
		self.matchingDendrites = []

#		self.initRandomReceptiveFields( numInputs )
		self.initTopologicalReceptiveFields( 5, 5 )

	def initRandomReceptiveFields( self, numInputs ):
		for column in self.columns:
			numProxSynapses = int( numInputs * 0.5 )

			synAddresses = np.random.choice( numInputs, numProxSynapses, replace=False )
			synPermanences = np.random.random_integers( 20, 21, numProxSynapses )
			column.createDendrite( numInputs, synAddresses, synPermanences )

	# Make more efficient
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

			synAddresses = [ x + self.numColumnsX * y
                             for x in range( startX, endX )
                             for y in range( startY, endY ) ]

			synPermanences = np.random.random_integers( 20, 21, len( synAddresses ) )
			column.createDendrite( synAddresses, synPermanences )

	# Finish coding
	# Figure out how this is implemented by Numenta
	# Move this over to temporal memory?
	# Make more efficient
	def computeBasalDendriteActivity(self, active_neurons):
		self.active_dendrites = []

		inputs = np.zeros(self.num_neurons, dtype=np.int8)
		active_neuron_indices = [ neuron.idx for neuron in active_neurons]
		inputs[active_neuron_indices] = 1

		for column in self.columns:
			column.has_active_basalDendrites = False
			for neuron in column.neurons:
				for basal_dendrite in neuron.basalDendrites:
					bs_addresses = basal_dendrite.synAddresses
					bs_permanences = basal_dendrite.synPermanences

					if_connected = bs_permanences > 20 # BS_THRESHOLD.  Find a home for it
					values = np.logical_and(inputs[bs_addresses], if_connected)
					overlap = np.sum(values)

					if overlap > 39: # Segment activation threshold.  Find a home for it
#					if overlap > 0:
						self.active_dendrites.append(basal_dendrite)
						self.predict_neurons.append(neuron)
						column.has_active_basalDendrites = True
