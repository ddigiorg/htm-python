import numpy as np

# c means column
# n means neuron
# d means dendrite segment
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
		self.bs_addresses   = np.empty([num_columns, num_neurons], dtype=object)
		self.bs_permanences = np.empty([num_columns, num_neurons], dtype=object)

		print(np.array(self.bs_addresses))

	def runSpatialPooler(self, inputs):
		self.c_active_addresses = SpatialPooler(inputs, self.ps_addresses, self.ps_permanences, self.s_threshold)

#		print(self.ps_permanences[self.c_active_addresses])

	def runTemporalMemory(self):
		self.n_active_addresses = TemporalMemory(self.num_columns,
                                                 self.num_neurons, 
                                                 self.bs_addresses,
                                                 self.bs_permanences,
                                                 self.c_active_addresses, 
                                                 self.n_active_addresses, 
                                                 self.n_predict_addresses,
                                                 self.n_learn_addresses)

#		print(self.n_active_addresses)


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
		adaptSynapses(input_axons, [ps_addresses[ac]], [ps_permanences[ac]], s_threshold)

	return c_active_addresses


def TemporalMemory(num_columns,
                   num_neurons,
                   bs_addresses,
                   bs_permanences,
                   c_active_addresses,
                   n_active_addresses,
                   n_predict_addresses,
                   n_learn_addresses):

	n_previous_active_addresses  = n_active_addresses
	n_previous_predict_addresses = n_predict_addresses
	n_previous_learn_addresses   = n_learn_addresses

	n_active_addresses  = []
	n_predict_addresses = []
	n_learn_addresses   = []

	# Determine neurons' active state
	for ac in c_active_addresses:
		pattern_recognized = False
		n_learn_chosen = False

		for n in range(num_neurons):
			if [ac, n] in n_previous_predict_addresses:
				pattern_recognized = True
				n_active_addresses.append([ac, n])
				

		if pattern_recognized == False:
			for n in range(num_neurons):
				n_active_addresses.append([ac, n])

		if n_learn_chosen == False:
			n_learn = 0
			n_learn_addresses.append([ac, n_learn])
#			print(bs_addresses[ac][n_learn])
#			print(n_previous_active_addresses)
#			bs_addresses[ac][n_learn].append(n_previous_active_addresses)
#			bs_permanences

#	print(np.array(bs_addresses))

	# Determine neurons' predict state
#	for c in range(num_columns):
#		for n in range (num_neurons):
#			if
#				n_predict_addresses.append([c, n])


	# Learning

	return n_active_addresses


"""CLEAN THIS"""
"""MAKE MORE EFFICIENT"""
def adaptSynapses(axons, d_s_addresses, d_s_permanences, s_threshold):
	s_learning_rate = 1
	s_permanence_lower = 0
	s_permanence_upper = 99

	for d in range(len(d_s_addresses)):
		for s in range(len(d_s_addresses[0])):

			# Increment a synapse permanence in a dendrite segment if connected axon is active or permanence is above threshold
			if axons[d_s_addresses[d][s]] == 1 and d_s_permanences[d][s] < s_permanence_upper:
				d_s_permanences[d][s] += s_learning_rate

			# Decrement a synapse permanence in a dendrite segment if connected axon is inactive or permanence is below threshold
			elif axons[d_s_addresses[d][s]] == 0 or d_s_permanences[d][s] > s_permanence_lower:
				d_s_permanences[d][s] -= s_learning_rate

				#  if synapse permanence falls below 0, randomly connect to new axon
				if d_s_permanences[d][s] < 0:
					connections = np.zeros(len(axons), dtype=np.int8)
					connections[d_s_addresses] = 1
					unused_connections = np.logical_not(connections)
					new_addresses = np.nonzero(unused_connections > 0)[0] 

					d_s_addresses[d][s]   = np.random.choice(new_addresses, None, replace=False)
					d_s_permanences[d][s] = s_threshold + 1
