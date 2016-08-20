import numpy as np

class TemporalMemory(object):
	def __init__(self):
		self.BS_THRESHOLD = 20

	def compute(self, layer):
		columns = layer.columns
		neurons = layer.neurons

		prev_active_neuron_indices  = layer.active_neuron_indices
		prev_winner_neuron_indices  = layer.winner_neuron_indices

		active_neuron_indices  = []
		predict_neuron_indices = []
		winner_neuron_indices  = []

		for column in columns:
			add_neuron_indices= []
			winner_neuron_index = []

			if column.is_active:
				if self.columnHasActiveBasalDendrites(column, neurons):
					print("test")
					add_neuron_indices = self.activatePredictedColumn(column, neurons)
					active_neuron_indices += add_neuron_indices
					winner_neuron_indices += add_neuron_indices
				else:
					(add_neuron_indices,
                     winner_neuron_index) = self.burstColumn(column, neurons, prev_winner_neuron_indices)
					active_neuron_indices += add_neuron_indices
					winner_neuron_indices.append(winner_neuron_index)

		for neuron_index, neuron in enumerate(neurons):
			neuron.active_basal_dendrites = []

			active_axons = np.zeros( layer.num_neurons, dtype=np.int8 )
			active_axons[active_neuron_indices] = 1

			for basal_dendrite_index, basal_dendrite in enumerate(neuron.basal_dendrites):
				bs_addresses = basal_dendrite.synapse_addresses
				bs_permanences = basal_dendrite.synapse_permanences
				if_connected = bs_permanences > self.BS_THRESHOLD
				values = np.logical_and( active_axons[bs_addresses], if_connected )
				overlap = np.sum(values)

				if overlap > 0: #0 is the segment activation threshold.  Find a home for it
					neuron.active_basal_dendrites.append( basal_dendrite_index )
					predict_neuron_indices.append( neuron_index )

		layer.active_neuron_indices  = active_neuron_indices
		layer.predict_neuron_indices = predict_neuron_indices
		layer.winner_neuron_indices  = winner_neuron_indices

	# Optimize this!
	def columnHasActiveBasalDendrites(self, column, neurons):
		neuron_indices = column.neuron_indices

		for neuron_index in neuron_indices:
			if neurons[neuron_index].active_basal_dendrites:
				return True


	# Clean and finish!
	def activatePredictedColumn(self, column, neurons):
		neuron_indices = column.neuron_indices

		active_neuron_indices = []
		winner_neuron_indices = []

		add_neuron_indices = [neuron_index for neuron_index in neuron_indices if neurons[neuron_index].active_basal_dendrites]

		return add_neuron_indices

	# Clean and finish!
	def burstColumn(self, column, neurons, prev_winner_neuron_indices):
		neuron_indices = column.neuron_indices

		best_neuron_index = np.random.choice( neuron_indices )

		num_added_synapses = min( 40, len(prev_winner_neuron_indices) ) #40 is max new synapse count.  Find a home for it

		if num_added_synapses > 0:
			best_neuron = neurons[best_neuron_index]

			dendrite_index = best_neuron.createBasalDendrite()
			permanences = np.full(len(prev_winner_neuron_indices), 21, dtype=np.int8) 
			best_neuron.basal_dendrites[dendrite_index].createSynapses(prev_winner_neuron_indices, permanences)

#			print( best_neuron.basal_dendrites[dendrite_index].synapse_addresses )

		return neuron_indices, best_neuron_index
