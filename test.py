import numpy as np
import time

size = 2048*32

active_state =  np.zeros(size, dtype=np.int8)
active_state[0] = 1
active_state[1] = 1
active_state[8] = 1

predict_state = np.zeros(size, dtype=np.int8)

#neuron_basal_addresses = np.array([ [[0, 1, 2],[3, 4, 5]], None, None, None, None, None, None, [[6, 7, 8]], None ])
neuron_basal_addresses = np.full(size, None, dtype=object)
neuron_basal_addresses[0] = [[0, 1, 2],[3, 4, 5]]
neuron_basal_addresses[7] = [[6, 7, 8, 0, 2, 1, 3, 4, 5, 6, 3, 2, 1]] 

'''
start = time.time()

addresses = np.ravel(np.argwhere(neuron_basal_addresses))
neuron_basal_addresses_exist = neuron_basal_addresses[addresses]

print(neuron_basal_addresses_exist)

end = time.time()
print(end - start)
'''

'''
i = 0
for dendrites in neuron_basal_addresses:
	if np.any(dendrites):
		for synapses in dendrites:	
			temp = np.sum(active_state[synapses])
			if temp > 1:
				predict_state[i] = 1
	i += 1
'''


start = time.time()
i = 0
for dendrites in neuron_basal_addresses:
	if np.any(dendrites):
		dendrite_active_state = active_state[np.array(dendrites)]			
		dendrite_overlap = np.sum(dendrite_active_state, axis=1)
		if np.any(dendrite_overlap > 1):
			predict_state[i] = 1
	i += 1
end = time.time()
print(end - start)


print(predict_state)

