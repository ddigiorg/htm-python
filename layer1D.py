import random as rand
import numpy as np
import time

def init_layer_neuron_states(n_time_steps, n_columns, n_neurons):
	# Initialize binary 3D tensors indicating neuron active and predicted state at time steps

	layer_states_shape   = (n_time_steps, n_columns, n_neurons)
	layer_active_states  = np.zeros(layer_states_shape, dtype=np.int8)
#	layer_active_states  = np.random.randint(2, size=layer_states_shape)
	layer_predict_states = np.zeros(layer_states_shape, dtype=np.int8)
	layer_predict_states[1][0][0] = 1
	layer_predict_states[1][1][1] = 1
	layer_predict_states[1][5][1] = 1
#	layer_predict_states = np.random.randint(2, size=layer_states_shape)

	return layer_active_states, layer_predict_states

def init_layer_proximal_synapses(n_inputs, n_columns):
	
	connectivity = 0.5
	proximal_synapses_threshold = 20
	proximal_synapses_shape = (n_columns, n_inputs * connectivity)

	# Initialize proximal synapse addresses to random 50% of input data
	proximal_synapses_addresses  = np.random.choice(n_inputs, proximal_synapses_shape)

	# Initialize proximal synapse permanances as a 2D array of integer values around the threshold value
	proximal_synapses_permanances = np.random.random_integers(proximal_synapses_threshold, proximal_synapses_threshold + 1, proximal_synapses_shape)

	return proximal_synapses_addresses, proximal_synapses_permanances

def init_layer_basal_synapses(n_columns, n_neurons, n_basal_dendrites, n_basal_synapses):

	basal_synapses_threshold = 20

	layer_shape = n_columns * n_neurons

	# Initialize basal synapse addresses to array of None types.  Gets filled as Temporal Memory learns.
	basal_synapses_addresses  = np.full(layer_shape, None, dtype=object)

	# Initialize basal synapse permanances to array of None types.  Gets filled as Temporal Memory learns.
	basal_synapses_permanances = np.full(layer_shape, None, dtype=object)
 
	return basal_synapses_addresses, basal_synapses_permanances

def spatial_pooling(inputs, n_columns, proximal_synapses_addresses, proximal_synapses_permanances):
	
	proximal_synapses_threshold = 20

	# Aquire the proximal synapses inputs: 2D array of binary values from the addresses of the input data
	proximal_synapses_inputs = inputs[proximal_synapses_addresses]

	# Calculate if proximal synapse is connected: 2D array of boolean values if permanance value is greater than threshold
	proximal_synapses_connections = proximal_synapses_permanances > proximal_synapses_threshold
	
	# Calculate proximal synapse values: 2D array of binary values of the input value if the proximal synapse is connected
	proximal_synapses_values = np.logical_and(proximal_synapses_inputs, proximal_synapses_connections) + 0

	# Calculate overlap scores: 1D array of integers indicating the sum of each column's proximal synapse values
	overlap_scores = np.sum(proximal_synapses_values, axis=1) 

	# Inhibition
	active_columns_percent = 0.2
	n_active_columns = np.int16(np.ceil(n_columns * active_columns_percent))
	
	active_columns_addresses = np.argpartition(-overlap_scores, n_active_columns)[:n_active_columns]
	column_states = np.zeros(n_columns, dtype=np.int8)
	column_states[active_columns_addresses] = 1

	# Learning
	proximal_synapses_learn_rate = 1
	proximal_synapses_permanance_lower = 0
	proximal_synapses_permanance_upper = 99

	learn_matrix = proximal_synapses_learn_rate * (2 * proximal_synapses_values[active_columns_addresses] - 1)
	proximal_synapses_permanances[active_columns_addresses] += learn_matrix

	np.clip(proximal_synapses_permanances, proximal_synapses_permanance_lower, proximal_synapses_permanance_upper, out=proximal_synapses_permanances)

	return column_states, active_columns_addresses

def temporal_memory(n_columns, n_neurons, layer_active_states, layer_predict_states, column_states, active_columns_addresses, basal_synapses_addresses, basal_synapses_permanances):


	# Active columns neurons that were previously in the predicted state are activated
	layer_active_states[0] = np.zeros((n_columns, n_neurons))
	layer_active_states[0][active_columns_addresses] = layer_predict_states[1][active_columns_addresses]

	# Test if an active column has no neurons in the previous predicted state, activate all neurons in the column
	test = np.logical_not( np.any(layer_active_states[0][active_columns_addresses], axis=1) )
	layer_active_states[0][active_columns_addresses] = np.logical_and(1, test)


#	print(active_columns_addresses)
	print(layer_active_states[0])

	'''
	# Determine the state of active column neurons
	for ac_index in active_columns_addresses:
		flag = 0
		for n in range(n_neurons):
			active = layer_active_states[1][ac_index][n]
			predict = layer_predict_states[0][ac_index][n]			
			if predict == 1:
				active == 1
				flag = 1
		if flag == 0:
			for n in range(n_neurons):
				layer_active_states[1][ac_index][n] = 1

	# Determine predictive state of all neurons
	'''

	# Load current states to previous states
	layer_active_states[1] = layer_active_states[0]
	layer_predict_states[1] = layer_predict_states[0]

	return layer_active_states


temp = [0]*10
temp[0] = 1
temp[1] = 1
temp[2] = 1
inputs = np.array(temp)
n_inputs = len(inputs)
n_time_steps = 2
n_columns = 10 #2048
n_neurons = 2  #32
n_basal_dendrites = 1
n_basal_synapses = 20

#print("Initializing...")

layer_active_states, layer_predict_states = init_layer_neuron_states(n_time_steps, n_columns, n_neurons)

start = time.time()
proximal_synapses_addresses, proximal_synapses_permanances = init_layer_proximal_synapses(n_inputs, n_columns)
end = time.time()
print("PS Init Time: {}s".format(end - start))

start = time.time()
basal_synapses_addresses, basal_synapses_permanances = init_layer_basal_synapses(n_columns, n_neurons, n_basal_dendrites, n_basal_synapses)
end = time.time()
print("BS Init Time: {}s".format(end - start))

for i in range(1):
	start = time.time()
	column_states, active_columns_addresses = spatial_pooling(inputs, n_columns, proximal_synapses_addresses, proximal_synapses_permanances)
	end = time.time()
	print("Spatial Pooling Time: {}s".format(end - start))
	
	start = time.time()
	neuron_states_active = temporal_memory(n_columns, n_neurons, layer_active_states, layer_predict_states, column_states, active_columns_addresses, basal_synapses_addresses, basal_synapses_permanances)
	end = time.time()
	print("Temporal Memory Time: {}s".format(end - start))
