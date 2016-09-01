# encoder.py

import numpy as np

class InputNeuron( object ):
	def __init__( self, idx ):
		self.idx = idx

		self.isActive = False

class InputLayer( object ):
	def __init__( self, dimensions ):
		self.numInputsX = dimensions[0]
		self.numInputsY = dimensions[1]

		self.neurons = [ InputNeuron(idxX + self.numInputsY * idxY)
                         for idxY in range( self.numInputsY ) 
                         for idxX in range( self.numInputsX ) ]

	def activeateInputs(self, lower, upper ):
		for neuron in self.neurons:
			if lower <= neuron.idx <= upper:
				neuron.isActive = True
			else:
				neuron.isActive = False
