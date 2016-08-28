import numpy as np

def computeTemporalMemory( layer ):
	columns = layer.columns

	prevActiveNeurons = layer.activeNeurons
	prevWinnerNeurons = layer.winnerNeurons

	layer.activeNeurons = []
	layer.winnerNeurons = []
	layer.predictNeurons = []

	for column in columns:
		if column in layer.activeColumns:
			if column.hasActiveBasalDendrites:
				activatePredictedColumn( layer )
			else:
				burstColumn( layer, column, prevWinnerNeurons )

	layer.computeBasalDendriteActivity()

# Finish coding
# Add learning
def activatePredictedColumn( layer ):
	addNeurons = []

	for activeDendrite in layer.activeDendrites:
		addNeurons.append( activeDendrite.parent )

	layer.activeNeurons += addNeurons
	layer.winnerNeurons += addNeurons

# Finish coding
# Add learning
def burstColumn( layer, column, prevWinnerNeurons ):
	neurons = column.neurons
	addNeurons = neurons
	bestNeuron = np.random.choice( neurons )

	numAxons = len( prevWinnerNeurons )

	numAddedSynapses = min( 40, numAxons ) # 40 is max new synapse count.  Find a home for it

	if numAddedSynapses > 0:
		synAddresses = np.array( [neuron.idx for neuron in prevWinnerNeurons], dtype=np.int32 )
		synPermanences = np.full( numAxons, 21, dtype=np.int8 )
		bestNeuron.createDendrite( synAddresses, synPermanences )

	layer.activeNeurons += addNeurons
	layer.winnerNeurons.append( bestNeuron )
