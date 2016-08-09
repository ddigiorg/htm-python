import numpy as np

# c means column
# n means neuron
# d means dendrite segment
# s means synapse
# ps means proximal synapse
# bs means basal synapse


class Layer3b(object):
	def __init__(self, num_inputs, num_columns, num_neurons):
		self.columns = [Column(num_inputs) for c in range(num_columns)]
		self.neurons = [[Neuron() for n in range(num_neurons)] for c in range(num_columns)]

		self.c_active_addresses = []

		self.n_previous_active_addresses  = []
		self.n_previous_predict_addresses = []
		self.n_previous_learn_addresses   = []

		self.n_active_addresses  = []
		self.n_predict_addresses = []
		self.n_learn_addresses   = []


	def runSpatialPooler(self, inputs):
		self.c_active_addresses = SpatialPooler(inputs, self.columns)

	def runTemporalMemory(self):

		self.n_previous_active_addresses  = self.n_active_addresses
		self.n_previous_predict_addresses = self.n_predict_addresses
		self.n_previous_learn_addresses   = self.n_learn_addresses

		self.n_active_addresses  = []
		self.n_predict_addresses = []
		self.n_learn_addresses   = []

		(self.n_active_addresses, 
         self.n_predict_addresses, 
         self.n_learn_addresses)  = TemporalMemory(
            self.c_active_addresses, 
            self.neurons, 
            self.n_previous_active_addresses,
            self.n_previous_predict_addresses,
            self.n_previous_learn_addresses)


class Column(object):
	ps_connectivity = 0.5
	ps_threshold = 20
	ps_learning_rate = 1
	ps_permanence_lower = 0
	ps_permanence_upper = 99

	def __init__(self, num_inputs):
		self.num_psynapses = int(num_inputs * self.ps_connectivity)
		self.ps_addresses   = np.random.choice(num_inputs, num_inputs * self.ps_connectivity, replace=False)
		self.ps_permanences = np.random.random_integers(self.ps_threshold, self.ps_threshold + 1, self.num_psynapses)

	"""MAKE THIS MORE EFFICIENT"""
	def adaptSynapses(self, axons):
		for s in range( len(self.ps_addresses) ):

			# Increment a synapse permanence in a dendrite segment if connected axon is active or permanence is above threshold
			if axons[self.ps_addresses[s]] == 1 and self.ps_permanences[s] < self.ps_permanence_upper:
				self.ps_permanences[s] += self.ps_learning_rate

			# Decrement a synapse permanence in a dendrite segment if connected axon is inactive or permanence is below threshold
			elif axons[self.ps_addresses[s]] == 0 or self.ps_permanences[s] > self.ps_permanence_lower:
				self.ps_permanences[s] -= self.ps_learning_rate

				#  if synapse permanence falls below 0, randomly connect to new axon
				if self.ps_permanences[s] < 0:
					connections = np.zeros(len(axons), dtype=np.int8)
					connections[self.ps_addresses] = 1
					unused_connections = np.logical_not(connections)
					new_addresses = np.nonzero(unused_connections > 0)[0] 

					self.ps_addresses[s]   = np.random.choice(new_addresses, None, replace=False)
					self.ps_permanences[s] = self.ps_threshold + 1


class Neuron(object):
	bs_threshold = 20
	bs_learning_rate = 1
	bs_permanence_lower = 0
	bs_permanence_upper = 99

	"""CHOOSE BETTER NAME"""
	bs_threshold2 = 1

	"""DETERMINE BETTER WAY OF INITIALIZING THIS"""
	num_new_synapses = 4

	def __init__(self):
		self.bs_addresses   = []
		self.bs_permanences = []

	def segmentActive(self, n_active_addresses, d):
		overlap = 0
		for bs_address in self.bs_addresses[d]:
			c = bs_address[0]
			n = bs_address[1]
			if [c, n] in n_active_addresses:
				overlap += 1

		if overlap >= self.bs_threshold2:
			return True

	def addDendriteSegment(self, n_previous_active_addresses):
		self.bs_addresses.append(n_previous_active_addresses)
		self.bs_permanences = [self.bs_threshold + 1] * len(n_previous_active_addresses)

	def adaptSynapses(self):
		print(1)

"""CONSIDER MAKING THIS A CLASS?"""
"""CLEAN THIS UP"""
def SpatialPooler(axons, columns):
	num_columns   = len(columns)
	num_psynapses = columns[0].num_psynapses
	ps_threshold  = columns[0].ps_threshold

	c_active_percent = 0.02
	num_c_active = np.int16( np.ceil( num_columns * c_active_percent ) )
	c_active_addresses = []

	# Boosting
	"""ADD BOOSTING TO SPATIAL POOLER"""

	# Overlap: For each column sum the input axon states of connected proximal synapses (synapses above permanence threshold)
	overlap = [0] * num_columns
	for c in range(num_columns):
		for s in range(num_psynapses):
			if columns[c].ps_permanences[s] > ps_threshold:
				overlap[c] += axons[columns[c].ps_addresses[s]]

	"""ADD RANDOM TIEBREAKER IF MULTIPLE OVERLAP SCORES ARE  MAX"""
	# Inhibiion: Active column addresses are the indices of maximum values in overlap list
	for i in range(num_c_active):
		c_active_address = np.argmax(overlap)
		c_active_addresses.append(c_active_address)
		overlap[c_active_address] = 0

	# Learning
	for ac in c_active_addresses:
		columns[ac].adaptSynapses(axons)

	return c_active_addresses

"""CONSIDER MAKING THIS A CLASS?"""
n_learn = 0 #!!!
def TemporalMemory(c_active_addresses, 
                   neurons,
                   n_previous_active_addresses,
                   n_previous_predict_addresses,
                   n_previous_learn_addresses):

	global n_learn #!!!
	num_columns = len(neurons)
	num_neurons = len(neurons[0])

	n_active_addresses  = []
	n_predict_addresses = []
	n_learn_addresses   = []

	# Determine neurons' active state and learn state
	for ac in c_active_addresses:
		pattern_recognized = False
		n_learn_chosen = False

		for n in range(num_neurons):
			if [ac, n] in n_previous_predict_addresses:
				pattern_recognized = True
				n_active_addresses.append([ac, n])
				n_learn_chosen = True #!!!

		if pattern_recognized == False:
			for n in range(num_neurons):
				n_active_addresses.append([ac, n])

		if n_learn_chosen == False:
			# Get best matching neuron
#			for n in range(num_neurons)
				# Get best matching segment
			n_learn = np.random.random_integers(num_neurons-1)
			# continue
			n_learn_addresses.append([ac, n_learn])
			neurons[ac][n_learn].addDendriteSegment(n_previous_active_addresses)

	# Determine neurons' predict state
	for c in range(num_columns):
		for n in range (num_neurons):
			for d in range(len(neurons[c][n].bs_addresses)):
				if neurons[c][n].segmentActive(n_active_addresses, d):
					n_predict_addresses.append([c, n])

	# Learning

	return (n_active_addresses, n_predict_addresses, n_learn_addresses)
