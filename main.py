import cortical_layer as cl
import spatial_pooler as sp
import temporal_memory as tm


inputs = [0] * 10
inputs[0] = 1
inputs[1] = 1
inputs[2] = 1

layer = cl.CorticalLayer(
	num_inputs = len(inputs),
	num_columns = 3,
	num_neurons = 2)

(n_active_states,
n_predict_states,
n_learn_states,
s_threshold,
s_learning_rate,
s_permanence_lower,
s_permanence_upper,
ps_addresses,
ps_permanences,
bs_addresses,
bs_permanences) = layer.getLayer()

spool = sp.SpatialPooler(
	inputs,
	s_threshold,
	s_learning_rate,
	s_permanence_lower,
	s_permanence_upper,
	ps_addresses,
	ps_permanences)

tmem = tm.TemporalMemory(
	n_active_states,
	n_predict_states,
	n_learn_states,
	s_threshold,
	s_learning_rate,
	s_permanence_lower,
	s_permanence_upper,
	bs_addresses,
	bs_permanences)

#print(inputs)
#print(ps_addresses)
#print(ps_permanances)

#for i in range(100):
spool.run()
tmem.run(spool.getActiveColumnsAddresses())
tmem.run(spool.getActiveColumnsAddresses())


#print(ps_permanences)
