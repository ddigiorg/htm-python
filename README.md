#Hierarchical Temporal Memory (HTM)

This is a simple python implementation of Numenta's HTM algorithm.  The purpose of this project is to develop an understanding of the basic neuroscience principles of the cortex and familiarity with cortical algorithms.

##Structure of the Cortex

###Cortex

Neuroscience:  About 2-3mm thick typically containing 6 layers(5 layers of neurons and an axon layer)

###Region



###Layers

Neuroscience: The cortex contains 6 layers(5 layers of neurons and an axon layer)
+ Pial Surface
+ Layer 1: 
+ Layer 2: 
+ Layer 3: One of the primary feed-forward layers of neurons
+ Layer 4: 
+ Layer 5: 
+ Layer 6: 
+ White Matter

###Columns

Neuroscience: Each layer of the cortex has neurons typically organized into vertical columns, and can be broken down into a more basic structure, the mini-column.  Due to a class of inhibitory neurons, all neurons in the column respond to the same feed forward inputs of the proximal dendrites.  Therefore in the HTM algorithm for organizational purposes, each column stores proximal dendrites rather than each neuron in a column.

###Neurons

The structure of an HTM cell, or neuron, is modeled after pyramidal neurons in the neocortex.  In a real neuron when it is in an active state the axon outputs a short burst of action potentials.  When it is in a predictive state the axon outputs a slower, steady rate of action potentials.  These action potentials are not modeled in the HTM.

Neuron Inputs
+ Proximal Dendrites
+ Apical Dendrites
+ Basal Dendrites

Neuron Outputs
+ Axon: has 3 output states:
	+ Inactive
	+ Active
	+ Prediction

###Dendrite Segments

+ Proximal Dendrite Segments: recieve feedforward input and used to put a neuron in an active state.
+ Apical Dendrite Segments: recieve feedback from higher cortical layers and used to put a neuron in a predictive state.
+ Basal Dendrite Segments: recieve lateral input from nearby neurons and is used to put a neuron in a predictive state.

###Synapses

+ Potential Synapses: Represents all the axons that pass close enough to a dendrite segment that they could potentially form a synapse.
+ Permanance: a scalar value representing the range of connectedness between an axon and a dendrite.  If the permanance is above a certain threshold, the synapse is connected.

##Spatial Pooler

Operates at the columnar level by using each column's proximal dendrite input.

##Temporal Pooler

Operates at the neuronal level by by using each neuron's basal dendrite input.  Apical dendrites have not been implemented in this version of the algorithm.
