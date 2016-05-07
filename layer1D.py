import random as rand
import numpy as np

# Naming Convention:
# c means column
# p means proximal dendrite
# s means synapse
# n means number of

def initLayer(inputs, nColumns):

	inputConnectivity = 0.5
	nSynapses = int(len(inputs) * inputConnectivity)
	psPermThresh = 20
	psShape = (nSynapses, nColumns)

	# Potential Pool: Every column gets a random subset of input bits
	indexList = list(range(len(inputs)))
	psIndices = np.zeros(psShape, dtype=np.int16)
	psInputs  = np.zeros(psShape, dtype=np.int8)
	for c in range(nColumns):
		rand.shuffle(indexList)
		psIndices[c] = np.array(indexList[0 : nSynapses])
		psInputs[c] = inputs[np.ix_(psIndices[c])]
	
	# Initialize each column's proximal synapse permanance values
	psPerms = np.random.random_integers(psPermThresh, psPermThresh + 1, psShape)

	# Initialize each column's proximal synapse permanance threshold values
	psPermThreshs = np.full(psShape, psPermThresh, dtype=np.int8)

	return psInputs, psIndices, psPerms, psPermThreshs

def spatialPooler(psInputs, psIndices, psPerms, psPermThreshs, nColumns):
	
	# Calculate if proximal synapse is connected to its input based on its permanance value
	psConnected = np.greater(psPerms, psPermThreshs) 

	# Overlap Scores: Calculate by performing row-wise dot product
	cOverlapScores = np.einsum('ij,ij->i', psInputs, psConnected) 

	# Inhibition
	cActivePercent = 0.4
	ncActive = np.int16(np.ceil(nColumns * cActivePercent))
	cActiveIndices = np.zeros(ncActive, dtype=np.int16)
	'''NOTE: MAY HAVE TO SKIP COLUMNS THAT HAVE OVERLAP SCORE < 1 ''' 
	for ac in range(ncActive):
		cActiveIndices[ac] = np.argmax(cOverlapScores)
		cOverlapScores[cActiveIndices[ac]] = -1	

	# Learning
	psLearnRate = 1
	psLowerPerm = 0
	psUpperPerm = 99
	for acIndex in cActiveIndices:
		learnArray = psLearnRate * (2 * psInputs[acIndex] - 1)
		psPerms[:,acIndex] = psPerms[:,acIndex] + learnArray

	np.clip(psPerms, psLowerPerm, psUpperPerm, out=psPerms)
	
	return cActiveIndices


inputs = np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
nColumns = 5

psInputs, psIndices, psPerms, psPermThreshs = initLayer(inputs, nColumns)

for i in range(10):
	cActiveIndices = spatialPooler(psInputs, psIndices, psPerms, psPermThreshs, nColumns)
	print(cActiveIndices)
