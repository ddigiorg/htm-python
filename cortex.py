class Cortex(object):
	def __init__(self, regions):
		self.regions = regions

	def getRegion(self, index):
		return self.regions[index]

class Region(object):
	def __init__(self, columns):
		self.columns = columns

	def getColumn(self, index):
		return self.columns[index]

class Column(object):
	def __init__(self, neurons, proximal_dendrite):
		self.proximal_dendrite = proximal_dendrite
		self.neurons = neurons

	def getProximalDendrite(self):
		return self.proximal_dendrite

	def getNeuron(self, index):
		return self.neurons[index]

class Neuron(object):
	def __init__(self, apical_dendrites, basal_dendrites):
		self.apical_dendrites = apical_dendrites
		self.basal_dendrites = basal_dendrites
		self.axon_output = 0

	def setAxonOutput(self, value):
		self.axon_output = value

	def getApicalDendrite(self, index):
		return self.apical_dendrites[index]

	def getBasalDendrite(self, index):
		return self.basal_dendrites[index]

	def getAxonOutput(self):
		return self.axon_output

class Dendrite(object):
	def __init__(self, synapses):
		self.synapses = synapses 

	def getSynapse(self, index):
		return self.synapses[index]

class Synapse(object):
	def __init__(self):
		self.permanance = 0.0
		self.connected = 0

	def setPermanance(self, value):
		self.permanance = value

	def setConnected(self, value):
		self.connected = value

	def getPermanance(self):
		return self.permanance

	def getConnected(self):
		return self.connected

def InitCortex(n_regions, n_columns, n_neurons, n_dendrites, n_synapses):
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

cortex = InitCortex(1, 1, 1, 1, 1)

cortex.getRegion(0).getColumn(0).getNeuron(0).getBasalDendrite(0).getSynapse(0).setPermanance(1.0)
print(cortex.getRegion(0).getColumn(0).getNeuron(0).getBasalDendrite(0).getSynapse(0).getPermanance())
print(cortex.getRegion(0).getColumn(0).getNeuron(0).getAxonOutput())
