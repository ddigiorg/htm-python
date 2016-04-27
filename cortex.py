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

	def setPermanance(self, value):
		self.permanance = value

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

	print(n_columns)
	print(n_neurons)

	return cortex

def runSpatialPooler(inputs, region):
	
	return region
