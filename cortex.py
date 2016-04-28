import random as random
import math as math

class Cortex(object):
	def __init__(self, regions):
		self.regions = regions

	def getRegions(self):
		return self.regions

class Region(object):
	def __init__(self, columns):
		self.columns = columns

	def getColumns(self):
		return self.columns

class Column(object):
	def __init__(self, neurons, proximal_dendrite):
		self.proximal_dendrite = proximal_dendrite
		self.neurons = neurons

	def getProximalDendrite(self):
		return self.proximal_dendrite

	def getNeurons(self):
		return self.neurons

class Neuron(object):
	def __init__(self, apical_dendrites, basal_dendrites):
		self.apical_dendrites = apical_dendrites
		self.basal_dendrites = basal_dendrites
		self.axon_output = 0

	def setAxonOutput(self, value):
		self.axon_output = value

	def getApicalDendrites(self):
		return self.apical_dendrites

	def getBasalDendrites(self):
		return self.basal_dendrites

	def getAxonOutput(self):
		return self.axon_output

class Dendrite(object):
	def __init__(self, synapses):
		self.synapses = synapses 

	def getSynapses(self):
		return self.synapses

class Synapse(object):
	def __init__(self):
		self.connection_address = 0
		self.permanance = 0.0

	def updatePermanance(self, value):
		self.permanance += value
		if self.permanance > 1.0: self.permanance = 1.0
		if self.permanance < 0.0: self.permanance = 0.0

	def setConnectionAddress(self, value):
		self.connected = value

	def getPermanance(self):
		return self.permanance

	def getConnectionAddress(self):
		return self.connected

def initCortex(n_regions, n_columns, n_neurons, n_dendrites, n_synapses):
	regions = [None]*n_regions
	for r in range(n_regions):
		columns = [None]*n_columns
		proximal_dendrite = [None]
		for c in range(n_columns):
			neurons = [None]*n_neurons
			for n in range(n_neurons):
				apical_dendrites = [None]*n_dendrites
				basal_dendrites = [None]*n_dendrites
				for d in range(n_dendrites):
					synapses = [None]*n_synapses
					for s in range(n_synapses):
						synapses[s] = Synapse()
					apical_dendrites[d] = Dendrite(synapses)
					basal_dendrites[d] = Dendrite(synapses)
				neurons[n] = Neuron(apical_dendrites, basal_dendrites)
			proximal_dendrite = Dendrite(synapses)
			columns[c] = Column(neurons, proximal_dendrite)
		regions[r] = Region(columns)
	cortex = Cortex(regions)
	return cortex

def initSynapticConnections(inputs, cortex):

	n_columns = len(cortex.getRegions()[0].getColumns())
	n_neurons = len(cortex.getRegions()[0].getColumns()[0].getNeurons())
	n_proximal_synapses = len(cortex.getRegions()[0].getColumns()[0].getProximalDendrite().getSynapses())

	synapse_threshold = 0.2	

	for c in range(n_columns):

		# Potential Pool: a random subset of inputs based on number of proximal dendrite synapses (usually 50% of input size)
		inputs_addresses = list(range(len(inputs)))
		random.shuffle(inputs_addresses)
		potential_pool = inputs_addresses[0:n_proximal_synapses]

		for s in range(n_proximal_synapses):
			synapse = cortex.getRegions()[0].getColumns()[c].getProximalDendrite().getSynapses()[s]
			# Link potential pool address to proximal dendrite synapse
			synapse.setConnectionAddress(potential_pool[s])

			# Randomize synapse permanance around threshold
			synapse.updatePermanance(synapse_threshold + 0.1*random.randint(-1, 1))

	return cortex

def runSpatialPooler(inputs, cortex):

	n_columns = len(cortex.getRegions()[0].getColumns())
	n_neurons = len(cortex.getRegions()[0].getColumns()[0].getNeurons())
	n_proximal_synapses = len(cortex.getRegions()[0].getColumns()[0].getProximalDendrite().getSynapses())

	# For each column compute the overlap score
	overlap_score = [0]*n_columns
	synapse_threshold = 0.2

	for c in range(n_columns):
		overlap_score[c] = 0 
		for s in range(n_proximal_synapses):
			synapse_address = cortex.getRegions()[0].getColumns()[c].getProximalDendrite().getSynapses()[s].getConnectionAddress()
			synapse_permanance = cortex.getRegions()[0].getColumns()[c].getProximalDendrite().getSynapses()[s].getPermanance()
			if synapse_permanance > synapse_threshold:
				overlap_score[c] = overlap_score[c] + inputs[synapse_address]

	print("overlap score {}".format(overlap_score))

	# Enforce sparcity by selecting a subset of active columns from the top overlap scores (usually top 2%)
	n_active_columns = math.ceil(len(overlap_score)*0.02)
	active_columns_addresses = [0]*n_active_columns

	for ac in range(n_active_columns):
		highest_score_address = overlap_score.index(max(overlap_score))
		active_columns_addresses[ac] = highest_score_address
		del overlap_score[highest_score_address] 

	print("active columns addresses: {}".format(active_columns_addresses))

	# Learning: look at active column's proximal dendrites and strengthen or weaken the synapse permanance
	learning_rate = 0.1
	permanance = [[0.0]*n_proximal_synapses]*n_active_columns

	for ac in range(n_active_columns):
		c = active_columns_addresses[ac] 
		for s in range(n_proximal_synapses):
			synapse = cortex.getRegions()[0].getColumns()[c].getProximalDendrite().getSynapses()[s]
			address = synapse.getConnectionAddress()
			if inputs[address] == 1:
				synapse.updatePermanance(learning_rate)
			else:
				synapse.updatePermanance(-learning_rate)
			permanance[ac][s] = synapse.getPermanance()

	print(permanance)

	#update neuron axon output
	for ac in range(n_active_columns):
		for n in range(n_neurons):
			cortex.getRegions()[0].getColumns()[ac].getNeurons()[n].setAxonOutput(1)

	return cortex
