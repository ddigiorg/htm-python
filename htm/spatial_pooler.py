#spatial_pooler.py

import numpy as np

class SpatialPooler(object):

	def __init__(self):
		self.PS_THRESHOLD = 20
		self.ACTIVE_COLUMN_PERCENT = 0.02

	def compute(self, axons, layer):
		columns = layer.columns

		overlap = []

		# !MAKE THIS A LAYER() ATTRIBUTE!
		numActiveColumns = int( layer.numColumnsX * layer.numColumnsY * self.ACTIVE_COLUMN_PERCENT )

		# Overlap
		for column in columns:
			synAddresses =  column.dendrite.synAddresses
			synPermanences = column.dendrite.synPermanences

			if_connected = synPermanences > self.PS_THRESHOLD
			values = np.logical_and( axons[synAddresses], if_connected )
			overlap.append( np.sum(values) )

			column.isActive = False

		# Inhibition !ADD RANDOM TIEBREAKER!
		for _ in range(numActiveColumns):
			activeColumn = np.argmax(overlap)
			columns[activeColumn].isActive = True
			overlap[activeColumn] = 0

		# Learning

#		print( [column.idx for column in columns if column.is_active == True] )
