import random as rand
import numpy as np
import time

# Naming Convention:
# c means column
# n means neuron
# p means proximal dendrite
# s means synapse
# num means number of

def initLayer(inputs, numColumns, numNeurons):
	
	# Initialize Proximal Synapses: Every column gets a random subset (potential pool) of input bits
	pConnectivity = 0.5
	numpSynapses = int(len(inputs) * pConnectivity)
	psShape = (numColumns, numpSynapses)

	psIndexList = [x for x in range(len(inputs))]
	psIndices = np.zeros(psShape, dtype=np.int16)
	psValues  = np.zeros(psShape, dtype=np.int8)
	
	for c in range(numColumns):
		rand.shuffle(psIndexList)
		psIndices[c] = np.array(psIndexList[0:numpSynapses])

	# Initialize each column's proximal synapse permanance value and permanance threshold values
	psPermThresh = 20
	psPerms = np.random.random_integers(psPermThresh, psPermThresh + 1, psShape)
	psPermThreshs = np.full(psShape, psPermThresh, dtype=np.int8)

	# Initialize neurons active and predicted state matrices
	nShape   = (numColumns, numNeurons)
	nActive  = np.zeros(nShape, dtype=np.int8)
#	nActive  = np.random.randint(2, size=nShape)
#	nPredict = np.random.randint(2, size=nShape)
	nPredict = np.zeros(nShape, dtype=np.int8)
	
	# Initialize Basal Synapses
	numbSynapses = 20
	numbDendrites = 1
	bsShape = (numColumns, numNeurons, numbDendrites, numbSynapses)

	bsIndexList = [(c, n) for c in range(numColumns) for n in range(numNeurons)]
	bsIndices = np.zeros((numColumns, numNeurons, numbDendrites, numbSynapses, 2), dtype=np.int16)
	bsValues  = np.zeros(bsShape, dtype=np.int8)

	for c in range(numColumns):
		for n in range(numNeurons):
			for bd in range(numbDendrites):
				rand.shuffle(bsIndexList)
				bsIndices[c][n][bd] = np.array(bsIndexList[0:numbSynapses])

	# Initialize each neuron's basal synapse permanance value and permanance threshold values
	bsPermThresh = 20
	bsPerms = np.random.random_integers(bsPermThresh, bsPermThresh + 1, bsShape)
	bsPermThreshs = np.full(bsShape, bsPermThresh, dtype=np.int8)

	print(bsPerms)

	return psValues, psIndices, psPerms, psPermThreshs, nActive, nPredict, bsValues, bsIndices, bsPerms, bsPermThreshs

def spatialPooling(inputs, psValues, psIndices, psPerms, psPermThreshs, numColumns):

	for c in range(numColumns):
		psValues[c] = inputs[psIndices[c]]

	# Calculate if proximal synapse is connected to its input based on its permanance value
	psConnected = np.greater(psPerms, psPermThreshs) 

	# Overlap Scores: Calculate by performing row-wise dot product
	cOverlapScores = np.einsum('ij,ij->i', psValues, psConnected) 

	# Inhibition
	cActivePercent = 0.2
	numcActive = np.int16(np.ceil(numColumns * cActivePercent))
	cActiveIndices = np.zeros(numcActive, dtype=np.int16)
	cActive = np.zeros(numColumns, dtype=np.int8)
	'''NOTE: MAY HAVE TO SKIP COLUMNS THAT HAVE OVERLAP SCORE < 1 ''' 
	for ac in range(numcActive):
		cActiveIndices[ac] = np.argmax(cOverlapScores)
		cActive[cActiveIndices[ac]] = 1
		cOverlapScores[cActiveIndices[ac]] = -1	

	# Learning
	psLearnRate = 1
	psLowerPerm = 0
	psUpperPerm = 99
	for acIndex in cActiveIndices:
		learnArray = psLearnRate * (2 * psValues[acIndex] - 1)
		psPerms[acIndex] = psPerms[acIndex] + learnArray

	np.clip(psPerms, psLowerPerm, psUpperPerm, out=psPerms)

	return cActive, cActiveIndices

def temporalMemory(bsValues, bsIndices, bsPerm, bsPermThreshs, cActive, cActiveIndices, nActive, nPredict, numNeurons):

	for c in range(numColumns):
		for n in range(numNeurons):
			for bd in range(1):
				bsValues[c][n][bd] = nActive[bsIndices[c][n][bd][:,0], bsIndices[c][n][bd][:,1]]	
#	print(bsValues)

	# Determine active state of active column neurons
	'''MAKE THIS MORE OPTIMIZED'''
	#nActive = np.einsum('i,ij->ij', cActive, nPredict) 
	for acIndex in cActiveIndices:
		flag = 0
		for n in range(numNeurons):
			active = nActive[acIndex][n]
			predict = nPredict[acIndex][n]			
			if predict == 1:
				active == 1
				flag = 1
		if flag == 0:
			for n in range(numNeurons):
				nActive[acIndex][n] = 1

	# Determine predictive state of all neurons

	return nActive	

temp = [0]*10
temp[0] = 1
temp[1] = 1
temp[2] = 1
inputs = np.array(temp)
numColumns = 10 #2048
numNeurons = 5  #32

print("Initializing...")
start = time.time()
psValues, psIndices, psPerms, psPermThreshs, nActive, nPredict, bsValues, bsIndices, bsPerms, bsPermThreshs = initLayer(inputs, numColumns, numNeurons)

end = time.time()
print("Initialization Time: {}s".format(end - start))

for i in range(1):
	start = time.time()
	cActive, cActiveIndices = spatialPooling(inputs, psValues, psIndices, psPerms, psPermThreshs, numColumns)
	end = time.time()
	print("Spatial Pooling Time: {}s".format(end - start))
	
	start = time.time()
	nActive = temporalMemory(bsValues, bsIndices, bsPerms, bsPermThreshs, cActive, cActiveIndices, nActive, nPredict, numNeurons)
	end = time.time()
	print("Temporal Memory Time: {}s".format(end - start))
