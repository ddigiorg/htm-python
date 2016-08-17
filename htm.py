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
	def __init__(self, inum_cells, num_columns, num_cells_per_column):
		self.num_columns   = num_columns
		self.num_cells_per_column = num_cells_per_column

		self.columns = [Column(inum_cells, num_cells_per_column) for c in range(num_columns)]
		self.sp = SpatialPooler(self.columns)
		self.tm = TemporalMemory(self.columns, num_cells_per_column)

		self.active_columns = []

		self.prev_active_cells  = []
		self.prev_predict_cells = []
		self.prev_winner_cells  = []

		self.active_cells  = []
		self.predict_cells = []
		self.winner_cells  = []

	def runSpatialPooler(self, inputs):
		self.active_columns = self.sp.compute(inputs, self.columns)

	def runTemporalMemory(self):
		self.prev_active_cells  = self.active_cells[:]
		self.prev_predict_cells = self.predict_cells[:]
		self.prev_winner_cells  = self.winner_cells[:]

		(self.active_cells, 
         self.predict_cells, 
         self.winner_cells) = self.tm.compute(
            self.active_columns, 
            self.prev_active_cells,
            self.prev_predict_cells,
            self.prev_winner_cells)


############################################################################
class Column(object):
	PS_CONNECTIVITY     = 0.5
	PS_THRESHOLD        = 20
	PS_LEARNING_RATE    = 1
	PS_PERMANENCE_LOWER = 0
	PS_PERMANENCE_UPPER = 99
	AC_PERCENT          = 0.02

	def __init__(self, inum_cells, num_cells_per_column):
		self.ps_size = int(inum_cells * self.PS_CONNECTIVITY)
		self.ps_addresses   = np.random.choice(inum_cells, self.ps_size, replace=False)
		self.ps_permanences = np.random.random_integers(self.PS_THRESHOLD, self.PS_THRESHOLD + 1, self.ps_size)

		self.cells = [Cell() for cell in range(num_cells_per_column)]

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

		self.prev_active_dendrites = []
		self.prev_learn_dendrites = []
		self.active_dendrites = []
		self.learn_dendrites = []

	def dendritesSet(self):
		self.prev_active_dendrites = self.active_dendrites
		self.prev_learn_dendrites  = self.learn_dendrites
		self.active_dendrites = []
		self.learn_dendrites  = []

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

	def __init__(self, columns):
		self.num_columns = len(columns)
		self.ps_size = columns[0].ps_size
		self.ps_threshold = columns[0].PS_THRESHOLD
		self.ac_percent = columns[0].AC_PERCENT
		self.anum_columns = int( self.num_columns * self.ac_percent )

	def compute(self, axons, columns):
		active_columns = []

		# Boosting
		"""ADD BOOSTING TO SPATIAL POOLER"""

		# Overlap: For each column sum the input axon states of connected proximal synapses (synapses above permanence threshold)
		overlap = np.zeros(self.num_columns)
		for c in range(self.num_columns):
			if_ps_connected = columns[c].ps_permanences > self.ps_threshold
			ps_values = np.logical_and( axons[columns[c].ps_addresses], if_ps_connected )
			overlap[c] = np.sum(ps_values)

		"""ADD RANDOM TIEBREAKER IF MULTIPLE OVERLAP SCORES ARE  MAX"""
		# Inhibiion: Active column addresses are the indices of maximum values in overlap list
		for ac in range(self.anum_columns):
			active_column = np.argmax(overlap)
			active_columns.append(active_column)
			overlap[active_columns] = 0

		# Learning
		for ac in active_columns:
			columns[ac].dendriteAdapt(axons)

		return active_columns


#############################################################################
class TemporalMemory(object):

	def __init__(self, columns, num_cells_per_column):
		self.num_columns = len(columns)
		self.num_cells_per_column = num_cells_per_column
		self.num_cells = self.num_columns * self.num_cells_per_column

		self.columns = columns

		self.max_new_synapse_count = columns[0].cells[0].BS_MAX_NEW

	def compute(self,
                active_columns,
                prev_active_cells,
                prev_predict_cells,
                prev_winner_cells):

		active_cells  = []
		predict_cells = []
		winner_cells  = []


		cells_to_add = []
		winner_cell = []

		columns = self.columns

		for column in range(self.num_columns):

			a = False
			if column in active_columns:
				if columns[column].has_active_basal_dendrites:
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

		return (active_cells, predict_cells, winner_cells)

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

			self.columns[column].cells[best_cell_per_column].dendriteAdd(prev_winner_cells)
		
		return cells, best_cell
