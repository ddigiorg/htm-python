import numpy as np

class Dendrite(object):
#	__slots__ = ['synapse_addresses', 'synapse_permanences']

	def __init__(self, idx, parent, addresses, permanences):
		self.idx = idx
		self.parent = parent
		self.synapse_addresses = addresses
		self.synapse_permanences = permanences

class Neuron(object):
	def __init__(self, idx, column):
		self.idx = idx
		self.column = column
		self.basal_dendrites = []

	def createBasalDendrite(self, num_inputs, addresses, permanences):
		d_idx = len(self.basal_dendrites)
		self.basal_dendrites.append(Dendrite(d_idx, self, addresses, permanences))

class Column(object):
	def __init__(self, idx, num_neurons_per_column):
		self.idx = idx
		self.neurons = [Neuron(self.idx * num_neurons_per_column + npc_idx, self) for npc_idx in range(num_neurons_per_column)]
		self.proximal_dendrite = None

		self.is_active = False
		self.has_active_basal_dendrites = False

	def createProximalDendrite(self, num_inputs, addresses, permanences):
		self.proximal_dendrite = Dendrite(0, self, addresses, permanences)

class Layer3b(object):
	def __init__(self, num_inputs, num_columns, num_neurons_per_column):
		self.num_columns = num_columns
		self.num_neurons_per_column = num_neurons_per_column
		self.num_neurons = num_columns * num_neurons_per_column

		self.columns = [Column(c_idx, num_neurons_per_column) for c_idx in range(num_columns)]

		self.active_neurons  = []
		self.winner_neurons  = []
		self.predict_neurons = []

		self.active_dendrites   = []
		self.matching_dendrites = []

		self.initRandomReceptiveFields(num_inputs)
#		self.initTopologicalReceptiveFields(num_inputs, 100)

	def initRandomReceptiveFields(self, num_inputs):
		for column in self.columns:
			num_proximal_synapses = int(num_inputs * 0.5)

			ps_addresses = np.random.choice(num_inputs, num_proximal_synapses, replace=False)
			ps_permanences = np.random.random_integers(20, 21, num_proximal_synapses)
			column.createProximalDendrite(num_inputs, ps_addresses, ps_permanences)

	# Make more efficient
	def initTopologicalReceptiveFields(self, num_inputs, field_size):
		for column in self.columns:
			start = column.idx - int(field_size * 0.5)
			stop  = column.idx + int(field_size * 0.5)
			if start < 0:
				start = 0
			if stop > num_inputs:
				stop = num_inputs

			ps_addresses = list(range(start, stop))
			ps_permanences = np.random.random_integers(20, 21, len(ps_addresses))
			column.createProximalDendrite(num_inputs, ps_addresses, ps_permanences)
		

	# Finish coding
	# Figure out how this is implemented by Numenta
	# Move this over to temporal memory?
	# Make more efficient
	def computeBasalDendriteActivity(self, active_neurons):
		self.active_dendrites = []

		inputs = np.zeros(self.num_neurons, dtype=np.int8)
		active_neuron_indices = [ neuron.idx for neuron in active_neurons]
		inputs[active_neuron_indices] = 1

		for column in self.columns:
			column.has_active_basal_dendrites = False
			for neuron in column.neurons:
				for basal_dendrite in neuron.basal_dendrites:
					bs_addresses = basal_dendrite.synapse_addresses
					bs_permanences = basal_dendrite.synapse_permanences

					if_connected = bs_permanences > 20 # BS_THRESHOLD.  Find a home for it
					values = np.logical_and(inputs[bs_addresses], if_connected)
					overlap = np.sum(values)

					if overlap > 39: # Segment activation threshold.  Find a home for it
#					if overlap > 0:
						self.active_dendrites.append(basal_dendrite)
						self.predict_neurons.append(neuron)
						column.has_active_basal_dendrites = True
