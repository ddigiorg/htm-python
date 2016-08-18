"""
TODO

+ Figure out better way to organize Column and Cell classes
+ Complete TemporalMemory
+ Add docstring comments for classes and methods
+ Address issues and comments

+ Consider adding receptive fields to Column class, aka initialize proximal synapses around certain

"""
# c   means column
# ac  means active column
# n   means cell
# npc means cell per column
# d   means dendrite segment
# s   means synapse
# ps  means proximal synapse
# bs  means basal synapse


import numpy as np

class Layer3b(object):
	def __init__(self, num_inputs, num_columns, num_cells_per_column):
		self.column_instances = [Column(num_inputs, num_cells_per_column) for _ in range(num_columns)]

		self.sp = SpatialPooler(self.column_instances)
		self.tm = TemporalMemory(self.column_instances, num_cells_per_column)

		self.active_columns = []

		self.prev_active_cells  = []
		self.prev_predict_cells = []
		self.prev_winner_cells  = []
		self.active_cells  = []
		self.predict_cells = []
		self.winner_cells  = []

	def runSpatialPooler(self, inputs):
		self.active_columns = self.sp.compute(inputs)

	def runTemporalMemory(self):
		self.tm.compute(self.active_columns) 


############################################################################
class Column(object):
	PS_CONNECTIVITY     = 0.5
	PS_THRESHOLD        = 20
	PS_LEARNING_RATE    = 1
	PS_PERMANENCE_LOWER = 0
	PS_PERMANENCE_UPPER = 99

	def __init__(self, num_inputs, num_cells_per_column):
		self.num_cells = num_cells_per_column

		self.cell_instances = [Cell() for _ in range(num_cells_per_column)]

		self.ps_size = int(num_inputs * self.PS_CONNECTIVITY)
		self.ps_addresses   = np.random.choice(num_inputs, self.ps_size, replace=False)
		self.ps_permanences = np.random.random_integers(self.PS_THRESHOLD, self.PS_THRESHOLD + 1, self.ps_size)

		self.has_active_basal_dendrites = False

	def dendriteAdapt(self, axons):
		ps_updates = self.PS_LEARNING_RATE * (2 * axons[self.ps_addresses] - 1)
		self.ps_permanences += ps_updates
		np.clip(self.ps_permanences, self.PS_PERMANENCE_LOWER, self.PS_PERMANENCE_UPPER, out=self.ps_permanences)
	
		"""MAKING THINGS UNSTABLE, KEEP OUT FOR NOW"""
		"""MAKE CLEARER CODE"""
#		for s in np.where(self.ps_permanences == 0)[0]:
#			connections = np.zeros(len(axons), dtype=np.int8)
#			connections[self.ps_addresses] = 1
#			new_addresses = np.where(connections == 0)[0]
#
#			self.ps_addresses[s]   = np.random.choice(new_addresses, None, replace=False)
#			self.ps_permanences[s] = self.PS_THRESHOLD + 1

	def computeOverlap(self, axons):
		if_ps_connected = self.ps_permanences > self.PS_THRESHOLD
		ps_values = np.logical_and( axons[self.ps_addresses], if_ps_connected )
		overlap = np.sum(ps_values)

		return overlap



#############################################################################
class Cell(object):
	BS_THRESHOLD        = 20
	BS_LEARNING_RATE    = 1
	BS_PERMANENCE_LOWER = 0
	BS_PERMANENCE_UPPER = 99
	BS_THRESHOLD2       = 1 # CHOOSE BETTER NAME
	BS_MAX_NEW          = 4 # DETERMINE BETTER WAY OF INITIALIZING THIS

	def __init__(self):
		self.bs_addresses = []
		self.bs_permanences = []

		self.active_dendrites = []
		self.learn_dendrites = []

	def dendriteActive(self, d, active_cells):
		overlap = np.sum( np.in1d(self.bs_addresses[d], active_cells) )
		if overlap >= self.BS_THRESHOLD2:
			self.active_dendrites.append(d)
			return True

	def dendriteAdd(self, prev_cells):
		self.bs_addresses.append(prev_cells)
		self.bs_permanences.append( [self.BS_THRESHOLD + 1] * len(prev_cells) )
		self.learn_dendrites.append( len(self.bs_addresses) - 1 )

	def dendriteAdapt(self, active_cells, is_winner_cell, num_cells):
		for d in self.prev_active_dendrites + self.learn_dendrites:
			if d in self.learn_dendrites or is_winner_cell:
				cell_axons = np.zeros(num_cells)
				cell_axons[active_cells] = 1

				bs_updates = self.BS_LEARNING_RATE * (2 * cell_axons[self.bs_addresses[d]] - 1)
				self.bs_permanences[d] += bs_updates


############################################################################
class SpatialPooler(object):
	ACTIVE_COLUMN_PERCENT = 0.02

	def __init__(self, column_instances):

		self.column_instances = column_instances
		self.num_columns = len(column_instances)
		self.num_active_columns = int( self.num_columns * self.ACTIVE_COLUMN_PERCENT )

	def compute(self, axons):
		active_columns = []

		# Boosting
		"""ADD BOOSTING TO SPATIAL POOLER"""

		# Overlap
		overlap = np.zeros(self.num_columns)
		for column in range(self.num_columns):
			overlap[column] = self.column_instances[column].computeOverlap(axons)

		# Inhibiion
		"""ADD RANDOM TIEBREAKER IF MULTIPLE OVERLAP SCORES ARE  MAX"""
		for ac in range(self.num_active_columns):
			active_column = np.argmax(overlap)
			active_columns.append(active_column)
			overlap[active_columns] = 0

		# Learning
		for active_column in active_columns:
			self.column_instances[active_column].dendriteAdapt(axons)

		return active_columns


#############################################################################
class TemporalMemory(object):

	def __init__(self, column_instances, num_cells_per_column):
		self.column_instances = column_instances
		self.num_columns = len(column_instances)
		self.num_cells_per_column = num_cells_per_column
		self.num_cells = self.num_columns * self.num_cells_per_column

		self.max_new_synapse_count = column_instances[0].cell_instances[0].BS_MAX_NEW

	def compute(self, active_columns):

		for column in range(self.num_columns):

			cells_to_add = []
			winner_cell = []

			prev_winner_cells = column_instances[column].prev_winner_cells

			a = False
			if column in active_columns:
				if self.column_instances[column].has_active_basal_dendrites:
					self.activatePredictedColumn(column)
					active_cells += cells_to_add
					winner_cells += cells_to_add 
				else:
					cells_to_add, winner_cell = self.burstColumn(column, prev_winner_cells)
					active_cells += cells_to_add
					winner_cells.append(winner_cell)

		# Make better
		columns[column].has_active_basal_dendrites = False
		for cell in range(self.num_cells_per_column):
			num_dendrites = len( columns[column].cells[cell].bs_addresses )
			for dendrite in range(num_dendrites):
				if columns[column].cells[cell].dendriteActive(active_cells):
					columns[column].has_active_basal_dendrites = True

#	def activatePredictedColumn(self, column):
 

	def burstColumn(self, column, prev_winner_cells):
		start = column * self.num_cells_per_column
		cells = range(start, start + self.num_cells_per_column)

		# if matching segment is not none
		# e#lse
		best_cell = np.random.choice(cells, 1)[0]
		num_added_synapses = min( self.max_new_synapse_count, len(prev_winner_cells) )
		if num_added_synapses > 0:

			# make better
			best_cell_per_column = best_cell - (column * self.num_cells_per_column)

			self.column_instances[column].cells[best_cell_per_column].dendriteAdd(prev_winner_cells)
		
		return cells, best_cell
