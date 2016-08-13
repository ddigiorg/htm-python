"""
TODO

+ Fix: Temporal Memory algorithm messes up because first passthrough of data has no previous learn or active addresses
+ Complete TemporalMemory
+ Add docstring comments for classes, methods, and functions
+ Address issues and comments

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
		self.ac_addresses = SpatialPooler(inputs, self.columns)

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


class Column(object):
	'''
	num_psynapses  
	ps_addresses   1D list of proximal synapse addresses   e.g. [addr0, addr1, ...]
                   address of connections to input picked randomly
	ps_permanences 1D list of proximal synapse permanences e.g. [sp0, sp1, ...]
	'''
	PS_CONNECTIVITY     = 0.5
	PS_THRESHOLD        = 20
	PS_LEARNING_RATE    = 1
	PS_PERMANENCE_LOWER = 0
	PS_PERMANENCE_UPPER = 99
	AC_PERCENT    = 0.02

	def __init__(self, in_size):
		self.ps_size = int(in_size * self.PS_CONNECTIVITY)
		self.ps_addresses   = np.random.choice(in_size, self.ps_size, replace=False)
		self.ps_permanences = np.random.random_integers(self.PS_THRESHOLD, self.PS_THRESHOLD + 1, self.ps_size)

	"""MAKE THIS MORE EFFICIENT"""
	def adaptProximalSynapses(self, axons):
		for s in range( len(self.ps_addresses) ):

			# Increment a synapse permanence in a dendrite segment if connected axon is active or permanence is above threshold
			if axons[self.ps_addresses[s]] == 1 and self.ps_permanences[s] < self.PS_PERMANENCE_UPPER:
				self.ps_permanences[s] += self.PS_LEARNING_RATE

			# Decrement a synapse permanence in a dendrite segment if connected axon is inactive or permanence is below threshold
			elif axons[self.ps_addresses[s]] == 0 or self.ps_permanences[s] > self.PS_PERMANENCE_LOWER:
				self.ps_permanences[s] -= self.PS_LEARNING_RATE

				#  if synapse permanence falls below 0, randomly connect to new axon
				if self.ps_permanences[s] < 0:
					connections = np.zeros(len(axons), dtype=np.int8)
					connections[self.ps_addresses] = 1
					unused_connections = np.logical_not(connections)
					new_addresses = np.nonzero(unused_connections > 0)[0] 

					self.ps_addresses[s]   = np.random.choice(new_addresses, None, replace=False)
					self.ps_permanences[s] = self.PS_THRESHOLD + 1


class Neuron(object):
	BS_THRESHOLD = 20
	BS_LEARNING_RATE = 1
	BS_PERMANENCE_LOWER = 0
	BS_PERMANENCE_UPPER = 99

	"""CHOOSE BETTER NAME"""
	BS_THRESHOLD2 = 1

	"""DETERMINE BETTER WAY OF INITIALIZING THIS"""
	BS_NUM_NEW = 4

	def __init__(self):
		self.bs_addresses   = []
		self.bs_permanences = []

	def segmentActive(self, d, n_addresses):
		overlap = 0
		for bs_address in self.bs_addresses[d]:
			if bs_address in n_addresses:
				overlap += 1

		if overlap >= self.BS_THRESHOLD2:
			return True

	def addDendriteSegment(self, n_previous_addresses):
		self.bs_addresses.append(n_previous_addresses)
		self.bs_permanences.append([self.BS_THRESHOLD + 1] * len(n_previous_addresses))

	def adaptSynapses(self):
		n = 0 # placeholder... delete this
		if n in n_learn_addresses:
			print(1) # increment
		elif n not in n_active_addresses and n in n_prev_active_addresses:
			print(-1) # decriment


"""CONSIDER MAKING THIS A CLASS?"""
"""CLEAN THIS UP"""
def SpatialPooler(axons, columns):
	c_size        = len(columns)
	ps_size       = columns[0].ps_size
	ps_threshold  = columns[0].PS_THRESHOLD
	ac_percent    = columns[0].AC_PERCENT
	ac_size       = int( np.ceil( c_size * ac_percent ) )
	c_active_addresses = []

	# Boosting
	"""ADD BOOSTING TO SPATIAL POOLER"""

	# Overlap: For each column sum the input axon states of connected proximal synapses (synapses above permanence threshold)
	overlap = [0] * c_size
	for c in range(c_size):
		for s in range(ps_size):
			if columns[c].ps_permanences[s] > ps_threshold:
				overlap[c] += axons[columns[c].ps_addresses[s]]

	"""ADD RANDOM TIEBREAKER IF MULTIPLE OVERLAP SCORES ARE  MAX"""
	# Inhibiion: Active column addresses are the indices of maximum values in overlap list
	for ac in range(ac_size):
		c_active_address = np.argmax(overlap)
		c_active_addresses.append(c_active_address)
		overlap[c_active_address] = 0

	# Learning
	for ac_address in c_active_addresses:
		columns[ac_address].adaptProximalSynapses(axons)

	return c_active_addresses

"""CONSIDER MAKING THIS A CLASS?"""
def TemporalMemory(c_size,
                   npc_size,
                   c_active_addresses, 
                   neurons,
                   n_previous_active_addresses,
                   n_previous_predict_addresses,
                   n_previous_learn_addresses):


	n_size = c_size * npc_size

	n_active_addresses  = []
	n_predict_addresses = []
	n_learn_addresses   = []

	# Determine active state and learn state for all neurons
	for ac in c_active_addresses:
		pattern_recognized = False
		n_learn_chosen = False

		for npc in range(npc_size):
			n = ac * npc_size + npc
			if n in n_previous_predict_addresses:
				pattern_recognized = True
				n_active_addresses.append(n)
				# d = neurons(n).getActiveSegment(n_previous_active_addresses)
				# if segmentActive(d, n_previous_learn_addresses)
				n_learn_chosen = True # tab this over -->
				n_learn_addresses.append(n) # tab this over -->
				print("==========")
				print("{} bs addresses:   {}".format(n, neurons[n].bs_addresses))
#				print("{} bs permanences: {}".format(n, neurons[n].bs_permanences))

		if pattern_recognized == False:
			for npc in range(npc_size):
				n = ac * npc_size + npc
				n_active_addresses.append(n)

		if n_learn_chosen == False:
			print("==========")
			print("previous learn neuron: {}".format(n_previous_learn_addresses))
			### Get best matching neuron ### <--put into a Neuron class method
#			for n in range(num_neurons)
				# Get best matching segment
			npc_learn = np.random.random_integers(npc_size - 1)
			n_learn = ac * npc_size + npc_learn
			### ###
			n_learn_addresses.append(n_learn)
			neurons[n_learn].addDendriteSegment(n_previous_learn_addresses)
			# ADD TO UPDATE LIST
			print("{} bs addresses:   {}".format(n_learn, neurons[n_learn].bs_addresses))
#			print("{} bs permanences: {}".format(n_learn, neurons[n_learn].bs_permanences))


	# Determine predict state for all neurons
		for n in range (n_size):
			num_dendrites = len(neurons[n].bs_addresses) 
			for d in range(num_dendrites):
				if neurons[n].segmentActive(d, n_active_addresses):
					n_predict_addresses.append(n)
					# getSegmentActiveSynapses <--lookup in notes on how to code this
					# ADD TO UPDATE LIST

	# Learning

	return (n_active_addresses, n_predict_addresses, n_learn_addresses)
