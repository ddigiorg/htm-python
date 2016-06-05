import numpy as np

class TemporalMemory(object):

	def __init__(self, n_active_states, n_predict_states, n_learn_states, s_threshold, s_learning_rate, s_permanence_lower, s_permanence_upper, bs_addresses, bs_permanences):

		# Layer Data Variables
		self.n_active_states = n_active_states
		self.n_predict_states = n_predict_states
		self.n_learn_states = n_learn_states

		# Synapse Variables
		self.s_threshold = s_threshold
		self.s_learning_rate = s_learning_rate
		self.s_permanence_lower = s_permanence_lower
		self.s_permanence_upper = s_permanence_upper

		# Basal Synapse Data Variables
		self.bs_addresses = bs_addresses
		self.bs_permanences = bs_permanences

		# Other Variables
		self.num_columns = len(bs_addresses)
		self.num_neurons = len(bs_addresses[0])

	def run(self, ac_addresses):

		self.n_active_states[1] = self.n_active_states[0]

		# Active States
		for ac in ac_addresses:		
			in_predicted = False
#			n_learning_chosen = False

			for n in range(self.num_neurons):
				if self.n_predict_states[ac, n] == 1:
					in_predicted = True
					self.n_active_states[0, ac, n] = 1

			if in_predicted == False:
				for n in range(self.num_neurons):
					self.n_active_states[0, ac, n] = 1

		print(self.n_active_states[0])

		# Predict States


		# Learning
