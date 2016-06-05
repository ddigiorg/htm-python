import numpy as np

class SpatialPooler(object):

	def __init__(self, inputs, s_threshold, s_learning_rate, s_permanence_lower, s_permanence_upper, ps_addresses, ps_permanences):
	
		# Inputs
		self.inputs = inputs

		# Synapse Variables
		self.s_threshold = s_threshold
		self.s_learning_rate = s_learning_rate
		self.s_permanence_lower = s_permanence_lower
		self.s_permanence_upper = s_permanence_upper

		# Proximal Synapse Data Variables
		self.ps_addresses = ps_addresses
		self.ps_permanences = ps_permanences

		# Other Variables
		self.num_inputs = len(inputs)
		self.num_columns = len(ps_addresses)
		self.num_synapses = len(ps_addresses[0])

		# Active Column Addresses for Temporal Memory
		self.ac_addresses = np.zeros(1, dtype=np.int8)
		self.active_columns_percent = 0.2
		self.num_active_columns = np.int16(np.ceil(self.num_columns * self.active_columns_percent))

	def run(self):

		# ADD BOOSTING TO SPATIAL POOLER
		
		# Overlap
		overlap = [0] * self.num_columns
		for c in range(self.num_columns):
			for s in range(self.num_synapses):
				if self.ps_permanences[c, s] > self.s_threshold:
					overlap[c] = overlap[c] + self.inputs[self.ps_addresses[c, s]]

		# Inhibiion
		self.ac_addresses = np.zeros(self.num_active_columns, dtype=np.int8)
		for ac in range(self.num_active_columns):
			self.ac_addresses[ac] = np.argmax(overlap)
			overlap[ac] = 0

		print(self.ac_addresses)
	
		# Learning (MAYBE LOOK INTO MAKING LEARNING ITS OWN FUNCTION IN LAYER CLASS?)
		for ac in self.ac_addresses:
			for s in range(self.num_synapses):
				address = self.ps_addresses[ac, s]
				input_value = self.inputs[address]
				permanence = self.ps_permanences[ac, s]
				if input_value == 1 and permanence < self.s_permanence_upper:
					self.ps_permanences[ac, s] += self.s_learning_rate
				elif input_value == 0 and permanence > self.s_permanence_lower:
					self.ps_permanences[ac, s] -= self.s_learning_rate
				elif permanence == 0:
					connections = np.zeros(self.num_inputs, dtype=np.int8)
					connections[self.ps_addresses[ac]] = 1
					new_connections = np.logical_not(connections)
					new_addresses = np.nonzero(new_connections > 0) #why the [0]???? 
		
					self.ps_addresses[ac, s] = np.random.choice(new_addresses, None, replace=False)
					self.ps_permanences[ac, s] = 21

	def getActiveColumnsAddresses(self):
		return self.ac_addresses
