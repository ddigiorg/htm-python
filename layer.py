import numpy as np

class Layer(object):

	def __init__(self, n_inputs, n_columns, n_neurons):

		layer_shape = (n_columns, n_neurons)

		# Neuron States
		self.neurons_active_addresses = [None]
		self.neurons_predict_addresses = [None]
		
		# Synapse 
		self.s_threshold = 20
		self.s_learning_rate = 1
		self.s_permanence_lower = 0
		self.s_permanence_upper = 99

		# Proximal Synapse Connections
		ps_connectivity = 0.5
		self.ps_shape = (n_columns, n_inputs * ps_connectivity)
		self.ps_addresses = np.zeros(self.ps_shape, dtype=np.int8)		
		for c in range(n_columns):
			self.ps_addresses[c] = np.random.choice(n_inputs, n_inputs * ps_connectivity, replace=False)
		self.ps_permanences = np.random.random_integers(self.s_threshold, self.s_threshold + 1, self.ps_shape)

		# Basal Synapses Connections
		self.bs_addresses = np.full(layer_shape, None, dtype=object)
		self.bs_permanences = np.full(layer_shape, None, dtype=object)

	def getLayer(self):

		return (self.neurons_active_addresses,
				self.neurons_predict_addresses,
				self.s_threshold,
				self.s_learning_rate,
				self.s_permanence_lower,
				self.s_permanence_upper,
				self.ps_addresses,
				self.ps_permanences,
				self.bs_addresses,
				self.bs_permanences)
