"""
TODO
"""

import numpy as np

class Dendrite(object):

#	__slots__ = ['synapse_addresses', 'synapse_permanences']

	def __init__(self):
		self.synapse_addresses   = np.array([], dtype=np.int16)
		self.synapse_permanences = np.array([], dtype=np.int16)

	def createSynapses(self, addresses, permanences):
		self.synapse_addresses   = np.append(self.synapse_addresses, addresses)
		self.synapse_permanences = np.append(self.synapse_permanences, permanences)

class Neuron(object):
	def __init__(self, neuron_index, neurons_per_column):
		self.neuron_index = neuron_index
		self.column_index = int( neuron_index / neurons_per_column)

		self.basal_dendrites = []

		self.active_basal_dendrites = []

	def createBasalDendrite(self):
		self.basal_dendrites.append( Dendrite() )
		dendrite_idx = len(self.basal_dendrites) - 1
		return  dendrite_idx

class Column(object):
	def __init__(self, column_index, num_neurons_per_column):
		self.index = column_index

		n_start = column_index * num_neurons_per_column
		n_stop = n_start + num_neurons_per_column
		self.neuron_indices = list( range(n_start, n_stop) )

		self.proximal_dendrite = Dendrite()
		self.is_active = False

class Layer3b(object):
	def __init__(self, num_inputs, num_columns, num_neurons_per_column):
		self.num_columns = num_columns
		self.num_neurons_per_column = num_neurons_per_column
		self.num_neurons = num_columns * num_neurons_per_column
		self.num_proximal_synapses = int(num_inputs * 0.5)

		self.columns = [Column(column_index, num_neurons_per_column) for column_index in range(num_columns)]
		self.neurons = [Neuron(neuron_index, num_neurons_per_column) for neuron_index in range(self.num_neurons)]

		self.active_neuron_indices = []
		self.predict_neuron_indices= []
		self.winner_neuron_indices = []

		# Initialize Synapses to Potential Pool
		for column in self.columns:
			addresses = np.random.choice(num_inputs, self.num_proximal_synapses, replace=False)
			permanences = np.random.random_integers(20, 21, self.num_proximal_synapses)
			column.proximal_dendrite.createSynapses(addresses, permanences)

#		self.active_segments   = [] # [ [cell, segment] ... ]
#		self.matching_segments = []
