import numpy as np

class CorticalLayer(object):

	def __init__(self, num_inputs, num_columns, num_neurons):

		layer_shape = (num_columns, num_neurons)

		# Layer Data Variables
		self.n_active_states = np.zeros((2, num_columns, num_neurons), dtype=np.int8)
		self.n_predict_states = np.zeros(layer_shape, dtype=np.int8)
		self.n_learn_states = np.zeros(layer_shape, dtype=np.int8)

		# Synapse Variables
		self.s_threshold = 20
		self.s_learning_rate = 1
		self.s_permanence_lower = 0
		self.s_permanence_upper = 99

		# Proximal Synapse Data Variables
		ps_connectivity = 0.5
		self.ps_shape = (num_columns, num_inputs * ps_connectivity)
		self.ps_addresses = np.zeros(self.ps_shape, dtype=np.int8)		
		for c in range(num_columns):
			self.ps_addresses[c] = np.random.choice(num_inputs, num_inputs * ps_connectivity, replace=False)
		self.ps_permanences = np.random.random_integers(self.s_threshold, self.s_threshold + 1, self.ps_shape)

		# Basal Synapse Data Variables
		self.bs_addresses = np.full(layer_shape, None, dtype=object)
		self.bs_permanences = np.full(layer_shape, None, dtype=object)

	def getLayer(self):

		return (self.n_active_states,
				self.n_predict_states,
				self.n_learn_states,
				self.s_threshold,
				self.s_learning_rate,
				self.s_permanence_lower,
				self.s_permanence_upper,
				self.ps_addresses,
				self.ps_permanences,
				self.bs_addresses,
				self.bs_permanences)
