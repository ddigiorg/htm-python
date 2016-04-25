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
	def __init__(self, neurons):
		self.neurons = neurons

	def getNeuron(self, index):
		return self.neurons[index]

class Neuron(object):
	def __init__(self, dendrites):
		self.dendrites = dendrites

	def getDendrite(self, index):
		return self.dendrites[index]

class Dendrite(object):
	def __init__(self, synapses):
		self.synapses = synapses 

	def getSynapse(self, index):
		return self.synapses[index]

class Synapse(object):
	def __init__(self):
		self.permanance = 0.0

	def getPermanance(self):
		return self.permanance

n_regions   = 1
n_columns   = 1
n_neurons   = 1
n_dendrites = 1
n_synapses  = 2

regions   = [None]*n_regions
columns   = [None]*n_columns
neurons   = [None]*n_neurons
dendrites = [None]*n_dendrites
synapses  = [None]*n_synapses

for r in range(n_regions):
	for c in range(n_columns):
		for n in range(n_neurons):
			for d in range(n_dendrites):
				for s in range(n_synapses):
					synapses[s] = Synapse()
				dendrites[d] = Dendrite(synapses)
			neurons[n] = Neuron(dendrites)
		columns[c] = Column(neurons)
	regions[r] = Region(columns)
cortex = Cortex(regions)

print(cortex.getRegion(0).getColumn(0).getNeuron(0).getDendrite(0).getSynapse(1).getPermanance())
