import numpy as np

# c means column
# n means neuron
# d means dendrite segment
# s means synapse
# ps means proximal synapse
# bs means basal synapse

"""MAYBE PUT PROXIMAL SYNAPSE SPECIFIC LEARNING HERE"""
class Column(object):
	ps_connectivity = 0.5
	ps_threshold = 20

	def __init__(self, num_inputs):

		self.num_psynapses = int(num_inputs * self.ps_connectivity)

		self.ps_addresses   = np.random.choice(num_inputs, num_inputs * self.ps_connectivity, replace=False)
		self.ps_permanences = np.random.random_integers(self.ps_threshold, self.ps_threshold + 1, self.num_psynapses)

"""MAYBE PUT BASAL SYNAPSE SPECIFIC LEARNING HERE"""
class Neuron(object):
	bs_threshold = 20
	num_new_synapses = 4

	def __init__(self):
		self.previous_active_state  = False
		self.previous_predict_state = False
		self.previous_learn_state   = False

		self.active_state  = False
		self.predict_state = False
		self.learn_state   = False

		self.bs_addresses   = []
		self.bs_permanences = []


class Layer3b(object):
	def __init__(self, num_inputs, num_columns, num_neurons):
		self.columns = [Column(num_inputs) for c in range(num_columns)]
		self.neurons = [[Neuron() for n in range(num_neurons)] for c in range(num_columns)]

		self.c_active_addresses = []

	def runSpatialPooler(self, inputs):
		self.c_active_addresses = SpatialPooler(inputs, self.columns)

	def runTemporalMemory(self):
		TemporalMemory(self.neurons, self.c_active_addresses)


"""CLEAN THIS UP"""
def SpatialPooler(input_axons, columns):
	num_columns   = len(columns)
	num_psynapses = columns[0].num_psynapses
	ps_threshold  = columns[0].ps_threshold

	c_active_percent = 0.02
	num_c_active = np.int16( np.ceil( num_columns * c_active_percent ) )

	"""ADD BOOSTING TO SPATIAL POOLER"""

	# Overlap
	# For each column sum the input axon states of connected proximal synapses (synapses above permanence threshold)
	overlap = [0] * num_columns
	for c in range(num_columns):
		for s in range(num_psynapses):
			if columns[c].ps_permanences[s] > ps_threshold:
				overlap[c] = overlap[c] + input_axons[columns[c].ps_addresses[s]]

	# Inhibiion
	# Active column addresses are the indices of maximum values in overlap list
	c_active_addresses = np.zeros(num_c_active, dtype=np.int8)
	for i in range(num_c_active):
		c_active_address = np.argmax(overlap)
		c_active_addresses[i] = c_active_address
		overlap[c_active_address] = 0

	# Learning
	for ac in c_active_addresses:
		adaptSynapses(input_axons, [columns[ac].ps_addresses], [columns[ac].ps_permanences], ps_threshold)

	return c_active_addresses


def TemporalMemory(neurons, c_active_addresses):
	num_columns = len(neurons)
	num_neurons = len(neurons[0])
	num_new_synapses = neurons[0][0].num_new_synapses

	n_previous_active_addresses = []

	for c in range(num_columns):
		for n in range(num_neurons):
			neurons[c][n].previous_active_state  = neurons[c][n].active_state
			neurons[c][n].previous_predict_state = neurons[c][n].predict_state
			neurons[c][n].previous_learn_state   = neurons[c][n].learn_state

			if neurons[c][n].previous_active_state == True:
				n_previous_active_addresses.append([c, n])

			neurons[c][n].active_state  = False
			neurons[c][n].predict_state = False
			neurons[c][n].learn_state   = False

	# Determine neurons' active state
	for ac in c_active_addresses:
		pattern_recognized = False
		n_learn_chosen = False

		for n in range(num_neurons):
			if neurons[ac][n].previous_predict_state == True:
				pattern_recognized = True
				neurons[ac][n].active_state = True
				n_learn_chosen = True #!!!

		if pattern_recognized == False:
			for n in range(num_neurons):
				neurons[ac][n].active_state = True

		if n_learn_chosen == False:
			n_previous_active_addresses.append([0, 0]) #!!!
			n_learn = 0
			neurons[ac][n_learn].learn_state = True
			neurons[ac][n_learn].bs_addresses.append(n_previous_active_addresses)
			neurons[ac][n_learn].bs_permanences = [21]*num_new_synapses

		neurons[ac][0].predict_state = True #!!!
		print(neurons[ac][0].bs_addresses)
		print(neurons[ac][0].bs_permanences)

	# Determine neurons' predict state
#	for c in range(num_columns):
#		for n in range (num_neurons):
#			if neurons[c][n].bs_addresses
#				n_predict_addresses.append([c, n])


	# Learning


"""CLEAN THIS"""
"""MAKE MORE EFFICIENT"""
"""MAYBE PUT IN COLUMN AND LAYER CLASSES INSTEAD?"""
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
