# spatial_pooler.py

import numpy as np
import htm.cortex as cortex

def computeSpatialPooler( layerIn, layer ):
	columns = layer.columns
	numActiveColumns = layer.numActiveColumns
	pSynThreshold = layer.pSynThreshold

	overlap = []

	# Overlap
	for column in columns:
		column.isActive = False
		dendrite = column.dendrites[-1]
		overlap.append( cortex.computeOverlap( dendrite, pSynThreshold ) )

	# Inhibition 
	# TODO: Add random tiebreaker
	for _ in range( numActiveColumns ):
		idxAC = np.argmax( overlap )
		layer.columns[idxAC].isActive = True
		overlap[idxAC] = 0

	# Learning
	# TODO: Add learning

#	print( [column.idx for column in columns if column.is_active == True] )
