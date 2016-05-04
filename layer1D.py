import random as rand
import numpy as np

# Naming Convention:
# c means column
# s means synapse
# n means number of

def initLayer(nColumns, nSynapses):
	sThreshold = 20

	# Get the shape of proximal dendrite segments: synapses (x-axis) by column (y-axis)
	shapeProximal = (nSynapses, nColumns)
	
	# Synapse Permanance 
	sPermProximal = np.random.random_integers(sThreshold, sThreshold + 1, shapeProximal)

	thresholds = np.full(shapeProximal, sThreshold, dtype=np.int8)

	return sPermProximal, thresholds

def spatialPooler(inputVector, sPermProximal, thresholds):
	
	# If permanance is greater than threshold then true, false otherwise
	connectedSynapses = np.greater(sPermProximal, thresholds) 

	overlapScores = np.dot(inputVector, connectedSynapses)

	# Inhibition
	percentageActiveColumns = 0.4
	nActiveColumns = np.int16(np.ceil(nColumns * percentageActiveColumns))
	activeColumnAddresses = np.zeros(nActiveColumns, dtype=np.int16)

	for c in range(nActiveColumns):
		activeColumnAddresses[c] = np.argmax(overlapScores)
		overlapScores[activeColumnAddresses[c]] = 0	

	# Learning
	learnRate = 1
	learnArray = learnRate * (inputVec - np.less_equal(inputVec, thresholds[:,0]))
	for cAddress in activeColumnAddresses:
		sPermProximal[:,cAddress] = sPermProximal[:,cAddress] + learnArray

	print(sPermProximal)

	return activeColumnAddresses


inputVec = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
nColumns = 5
nSynapses = len(inputVec)

perm, thresh = initLayer(nColumns, nSynapses)
for i in range(10):
	activeColumns = spatialPooler(inputVec, perm, thresh)
