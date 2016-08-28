# encoder.py

import numpy as np

class Encoder( object ):
	def __init__( self, numInputsX, numInputsY ):
		self.numInputsX = numInputsX
		self.numInputsY = numInputsY

		self.inputs = np.zeros( (2, numInputsY * numInputsX ), dtype=np.int8 )
		self.inputs[0, 0:  5] = 1 
		self.inputs[1, 5: 10] = 1 
