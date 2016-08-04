import numpy as np

# Synapse Variables
s_threshold = 20
s_learning_rate = 1
s_permanence_lower = 0
s_permanence_upper = 99

class Layer3b(object):

	"""CLEAN THIS UP"""
	def __init__(self, num_inputs, num_columns, num_cells, threshold=s_threshold):

		ps_connectivity = 0.5 # put outside of layer3?
		active_columns_percent = 0.2 #!!!

		self.num_columns  = num_columns #!!!
		self.num_psynapses = int(num_inputs * ps_connectivity) #!!!
		self.s_threshold = s_threshold #!!!
#		self.learning_rate = 
#		self.s_permanence_lower = 
#		self.s_permanence_upper = 
		self.num_active_columns = int(np.ceil(num_columns * active_columns_percent))

		layer_shape = (num_columns, num_cells)
		ps_shape = (num_columns, self.num_psynapses) #!!!

		# Layer3b Data Variables
		self.cells_active  = np.zeros(layer_shape, dtype=np.int8)
		self.cells_predict = np.zeros(layer_shape, dtype=np.int8)
		self.cells_learn   = np.zeros(layer_shape, dtype=np.int8)

		# Proximal Synapse Data Variables
		self.ps_addresses = np.zeros(ps_shape, dtype=np.int8)		
		for c in range(num_columns):
			self.ps_addresses[c] = np.random.choice(num_inputs, num_inputs * ps_connectivity, replace=False)
		self.ps_permanences = np.random.random_integers(threshold, threshold + 1, ps_shape)

		# Basal Synapse Data Variables
		self.bs_addresses = np.full(layer_shape, None, dtype=object)
		self.bs_permanences = np.full(layer_shape, None, dtype=object)


	"""CLEAN THIS UP"""
	def runSpatialPooler(self, inputs):
		
		# ADD BOOSTING TO SPATIAL POOLER

		# Overlap
		# For each column sum the input axon states of connected proximal synapses (synapses above permanence threshold)
		overlap = [0] * self.num_columns
		for c in range(self.num_columns):
			for s in range(self.num_psynapses):
				if self.ps_permanences[c, s] > self.s_threshold:
					overlap[c] = overlap[c] + inputs[self.ps_addresses[c, s]]

		# Inhibiion
		# Active column addresses are the indices of maximum values in overlap list
		self.ac_addresses = np.zeros(self.num_active_columns, dtype=np.int8)
		for i in range(self.num_active_columns):
			ac = np.argmax(overlap)
			self.ac[i] = ac
			overlap[ac] = 0

		return self.ac_addresses

#	def runTemporalMemory(self):

	def getLayer3b(self):

		return (self.n_active_states,
				self.n_predict_states,
				self.n_learn_states,
				self.ps_addresses,
				self.ps_permanences,
				self.bs_addresses,
				self.bs_permanences)
