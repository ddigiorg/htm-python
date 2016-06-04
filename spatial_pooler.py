import numpy as np

class SpatialPooler(object):

	def __init__(self, inputs, s_threshold, s_learning_rate, s_permanence_lower, s_permanence_upper, ps_addresses, ps_permanences):
	
		self.inputs = inputs
		self.s_threshold = s_threshold
		self.s_learning_rate = s_learning_rate
		self.s_permanence_lower = s_permanence_lower
		self.s_permanence_upper = s_permanence_upper
		self.ps_addresses = ps_addresses
		self.ps_permanences = ps_permanences

		self.n_inputs = len(inputs)
		self.n_columns = len(ps_addresses)
		self.n_synapses = len(ps_addresses[0])

		self.active_columns_percent = 0.2
		self.n_active_columns = np.int16(np.ceil(self.n_columns * self.active_columns_percent))
		self.active_columns_addresses = [0] * self.n_active_columns

	def run(self):
		
		# Overlap
		overlap = [0] * self.n_columns
		for c in range(self.n_columns):
			for s in range(self.n_synapses):
				if self.ps_permanences[c, s] > self.s_threshold:
					overlap[c] = overlap[c] + self.inputs[self.ps_addresses[c, s]]

#		print(overlap)

		# Inhibiion
		for ac in range(self.n_active_columns):
			self.active_columns_addresses[ac] = np.argmax(overlap)
			overlap[ac] = 0
	
#		print(active_columns_addresses)

		# Learning
		for ac in self.active_columns_addresses:
			for s in range(self.n_synapses):
				address = self.ps_addresses[ac, s]
				input_value = self.inputs[address]
				permanence = self.ps_permanences[ac, s]
				if input_value == 1 and permanence < self.s_permanence_upper:
					self.ps_permanences[ac, s] += self.s_learning_rate
				elif input_value == 0 and permanence > self.s_permanence_lower:
					self.ps_permanences[ac, s] -= self.s_learning_rate
				elif permanence == 0:
					connections = np.zeros(self.n_inputs, dtype=np.int8)
					connections[self.ps_addresses[ac]] = 1
					new_connections = np.logical_not(connections)
					new_addresses = np.nonzero(new_connections > 0)[0] #why the [0]???? 
		
					self.ps_addresses[ac, s] = np.random.choice(new_addresses, None, replace=False)
					self.ps_permanences[ac, s] = 21

		print(self.ps_permanences)

		def get_active_columns_addresses(self):
			return self.active_columns_addresses
