import numpy as np

class TemporalMemory(object):
	def __init__(self):
		pass

	def compute(self, layer):
		columns = layer.columns

		prev_active_neurons  = layer.active_neurons
		prev_winner_neurons  = layer.winner_neurons

		layer.active_neurons  = []
		layer.winner_neurons  = []
		layer.predict_neurons = []

		for column in columns:
			if column.is_active:
				if column.has_active_basal_dendrites:
					self.activatePredictedColumn(layer)
				else:
					self.burstColumn(layer, column, prev_winner_neurons)

#		print("prev active: {}".format( [neuron.idx for neuron in prev_active_neurons] ) )
#		print("prev winner: {}".format( [neuron.idx for neuron in prev_winner_neurons] ) )
#		print("active: {}".format( [neuron.idx for neuron in layer.active_neurons] ) )
#		print("winner: {}".format( [neuron.idx for neuron in layer.winner_neurons] ) )

		layer.computeBasalDendriteActivity(layer.active_neurons)

	# Finish coding
	# Add learning
	def activatePredictedColumn(self, layer):
		add_neurons = []
		for active_dendrite in layer.active_dendrites:
			add_neurons.append(active_dendrite.parent)
		layer.active_neurons += add_neurons
		layer.winner_neurons += add_neurons

	# Finish coding
	# Add learning
	def burstColumn(self, layer, column, prev_winner_neurons):
		neurons = column.neurons
		add_neurons = neurons
		best_neuron = np.random.choice(neurons)

		num_inputs = len(prev_winner_neurons)

		num_added_synapses = min( 40, num_inputs ) # 40 is max new synapse count.  Find a home for it

		if num_added_synapses > 0:
			addresses = np.array( [ neuron.idx for neuron in prev_winner_neurons], dtype=np.int32)
			permanences = np.full( num_inputs, 21, dtype=np.int8) 
			best_neuron.createBasalDendrite(num_inputs, addresses, permanences)

		layer.active_neurons += add_neurons
		layer.winner_neurons.append(best_neuron)
