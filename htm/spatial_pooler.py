#spatial_pooler.py

import numpy as np

def computeSpatialPooler( axons, layer ):
	layer.activeColumns = []
	columns = layer.columns
	pSynThreshold = layer.pSynThreshold
	numActiveColumns = layer.numActiveColumns
	overlap = []

	# Overlap
	for column in columns:
		column.isActive = False
		pSynAddresses =  column.dendrite.synAddresses
		pSynPermanences = column.dendrite.synPermanences

		if_connected = pSynPermanences > pSynThreshold
		values = np.logical_and( axons[pSynAddresses], if_connected )
		overlap.append( np.sum( values ) )

	# Inhibition 
	# TODO: Add random tiebreaker
	for _ in range( numActiveColumns ):
		idxAC = np.argmax( overlap )
		layer.activeColumns.append( columns[idxAC] )
		overlap[idxAC] = 0

	# Learning
	# TODO: Add learning

#	print( [column.idx for column in columns if column.is_active == True] )
