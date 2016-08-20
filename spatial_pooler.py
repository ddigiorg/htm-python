import numpy as np

class SpatialPooler(object):

	def __init__(self):
		self.PS_THRESHOLD = 20
		self.ACTIVE_COLUMN_PERCENT = 0.02

	def compute(self, layer, axons):
		
		columns = layer.columns

		overlap = []
		active_columns = []
		num_active_columns = int( len(columns) * self.ACTIVE_COLUMN_PERCENT )
#		num_active_columns = 1

		overlap = list( range( len(columns) ) )

		# Overlap
		# TODO: Make faster
		for column in columns:
			proximal_synapses = column.proximal_dendrite.synapses
			
			ps_addresses = np.array( [ps.address for ps in proximal_synapses] )
			ps_permanences = np.array( [ps.permanence for ps in proximal_synapses] )

			if_connected = ps_permanences > self.PS_THRESHOLD
			values = np.logical_and( axons[ps_addresses], if_connected )
			overlap.append( np.sum(values) )

		# Inhibition
		# TODO: Add random tiebreaker if multiple overlap scores are max
		for _ in range(num_active_columns):
			active_column = np.argmax(overlap)
			active_columns.append(active_column)
			del overlap[active_column]

		# Learning
		# TODO: Complete learning

#		print(active_columns)
