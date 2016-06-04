import layer as lay
import spatial_pooler as sp

inputs = [0] * 10
inputs[0] = 1
inputs[1] = 1

layer = lay.Layer(len(inputs), 3, 2)

(neurons_active_addresses,
neurons_predict_addresses,
s_threshold,
s_learning_rate,
s_permanence_lower,
s_permanence_upper,
ps_addresses,
ps_permanances,
bs_addresses,
bs_permanances) = layer.getLayer()

print(inputs)
print(ps_addresses)
print(ps_permanances)

spool = sp.SpatialPooler(
	inputs,
	s_threshold,
	s_learning_rate,
	s_permanence_lower,
	s_permanence_upper,
	ps_addresses,
	ps_permanances)


for i in range(100):
	spool.run()
