"""
TODO

+ Complete TemporalMemory
+ Add docstring comments for classes and methods
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
	def __init__(self, in_size, c_size, npc_size):
		self.c_size   = c_size
		self.npc_size = npc_size

		self.columns = [Column(in_size) for c in range(c_size)]
		self.neurons = [Neuron()        for n in range(c_size * npc_size)]
		self.sp = SpatialPooler(c_size, 
                                self.columns[0].ps_size, 
                                self.columns[0].PS_THRESHOLD, 
                                self.columns[0].AC_PERCENT)
		self.tm = TemporalMemory(c_size, npc_size)

		self.active_columns = []

		self.prev_active_neurons  = []
		self.prev_predict_neurons = []
		self.prev_winner_neurons  = []

		self.active_neurons  = []
		self.predict_neurons = []
		self.winner_neurons  = []

	def runSpatialPooler(self, inputs):
		self.active_columns = self.sp.compute(inputs, self.columns)

	def runTemporalMemory(self):
		self.prev_active_neurons  = self.active_neurons[:]
		self.prev_predict_neurons = self.predict_neurons[:]
		self.prev_winner_neurons   = self.winner_neurons[:]

		(self.active_neurons, 
         self.predict_neurons, 
         self.winner_neurons) = self.tm.compute(self.neurons,
            self.active_columns, 
            self.prev_active_neurons,
            self.prev_predict_neurons,
            self.prev_winner_neurons)


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

	def dendriteAdapt(self, axons):
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
		self.bs_addresses = []
		self.bs_permanences = []

		self.prev_active_dendrites = []
		self.prev_learn_dendrites = []
		self.active_dendrites = []
		self.learn_dendrites = []

	def dendritesSet(self):
		self.prev_active_dendrites = self.active_dendrites
		self.prev_learn_dendrites  = self.learn_dendrites
		self.active_dendrites = []
		self.learn_dendrites  = []

	def dendriteActive(self, d, active_neurons):
		overlap = np.sum( np.in1d(self.bs_addresses[d], active_neurons) )

		print("bs_addresses:", self.bs_addresses[d])
		print("active neurons:", active_neurons)
		print("overlap", overlap)

#		print(overlap)
		if overlap >= self.BS_THRESHOLD2:
			self.active_dendrites.append(d)
			return True

	def dendriteAdd(self, prev_neurons):
		self.bs_addresses.append(prev_neurons)
		self.bs_permanences.append( [self.BS_THRESHOLD + 1] * len(prev_neurons) )
		self.learn_dendrites.append( len(self.bs_addresses) - 1 )

	def dendriteAdapt(self, active_neurons, is_winner_neuron, n_size):
		for d in self.prev_active_dendrites + self.learn_dendrites:
			if d in self.learn_dendrites or is_winner_neuron:
				neuron_axons = np.zeros(n_size)
				neuron_axons[active_neurons] = 1

				bs_updates = self.BS_LEARNING_RATE * (2 * neuron_axons[self.bs_addresses[d]] - 1)
				self.bs_permanences[d] += bs_updates


############################################################################
class SpatialPooler(object):

	def __init__(self, c_size, ps_size, ps_threshold, ac_percent):
		self.c_size = c_size
		self.ps_size = ps_size
		self.ps_threshold = ps_threshold
		self.ac_percent = ac_percent
		self.ac_size = int( c_size * ac_percent )

	def compute(self, axons, columns):
		active_columns = []

		# Boosting
		"""ADD BOOSTING TO SPATIAL POOLER"""

		# Overlap: For each column sum the input axon states of connected proximal synapses (synapses above permanence threshold)
		overlap = np.zeros(self.c_size)
		for c in range(self.c_size):
			if_ps_connected = columns[c].ps_permanences > self.ps_threshold
			ps_values = np.logical_and( axons[columns[c].ps_addresses], if_ps_connected )
			overlap[c] = np.sum(ps_values)

		"""ADD RANDOM TIEBREAKER IF MULTIPLE OVERLAP SCORES ARE  MAX"""
		# Inhibiion: Active column addresses are the indices of maximum values in overlap list
		for ac in range(self.ac_size):
			active_column = np.argmax(overlap)
			active_columns.append(active_column)
			overlap[active_columns] = 0

		# Learning
		for ac in active_columns:
			columns[ac].dendriteAdapt(axons)

		return active_columns


#############################################################################
class TemporalMemory(object):

	def __init__(self, c_size, npc_size):
		self.c_size = c_size
		self.npc_size = npc_size
		self.n_size = c_size * npc_size

	def compute(self,
                neurons,
                active_columns,
                prev_active_neurons,
                prev_predict_neurons,
                prev_winner_neurons):

		active_neurons  = []
		predict_neurons = []
		winner_neurons  = []

		burst_columns = active_columns[:]

		print("active column", active_columns)
	
#		for n in range(self.n_size):
#			neurons[n].dendritesSet()

		# Phase 1: Activate correctly predicted neurons
		for n in prev_predict_neurons:
			c = int( np.floor(n / self.npc_size) )
			if c in active_columns:
				active_neurons.append(n)
				winner_neurons.append(n)
				burst_columns.remove(c)

		# Phase 2: Burst unpredicted columns
		# INCOMPLETE
		for c in burst_columns:
			for npc in range(self.npc_size):
				n = c * self.npc_size + npc
				active_neurons.append(n)

			# work on properly getting best matching cell
			npc_winner = np.random.random_integers(self.npc_size - 1)
			n_winner = c * self.npc_size + npc_winner
			winner_neurons.append(n_winner)

			# FIGURE THIS STUPID THING OUT...... HOW TO HANDLE INITIALIZATION...
			neurons[n_winner].dendriteAdd(prev_winner_neurons)

#		# Phase 3: Perform learning by adapting segments
#		# INCOMPLETE
#		for n in range(self.n_size):
#			is_winner_neuron = False
#			if n in winner_neurons:
#				is_winner_neuron = True	
#			neurons[n].dendriteAdapt(prev_active_neurons, is_winner_neuron, self.n_size)

		# Phase 4: Compute predicted cells
		for n in range(self.n_size):
			num_dendrites = len( neurons[n].bs_addresses )
			for d in range(num_dendrites):
				print()
				print("neuron", n)
				if neurons[n].dendriteActive(d, active_neurons):
					predict_neurons.append(n)

		print("==============")

		return (active_neurons, predict_neurons, winner_neurons)
