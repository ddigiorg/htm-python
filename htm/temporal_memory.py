# temporal_memory.py

import numpy as np
import htm.cortex as cortex

def computeTemporalMemory( layer ):
	prevWinnerNeurons = cortex.resetNeuronStates( layer )

	for column in layer.columns:
		if column.isActive:
			if column.hasActiveBasalDendrites:
				activatePredictedColumn( layer, column )
			else:
				burstColumn( layer, column, prevWinnerNeurons )

	layer.activeSegments = []
	cortex.computeDendriteActivity( layer )

#	print( [dendrite.parent.idx for dendrite in layer.activeDendrites] )
#	print( [neuron.idx for neuron in layer.winnerNeurons] )

# Finish coding
# Add learning
def activatePredictedColumn( layer, column ):
	for activeDendrite in layer.activeDendrites:
		if activeDendrite.parent.column == column:
			neuron = activeDendrite.parent
			neuron.isActive = True
			neuron.isWinner = True

# Finish coding
# Add learning
def burstColumn( layer, column, prevWinnerNeurons ):
	activeNeurons = column.neurons
	bestNeuron = np.random.choice( activeNeurons )

	numSynapses = len( prevWinnerNeurons )

	numAddedSynapses = min( 40, numSynapses ) # 40 is max new synapse count.  Find a home for it

	if numAddedSynapses > 0:
		synConnections = prevWinnerNeurons
		synPermanences = np.full( numSynapses, 21, dtype=np.int8 )
		cortex.createDendrite( bestNeuron )
		dendrite = bestNeuron.dendrites[-1]
		cortex.createSynapses( numSynapses, dendrite, synConnections, synPermanences )

	for neuron in activeNeurons:
		neuron.isActive = True
	bestNeuron.isWinner = True
