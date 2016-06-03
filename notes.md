###Input SDR

rows: inputs
dtype: binary (int8)
0001100...


###Spatial Pooling

####Proximal Synapse Initialization

ps_threshold
value: 20

ps_addresses
dim 0: columns (32)
dim 1: synapses (16)
dtype: int16
value: 0 to num inputs - 1
init: random address of input SDR

ps_permanances
dim 0: columns (32)
dim 1: synapses (16)
dtype: int8
value: 0 to 100
init: random number at or 1 above proximal synapse threshold

####Overlap

Determine the overlap score by summing the proximal synapse values of each column.
+ If a synapse permanance is above the threshold and the input SDR value at that synapse address is 1, then the synapse value is 1.  
+ If a synapse permanance is below the threshold or the input SDR value at that synapse address is 0, then the synapse value is 0.

####Inhibition

Determine the addresses of active columns by picking a percentage of columns with the highest overlap score.

####Learning

Update the synapse permanances of active columns.  
+ If the synapse value is 1, increment the synapse permanance
+ If the synapse value is 0, decrement the synapse permanance
+ Bound the synapse permanance between 0 and 100

####Plasticity

If a synapse permanance falls to 0:
+ Randomize the synapse address
+ Set permanance to threshold value

####Boosting

???


###Temporal Memory

####Basal Synapse Initialization

bs_threshold
value: 20

bs_addresses_columns
dim 0: columns (32)
dim 1: neurons (8)
dim 2: dendrites (4)
dim 3: synapses (8)
dtype: int16
value: 0 to num columns - 1
init: 0

bs_addresses_neurons
dim 0: columns (32)
dim 1: neurons (8)
dim 2: dendrites (4)
dim 3: synapses (8)
dtype: int8
value: 0 to num neurons - 1
init: 0

bs_permanances
dim 0: columns (32)
dim 1: neurons (8)
dim 2: dendrites (4)
dim 3: synapses (8)
dtype: int8
value: 0 to 100
init: 0

active_state
dim 0: columns (32)
dim 1: neurons (8)
dtype: int8
value: binary
init: 0

predict_state
dim 0: columns (32)
dim 1: neurons (8)
dtype: int8
value: binary
init: 0



####Active State



####Predict State

####Learning


