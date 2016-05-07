#Hierarchical Temporal Memory (HTM)

A simple python implementation of Numenta's HTM algorithm.  The purpose of this project is to develop a foundational understanding of the basic neuroscience principles of the cortex and apply algorithms using that knowlege.

##Structure of the Cortex

####Cortex

The human cortex is about 2-3mm thick with many regions arranged in a hierarchy.  Some well-known regions include the frontal lobe, parietal lobe, occipical lobe, and temporal lobe.

####Region

Each region of the cortex typically contains 6 layers (5 layers of neurons and an axon layer).

####Layers

+ Pial Surface
+ Layer 1: 
+ Layer 2: 
+ Layer 3: One of the primary feedforward layers. Multiple cells per column useful for inference and prediction of moving images (Numenta).
+ Layer 4: One of the primary feedforward layers. One cell per column useful in forming representations that are invariant to spatial changes (Numenta).
+ Layer 5: Motor behavior
+ Layer 6: Feedback
+ White Matter

Each layer contains ocolumns of neurons that all respond to a particular stimulus.

####Columns

Macrocolumns are  vertical structures of neurons and can be broken down into a more basic structure, the minicolumn.  Due to a class of inhibitory neurons, all neurons in the column respond to the same feed forward inputs of the proximal dendrites.  Therefore in the HTM algorithm for organizational purposes, each column stores proximal dendrites rather than each neuron in a column.

####Neurons

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

####Dendrite Segments

+ Proximal Dendrite Segment: recieve feedforward input and used to put a neuron in an active state.
+ Apical Dendrite Segments: recieve feedback from higher cortical layers and used to put a neuron in a predictive state.
+ Basal Dendrite Segments: recieve lateral input from nearby neurons and is used to put a neuron in a predictive state.

####Synapses

+ Potential Synapses: Represents all the axons that pass close enough to a dendrite segment that they could potentially form a synapse.
+ Permanance: A scalar value representing the range of connectedness between an axon and a dendrite.  If the permanance is above a certain threshold, the synapse is connected.
+ Index: Denotes what input or axon the synapse is paired with.

##Spatial Pooler Function

The spatial pooler function operates on a layer of a cortical region.  It uses each column's proximal dendrite input to return active columns that reflect the greatest connectivity with that layer's input.

1. Potential Pool: Each column sees a random subset of the input bits.
2. Overlap Score: How many of column's connected synapses(permanance above threshold) are binary 1.
3. Inhibition: enforce sparcity by selecting active columns from the top overlap scores.
4. Learning: Look at all the active columns and strengthen or weaken connections.
5. Output: active columns

##Temporal Memory Function

The temporal pooler function operates at the neuronal level by by using each neuron's basal dendrite input.  Apical dendrites have not been implemented in this version of the algorithm.

htm whitepaper page 30
