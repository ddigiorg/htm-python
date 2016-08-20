import numpy as np

class SpatialPooler(object):

	def __init__(self):
		self.PS_THRESHOLD = 20
		self.ACTIVE_COLUMN_PERCENT = 0.02

	def compute(self, layer, axons):
		
		columns = layer.columns

		overlap = []
		num_active_columns = int( len(columns) * self.ACTIVE_COLUMN_PERCENT )

		# Overlap
		for column in columns:
			ps_addresses =  column.proximal_dendrite.synapse_addresses
			ps_permanences = column.proximal_dendrite.synapse_permanences

			if_connected = ps_permanences > self.PS_THRESHOLD
			values = np.logical_and( axons[ps_addresses], if_connected )
			overlap.append( np.sum(values) )

			column.is_active = False

		# Inhibition
		# TODO: Add random tiebreaker if multiple overlap scores are max

		for _ in range(num_active_columns):
			active_column = np.argmax(overlap)
			columns[active_column].is_active = True
			overlap[active_column] = 0

		# Learning
		# TODO: Complete learning
