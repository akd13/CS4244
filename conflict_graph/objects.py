from itertools import filterfalse


class Clause:
	def __init__(self, clause, clause_id):
		self.id = clause_id
		self.assigned_literals = {}
		# Initialise all clause literals to be false i.e unassigned
		for lit in clause:
			self.assigned_literals[lit] = None

		# self.unsatisfied will be False if not all literals have been assigned
		self.unsatisfied = False

	# Get clause ID
	def get_id(self):
		return self.id

	# Get list of literals found in this clause
	def get_literal_list(self):
		return list(self.assigned_literals.keys())

	# Checks if literal exists
	def lit_exists(self, lit):
		return lit in self.assigned_literals or -lit in self.assigned_literals

	# Get number of assigned literals in clause
	def get_num_assigned(self):
		sum_lit = 0
		for key in self.assigned_literals:
			if self.assigned_literals[key] is not None:
				sum_lit += 1
		return sum_lit

	# Update status of clause if it is unsat.
	def update_unsat(self):
		if self.get_num_assigned() == 0:
			self.unsatisfied = True
			for key in self.assigned_literals:
				if self.assigned_literals[key] is True:
					self.unsatisfied = False

	def set_literal(self, lit, boolean=None):
		if lit in self.assigned_literals:
			self.assigned_literals[lit] = boolean


class Node:
	def __init__(self, v, decision_level):
		self.v = v
		# each element is a pair (next_node, clause_id)
		self.children = []
		self.decision_level = decision_level

	def add_child(self, node, clause_id):
		self.children.append((node, clause_id))

	def get_decision_level(self):
		return self.decision_level


class Graph:
	def __init__(self):
		self.adjacency_list = []

	def get_adj_list(self):
		return self.adjacency_list

	def add_node(self, node):
		self.adjacency_list.append(node)

	# Removes nodes of decision level specified or higher (not tested yet)
	def remove_decision_level_nodes(self, decision_level):
		self.adjacency_list = filterfalse(lambda x: x.get_decision_level() >= decision_level, self.adjacency_list)
