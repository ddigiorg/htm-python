import random as rand
import numpy as np
import time

def init_layer_neuron_states(n_time_steps, n_columns, n_neurons):
	# Initialize binary 3D tensors indicating neuron active and predicted state at time steps

	neuron_states_shape   = (n_time_steps, n_columns, n_neurons)
	neuron_states_active  = np.zeros(neuron_states_shape, dtype=np.int8)
#	neuron_states_active  = np.random.randint(2, size=neuron_states_shape)
	neuron_states_predict = np.zeros(neuron_states_shape, dtype=np.int8)
#	neuron_states_predict = np.random.randint(2, size=neuron_states_shape)

	return neuron_states_active, neuron_states_predict

def init_layer_proximal_synapses(n_inputs, n_columns):
	# Initialize Proximal Synapses: Every column gets a random subset (potential pool) of input bits

	proximal_dendrite_connectivity = 0.5
	n_proximal_synapses = int(n_inputs * proximal_dendrite_connectivity)
	proximal_synapse_threshold = 20

	proximal_synapse_shape = (n_columns, n_proximal_synapses)

	proximal_synapse_indices = np.zeros(proximal_synapse_shape, dtype=np.int16)
	proximal_synapse_values  = np.zeros(proximal_synapse_shape, dtype=np.int8)
	proximal_synapse_permanances = np.random.random_integers(proximal_synapse_threshold, proximal_synapse_threshold + 1, proximal_synapse_shape)
	proximal_synapse_thresholds  = np.full(proximal_synapse_shape, proximal_synapse_threshold, dtype=np.int8)

	input_indices = [c for c in range(n_inputs)]
	
	for c in range(n_columns):
		input_indices = np.random.permutation(input_indices)
		proximal_synapse_indices[c] = input_indices[0:n_proximal_synapses]

	return proximal_synapse_values, proximal_synapse_indices, proximal_synapse_permanances, proximal_synapse_thresholds

def init_layer_basal_synapses(n_columns, n_neurons, n_basal_dendrites):

	n_basal_synapses = 20
	basal_synapse_threshold = 20

	basal_synapse_shape = (n_columns, n_neurons, n_basal_dendrites, n_basal_synapses)

	basal_synapse_indices = np.zeros(basal_synapse_shape + (2,), dtype=np.int16)
	basal_synapse_values  = np.zeros(basal_synapse_shape, dtype=np.int8)
	basal_synapse_permanances = np.random.random_integers(basal_synapse_threshold, basal_synapse_threshold + 1, basal_synapse_shape)
	basal_synapse_thresholds = np.full(basal_synapse_shape, basal_synapse_threshold, dtype=np.int8)

	neuron_indices = [(c, n) for c in range(n_columns) for n in range(n_neurons)]

	for c in range(n_columns):
		for n in range(n_neurons):
			neuron_indices = np.random.permutation(neuron_indices)
			for bd in range(n_basal_dendrites):
				basal_synapse_indices[c][n][bd] = neuron_indices[bd:bd+n_basal_synapses]

	return basal_synapse_values, basal_synapse_indices, basal_synapse_permanances, basal_synapse_thresholds

def spatial_pooling(inputs, n_columns, proximal_synapse_values, proximal_synapse_indices, proximal_synapse_permanances, proximal_synapse_thresholds):

	# Assign the proximal synapse the value of the input value it points to
	proximal_synapse_values = inputs[proximal_synapse_indices]

	# Calculate if proximal synapse is connected to its input based on its permanance value
	proximal_synapse_is_connected = np.greater(proximal_synapse_permanances, proximal_synapse_thresholds) 

	# Overlap Scores: Calculate by performing row-wise dot product
	overlap_scores = np.einsum('ij,ij->i', proximal_synapse_values, proximal_synapse_is_connected) 

	# Inhibition
	active_columns_percent = 0.2
	n_active_columns = np.int16(np.ceil(n_columns * active_columns_percent))
	active_column_indices = np.zeros(n_active_columns, dtype=np.int16)
	column_states = np.zeros(n_columns, dtype=np.int8)	

	'''NOTE: MAY HAVE TO SKIP COLUMNS THAT HAVE OVERLAP SCORE < 1 ''' 
	for ac in range(n_active_columns):
		greatest_overlap_index =  np.argmax(overlap_scores)
		active_column_indices[ac] = greatest_overlap_index
		column_states[greatest_overlap_index] = 1
		overlap_scores[greatest_overlap_index] = -1	

	# Learning
	proximal_synapse_learn_rate = 1
	proximal_synapse_permanance_lower = 0
	proximal_synapse_permanance_upper = 99
	for ac_index in active_column_indices:
		learn_array = proximal_synapse_learn_rate * (2 * proximal_synapse_values[ac_index] - 1)
		proximal_synapse_permanances[ac_index] = proximal_synapse_permanances[ac_index] + learn_array

	np.clip(proximal_synapse_permanances, proximal_synapse_permanance_lower, proximal_synapse_permanance_upper, out=proximal_synapse_permanances)

	return column_states, active_column_indices


def temporal_memory(n_neurons, neuron_states_active, neuron_states_predict, column_states, active_column_indices, basal_synapse_values, basal_synapse_indices, basal_synapse_permanances, basal_synapse_thresholds):

	neuron_states_active[0] = neuron_states_active[1]

	# Assign the basal synapse the active state value it points to
	basal_synapse_values = neuron_states_active[0][basal_synapse_indices[:, :, :, :, 0], basal_synapse_indices[:, :, :, :, 1]]	

#	print(basal_synapse_indices[0][0][0])

	# Determine active state of active column neurons
	'''MAKE THIS MORE OPTIMIZED'''
	#nActive = np.einsum('i,ij->ij', cActive, nPredict) 
	for ac_index in active_column_indices:
		flag = 0
		for n in range(n_neurons):
			active = neuron_states_active[0][ac_index][n]
			predict = neuron_states_predict[0][ac_index][n]			
			if predict == 1:
				active == 1
				flag = 1
		if flag == 0:
			for n in range(n_neurons):
				neuron_states_active[1][ac_index][n] = 1

	# Determine predictive state of all neurons
#	for c in range(numColumns):
#	test = np.dot(nActive[1][0], bsValues[0]
	
#	print(nActive)

	return neuron_states_active	


temp = [0]*40
temp[0] = 1
temp[1] = 1
temp[2] = 1
inputs = np.array(temp)
n_inputs = len(inputs)
n_time_steps = 2
n_columns = 1000 #2048
n_neurons = 1  #32
n_basal_dendrites = 1

#print("Initializing...")

neuron_states_active, neuron_states_predict = init_layer_neuron_states(n_time_steps, n_columns, n_neurons)

start = time.time()
proximal_synapse_values, proximal_synapse_indices, proximal_synapse_permanances, proximal_synapse_thresholds = init_layer_proximal_synapses(n_inputs, n_columns)
end = time.time()
print("PS Init Time: {}s".format(end - start))

start = time.time()
basal_synapse_values, basal_synapse_indices, basal_synapse_permanances, basal_synapse_thresholds = init_layer_basal_synapses(n_columns, n_neurons, n_basal_dendrites)
end = time.time()
print("BS Init Time: {}s".format(end - start))

#for i in range(1):
#	start = time.time()
#	column_states, active_column_indices = spatial_pooling(inputs, n_columns, proximal_synapse_values, proximal_synapse_indices, proximal_synapse_permanances, proximal_synapse_thresholds)
#	end = time.time()
#	print("Spatial Pooling Time: {}s".format(end - start))
	
#	start = time.time()
#	neuron_states_active = temporal_memory(n_neurons, neuron_states_active, neuron_states_predict, column_states, active_column_indices, basal_synapse_values, basal_synapse_indices, basal_synapse_permanances, basal_synapse_thresholds)
#	end = time.time()
#	print("Temporal Memory Time: {}s".format(end - start))
