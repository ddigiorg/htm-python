import random as random
import math as math

n_regions = None 
n_columns = None
n_neurons = None
n_dendrites_proximal = None
n_dendrites_apical = None
n_dendrites_basal = None
n_synapses_proximal = None
n_synapses_apical = None
n_synapses_basal = None

n_active_columns = None

INACTIVE = 0
ACTIVE = 1
PREDICTIVE = 2

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
	def __init__(self, neurons, dendrites_proximal):
		self.dendrites_proximal = dendrites_proximal
		self.neurons = neurons

	def getProximalDendrites(self):
		return self.dendrites_proximal

	def getNeurons(self):
		return self.neurons

class Neuron(object):
	def __init__(self, dendrites_apical, dendrites_basal):
		self.dendrites_apical = dendrites_apical
		self.dendrites_basal  = dendrites_basal
		self.axon = 0

	def setAxon(self, value):
		self.axon = value

	def getApicalDendrites(self):
		return self.dendrites_apical

	def getBasalDendrites(self):
		return self.dendrites_basal

	def getAxon(self):
		return self.axon

class Dendrite(object):
	def __init__(self, synapses):
		self.synapses = synapses 

	def getSynapses(self):
		return self.synapses

class Synapse(object):
	def __init__(self):
		self.connection_address = 0
		self.permanance = 0

	def updatePermanance(self, value):
		self.permanance += value
		if self.permanance > 100: self.permanance = 100
		if self.permanance <   0: self.permanance = 0

	def setConnectionAddress(self, value):
		self.connected = value

	def getPermanance(self):
		return self.permanance

	def getConnectionAddress(self):
		return self.connected

def initDendrites(n_dendrites, n_synapses):
	dendrites = [None]*n_dendrites
	for d in range(n_dendrites):
		synapses = [None]*n_synapses
		for s in range(n_synapses):
			synapses[s] = Synapse()
		dendrites[d] = Dendrite(synapses)

	return dendrites

def initNeurons(n_neurons):
	neurons = [None]*n_neurons
	for n in range(n_neurons):
#		dendrites_apical = initDendrites(n_dendrites_apical, n_synapses_apical)
		dendrites_apical = None
		dendrites_basal  = initDendrites(n_dendrites_basal , n_synapses_basal )
		neurons[n] = Neuron(dendrites_apical, dendrites_basal)

	return neurons

def initColumns(n_columns, n_dendrites_proximal):
	columns = [None]*n_columns
	dendrites_proximal = [None]*n_dendrites_proximal
	for c in range(n_columns):
		neurons = initNeurons(n_neurons) 
		dendrites_proximal = initDendrites(n_dendrites_proximal, n_synapses_proximal)
		columns[c] = Column(neurons, dendrites_proximal)
		
	return columns

def initRegion(inputs, c, n, d, s):
	global n_columns, n_neurons
	global n_dendrites_proximal, n_dendrites_apical, n_dendrites_basal
	global n_synapses_proximal,  n_synapses_apical,  n_synapses_basal

	n_columns = c
	n_neurons = n
	n_dendrites_proximal = 1
	n_dendrites_apical = d
	n_dendrites_basal  = d
	n_synapses_proximal = int(len(inputs)/2)
	n_synapses_apical = s
	n_synapses_basal  = s

	columns = initColumns(n_columns, n_dendrites_proximal)

	region = Region(columns)	

	return region

def initCortex(regions):
	global n_regions
	n_regions = r

	cortex = Cortex(regions)
	return cortex

def initConnections(inputs, region):
	global n_columns, n_synapses_proximal

	synapse_threshold = 20

	for c in range(n_columns):

		# Potential Pool: a random subset of inputs based on number of proximal dendrite synapses (usually 50% of input size)
		inputs_addresses = list(range(len(inputs)))
		random.shuffle(inputs_addresses)
		potential_pool = inputs_addresses[0:n_synapses_proximal]

		for s in range(n_synapses_proximal):
			synapse = region.getColumns()[c].getProximalDendrites()[0].getSynapses()[s]
			# Link potential pool address to proximal dendrite synapse
			synapse.setConnectionAddress(potential_pool[s])

			# Randomize synapse permanance around threshold
			synapse.updatePermanance(synapse_threshold + random.randint(0, 1))

	return region

def runSpatialPooler(inputs, region):
	global n_columns, n_active_columns,  n_neurons, n_dendrites_proximal, n_synapses_proximal

	synapse_threshold = 20
	active_percentage = 0.02
	learning_rate = 1

	# Overlap Score: for each column compute the overlap score  
	overlap_score = [0]*n_columns
	for c in range(n_columns):
		proximal_dendrite = region.getColumns()[c].getProximalDendrites()[0]
		for s in range(n_synapses_proximal):
			synapse = proximal_dendrite.getSynapses()[s]
			synapse_address = synapse.getConnectionAddress()
			synapse_permanance = synapse.getPermanance()
			if synapse_permanance > synapse_threshold:
				overlap_score[c] = overlap_score[c] + inputs[synapse_address]
#	print("overlap score {}".format(overlap_score))

	# Active Columns: enforce sparcity by selecting a subset of active columns from the top overlap scores (usually top 2%)
	n_active_columns = math.ceil(n_columns*active_percentage)
	active_columns_addresses = [0]*n_active_columns
	for ac in range(n_active_columns):
		column_highest_score_address = overlap_score.index(max(overlap_score))
		active_columns_addresses[ac] = column_highest_score_address
		overlap_score[column_highest_score_address] = 0
#	print("active columns addresses: {}".format(active_columns_addresses))

	# Learning: look at active column's proximal dendrites and strengthen or weaken the synapse permanance
	learning_rate = 1
	permanance = [[0]*n_synapses_proximal]*n_active_columns

	for ac in range(n_active_columns):
		c = active_columns_addresses[ac]
		proximal_dendrite = region.getColumns()[c].getProximalDendrites()[0]
		for s in range(n_synapses_proximal):
			synapse = proximal_dendrite.getSynapses()[s]
			address = synapse.getConnectionAddress()
			if inputs[address] == 1:
				synapse.updatePermanance(learning_rate)
			else:
				synapse.updatePermanance(-learning_rate)
			permanance[ac][s] = synapse.getPermanance()
#	print("permanance: {}".format(permanance))

	return active_columns_addresses

def runTemporalPooler(active_columns_addresses, region):
	global n_columns, n_active_columns, n_neurons, n_dendrites_proximal, n_synapses_proximal

	zeroNeuronAxon(region)
	
	# For every active columns check if neurons in predeictive state.  If so activate them
	for ac in range(n_active_columns):
		axon_predictive_state = False
		c = active_columns_addresses[ac]	
		column = region.getColumns()[c]
		for n in range(n_neurons):
			neuron = column.getNeurons()[n] 
			axon = neuron.getAxon()
			if axon == PREDICTIVE:
				neuron.setAxon(ACTIVE)
				axon_predictive_state = True
		if axon_predictive_state == False:
			for n in range(n_neurons):
				neuron = column.getNeurons()[n] 
				neuron.setAxon(ACTIVE)
			
	return region

def zeroNeuronAxon(region):
	global n_columns, n_active_columns, n_neurons, n_dendrites_proximal, n_synapses_proximal

	for c in range(n_columns):
		for n in range(n_neurons):
			region.getColumns()[c].getNeurons()[n].setAxon(INACTIVE)
