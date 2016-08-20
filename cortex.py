"""
Stuff I learned:

After reading NuPIC's Connections.py, I agree with the principles of their approach
to structuring data.

The special attribute __slots__ allows you to explicitly state in your code which 
instance attributes you expect your object instances to have, with the expected results:
    + faster attribute access.
    + potential space savings in memory.
http://stackoverflow.com/questions/472000/usage-of-slots


"""

import numpy as np

class Synapse(object):

	__slots__ = ['address', 'permanence']

	def __init__(self, address, permanence):
		self.address = address
		self.permanence = permanence

#	def updateAddress(self, address):
#		self.address = address
#
#	def updatePermanence(self, permanence):
#		self.permanence = permanence

class Dendrite(object):
	def __init__(self):
		self.synapses = []

	def createSynapses(self, num_synapses, addresses, permanences):
		self.synapses = [ Synapse(addresses[s], permanences[s]) for s in range(num_synapses) ]
#		self.synapses = ( Synapse(addresses[s], permanences[s]) for s in range(num_synapses) )
#		self.synapses = map( lambda s: Synapse(addresses[s], permanences[s]), range(num_synapses) )

class Neuron(object):
	def __init__(self):
		self.basal_dendrites = []

#		self.isActive  = False
#		self.isPredict = False
#		self.isWinner  = False

	def createDendrite(self):
		self.proximal_dendrite = Dendrite()

class Column(object):
	def __init__(self):
		self.proximal_dendrite = Dendrite()

class Layer3b(object):
	def __init__(self, num_inputs, num_columns, num_neurons_per_column):
		self.num_columns = num_columns
		self.num_neurons = num_columns * num_neurons_per_column

		num_proximal_synapses = int(num_inputs * 0.5)
		initial_permanences = [21] * num_proximal_synapses
		potential_pool = list( range( num_inputs ) )

		self.columns = [Column() for _ in range(self.num_columns)]
		self.neurons = [Neuron() for _ in range(self.num_neurons)]

		# Initialize Synapses to Potential Pool
		for column in self.columns:
			proximal_dendrite = column.proximal_dendrite

			np.random.shuffle(potential_pool)
			addresses = potential_pool[0:num_proximal_synapses]

			proximal_dendrite.createSynapses(num_proximal_synapses, addresses, initial_permanences)

#		print( list(self.columns[0].proximal_dendrite.synapses) )
#			print( [synapse.address  for synapse in proximal_dendrite.synapses] )
#			print( [synapse.permanence for synapse in proximal_dendrite.synapses] )


#		self.active_columns = []
#		self.prev_active_cells  = []
#		self.prev_predict_cells = []
#		self.prev_winner_cells  = []
#		self.active_cells  = [] # [ cell, ... ]
#		self.predict_cells = []
#		self.winner_cells  = []
#		self.active_segments   = [] # [ [cell, segment] ... ]
#		self.matching_segments = []
