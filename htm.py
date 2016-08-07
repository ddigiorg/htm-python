import numpy as np

# c means column
# n means neuron
# s means synapse
# ps means proximal synapse
# bs means basal synapse

class Layer3b(object):

	s_threshold = 20
	ps_connectivity = 0.5

	"""CLEAN THIS UP"""
	def __init__(self, num_inputs, num_columns, num_neurons):

		# L3b shape data variables
		self.num_columns   = num_columns
		self.num_neurons   = num_neurons
		self.num_psynapses = int(num_inputs * self.ps_connectivity)

		# L3b state data variables
		self.c_active_addresses  = []
		self.n_active_addresses  = []
		self.n_predict_addresses = []
		self.n_learn_addresses   = []

		# L3b proximal synapse data variables
		self.ps_addresses = np.zeros( (num_columns, self.num_psynapses), dtype=np.int8)		
		for c in range(num_columns):
			self.ps_addresses[c] = np.random.choice(num_inputs, num_inputs * self.ps_connectivity, replace=False)
		self.ps_permanences = np.random.random_integers(self.s_threshold, self.s_threshold + 1, (num_columns, self.num_psynapses) )

		# L3b basal synapse data variables
		self.bs_addresses   = np.full( (num_columns, num_neurons), None, dtype=object)
		self.bs_permanences = np.full( (num_columns, num_neurons), None, dtype=object)

	def runSpatialPooler(self, inputs):
		self.c_active_addresses = SpatialPooler(inputs, self.ps_addresses, self.ps_permanences, self.s_threshold)

	def runTemporalMemory(self):
		self.n_active_addresses = TemporalMemory(self.num_neurons, 
                                                 self.c_active_addresses, 
                                                 self.n_active_addresses, 
                                                 self.n_predict_addresses)

	def getActiveColumnAddresses(self):
		return self.c_active_addresses

	def getActiveNeuronAddresses(self):
		return self.n_active_addresses

"""CLEAN THIS UP"""
def SpatialPooler(input_axons, ps_addresses, ps_permanences, s_threshold):

	num_columns   = len(ps_addresses)
	num_psynapses = len(ps_addresses[0])

	c_active_percent = 0.02
	num_c_active = np.int16( np.ceil( num_columns * c_active_percent ) )

	"""ADD BOOSTING TO SPATIAL POOLER"""

	# Overlap
	# For each column sum the input axon states of connected proximal synapses (synapses above permanence threshold)
	overlap = [0] * num_columns
	for c in range(num_columns):
		for s in range(num_psynapses):
			if ps_permanences[c, s] > s_threshold:
				overlap[c] = overlap[c] + input_axons[ps_addresses[c, s]]

	# Inhibiion
	# Active column addresses are the indices of maximum values in overlap list
	c_active_addresses = np.zeros(num_c_active, dtype=np.int8)
	for i in range(num_c_active):
		c_active_address = np.argmax(overlap)
		c_active_addresses[i] = c_active_address
		overlap[c_active_address] = 0

	# Learning
	for ac in c_active_addresses:
		adaptSynapses(input_axons, ps_addresses[ac], ps_permanences[ac], s_threshold)

	return c_active_addresses


def TemporalMemory(num_neurons, c_active_addresses, n_active_addresses, n_predict_addresses):

	n_active_addresses = []

	# Determine neuron axons' active state
	for ac in c_active_addresses:
		pattern_recognized = False

#		for n in range(num_neurons):
#			if n_active_addresses[ac, n] in predict_addresses[ac, n]:
#				pattern_recognized = True
#				n_active_addresses[ac, n] = 

		if pattern_recognized == False:
			for n in range(num_neurons):
				n_active_addresses.append([ac, n])

		print(n_active_addresses)				

		return n_active_addresses


"""MAKE MORE EFFICIENT"""
def adaptSynapses(axons, s_addresses, s_permanences, s_threshold):
	s_learning_rate = 1
	s_permanence_lower = 0
	s_permanence_upper = 99

	for s in range(len(s_addresses)):

		# Increment synapse permanence if connected axon is active or permanence is above threshold
		if axons[s_addresses[s]] == 1 and s_permanences[s] < s_permanence_upper:
			s_permanences[s] += s_learning_rate

		# Decrement synapse permanence if connected axon is inactive or permanence is below threshold
		elif axons[s_addresses[s]] == 0 or s_permanences[s] > s_permanence_lower:
			s_permanences[s] -= s_learning_rate

			#  if synapse permanence falls below 0, randomly connect to new axon
			if s_permanences[s] < 0:
				connections = np.zeros(len(axons), dtype=np.int8)
				connections[s_addresses] = 1
				unused_connections = np.logical_not(connections)
				new_addresses = np.nonzero(unused_connections > 0)[0] 

				s_addresses[s]   = np.random.choice(new_addresses, None, replace=False)
				s_permanences[s] = s_threshold + 1
