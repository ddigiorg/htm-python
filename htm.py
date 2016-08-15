"""
TODO

+ Complete TemporalMemory
+ Add docstring comments for classes, methods, and functions
+ Address issues and comments

+ Consider adding receptive fields to Column class, aka initialize proximal synapses around certain
+ Consider changinge variable names, i.e. n_prev_predict_addresses -> prev_predict_neurons

"""


import numpy as np

# c   means column
# ac  means active column
# n   means neuron
# npc means neuron per column
# d   means dendrite segment
# s   means synapse
# ps  means proximal synapse
# bs  means basal synapse


class Layer3b(object):
	"""
	columns                      1D list of Column objects
	neurons                      1D list of Neuron objects
	c_active_addresses           1D list of active column addresses    e.g. [c0, c1, ...]
	n_previous_active_addresses  1D list of previous active neurons    e.g. [n0, n1, ...]
	n_previous_predict_addresses 1D list of previous predicted neurons e.g. [n0, n1, ...]
	n_previous_learn_addresses   1D list of previous learn neurons     e.g. [n0, n1, ...] 
	n_active_addresses           1D list of current active neurons     e.g. [n0, n1, ...]
	n_predict_addresses          1D list of current predicted neurons  e.g. [n0, n1, ...]
	n_learn_addresses            1D list of current learn neurons      e.g. [n0, n1, ...]

	"""
	def __init__(self, in_size, c_size, npc_size):
		self.c_size   = c_size
		self.npc_size = npc_size

		self.columns = [Column(in_size) for c in range(c_size)]
		self.neurons = [Neuron()        for n in range(c_size * npc_size)]

		self.ac_addresses = []

		self.n_prev_active_addresses  = []
		self.n_prev_predict_addresses = []
		self.n_prev_learn_addresses   = []

		self.n_active_addresses  = []
		self.n_predict_addresses = []
		self.n_learn_addresses   = []

	def runSpatialPooler(self, inputs):
		self.ac_addresses = SpatialPooler( inputs, self.columns)

	def runTemporalMemory(self):

		self.n_prev_active_addresses  = self.n_active_addresses
		self.n_prev_predict_addresses = self.n_predict_addresses
		self.n_prev_learn_addresses   = self.n_learn_addresses

		self.n_active_addresses  = []
		self.n_predict_addresses = []
		self.n_learn_addresses   = []

		(self.n_active_addresses, 
         self.n_predict_addresses, 
         self.n_learn_addresses)  = TemporalMemory(
            self.c_size,
            self.npc_size,
            self.ac_addresses, 
            self.neurons, 
            self.n_prev_active_addresses,
            self.n_prev_predict_addresses,
            self.n_prev_learn_addresses)


############################################################################
class Column(object):
	PS_CONNECTIVITY     = 0.5
	PS_THRESHOLD        = 20
	PS_LEARNING_RATE    = 1
	PS_PERMANENCE_LOWER = 0
	PS_PERMANENCE_UPPER = 99
	AC_PERCENT          = 0.02

	def __init__(self, in_size):
		self.ps_size = int(in_size * self.PS_CONNECTIVITY)
		self.ps_addresses   = np.random.choice(in_size, self.ps_size, replace=False)
		self.ps_permanences = np.random.random_integers(self.PS_THRESHOLD, self.PS_THRESHOLD + 1, self.ps_size)

	def adaptProximalSynapses(self, axons):
		ps_updates = self.PS_LEARNING_RATE * (2 * axons[self.ps_addresses] - 1)
		self.ps_permanences += ps_updates
		np.clip(self.ps_permanences, self.PS_PERMANENCE_LOWER, self.PS_PERMANENCE_UPPER, out=self.ps_permanences)
	
		"""MAKING THINGS UNSTABLE, KEEP OUT FOR NOW"""
		"""MAKE CLEARER CODE"""
#		for s in np.where(self.ps_permanences == 0)[0]:
#			connections = np.zeros(len(axons), dtype=np.int8)
#			connections[self.ps_addresses] = 1
#			new_addresses = np.where(connections == 0)[0]
#
#			self.ps_addresses[s]   = np.random.choice(new_addresses, None, replace=False)
#			self.ps_permanences[s] = self.PS_THRESHOLD + 1


#############################################################################
class Neuron(object):
	BS_THRESHOLD        = 20
	BS_LEARNING_RATE    = 1
	BS_PERMANENCE_LOWER = 0
	BS_PERMANENCE_UPPER = 99
	BS_THRESHOLD2       = 1 # CHOOSE BETTER NAME
	BS_NUM_NEW          = 4 # DETERMINE BETTER WAY OF INITIALIZING THIS

	def __init__(self):
		self.bs_addresses   = []
		self.bs_permanences = []

	def segmentActive(self, d, n_addresses):
		overlap = np.sum( np.in1d(self.bs_addresses[d], n_addresses) )
		if overlap >= self.BS_THRESHOLD2:
			return True

	def addDendriteSegment(self, n_previous_addresses):
		if n_previous_addresses:
			self.bs_addresses.append(n_previous_addresses)
			self.bs_permanences.append([self.BS_THRESHOLD + 1] * len(n_previous_addresses))


	def adaptSynapses(self, n, d, n_learn_addresses, n_active_addresses, n_prev_predict_addresses):
		s_remove = []
		for s in range( len(self.bs_addresses[d]) ):
			if self.bs_addresses[d][s] in n_learn_addresses and self.bs_permanences[d][s] < self.BS_PERMANENCE_UPPER: 
				self.bs_permanences[d][s] += self.BS_LEARNING_RATE

			elif self.bs_permanences[d][s] >= self.BS_PERMANENCE_LOWER:
				self.bs_permanences[d][s] -= self.BS_LEARNING_RATE


############################################################################
def SpatialPooler(axons, columns):
	c_size        = len(columns)
	ps_size       = columns[0].ps_size
	ps_threshold  = columns[0].PS_THRESHOLD
	ac_percent    = columns[0].AC_PERCENT
	ac_size       = int( c_size * ac_percent )
	ac_addresses = []

	# Boosting
	"""ADD BOOSTING TO SPATIAL POOLER"""

	# Overlap: For each column sum the input axon states of connected proximal synapses (synapses above permanence threshold)
	overlap = np.zeros(c_size)
	for c in range(c_size):
		if_ps_connected = columns[c].ps_permanences > ps_threshold
		ps_values = np.logical_and( axons[columns[c].ps_addresses], if_ps_connected )
		overlap[c] = np.sum(ps_values)

	"""ADD RANDOM TIEBREAKER IF MULTIPLE OVERLAP SCORES ARE  MAX"""
	# Inhibiion: Active column addresses are the indices of maximum values in overlap list
	for ac in range(ac_size):
		ac_address = np.argmax(overlap)
		ac_addresses.append(ac_address)
		overlap[ac_address] = 0

	# Learning
	for ac in ac_addresses:
		columns[ac].adaptProximalSynapses(axons)

	return ac_addresses


#############################################################################
def TemporalMemory(c_size,
                   npc_size,
                   ac_addresses, 
                   neurons,
                   n_prev_active_addresses,
                   n_prev_predict_addresses,
                   n_prev_learn_addresses):

	n_size = c_size * npc_size

	n_active_addresses  = []
	n_predict_addresses = []
	n_learn_addresses   = []

	c_burst_addresses = ac_addresses
	
	# Phase 1: Activate correctly predicted neurons
	for n in n_prev_predict_addresses:
		c = int( np.floor(n / npc_size) )
		if c in ac_addresses:
			n_active_addresses.append(n)
			n_learn_addresses.append(n)
			c_burst_addresses.remove(c)

	# Phase 2: Burst unpredicted columns
	# INCOMPLETE
	for c in c_burst_addresses:
		for npc in range(npc_size):
			n = c * npc_size + npc
			n_active_addresses.append(n)

		# work on properly getting best matching cell
		npc_learn = np.random.random_integers(npc_size - 1)
		n_learn = c * npc_size + npc_learn
		n_learn_addresses.append(n_learn)
	
	
		neurons[n_learn].addDendriteSegment(n_prev_learn_addresses)

	# Phase 3: Perform learning by adapting segments
	# INCOMPLETE


	# Phase 4: Compute predicted cells
	for n in range(n_size):
		num_dendrites = len( neurons[n].bs_addresses )
		for d in range(num_dendrites):
			if neurons[n].segmentActive(d, n_active_addresses):
				n_predict_addresses.append(n)

	return (n_active_addresses, n_predict_addresses, n_learn_addresses)
