import re
from itertools import filterfalse
import random
import numpy as np
import copy
import heapq


def add_arguments(filename, heuristic):
	"""
	Check validity of each clause and adds to clause set
	:return: Solver
	"""
	file = open(filename, "r")
	num_variables = 0
	cnf = []

	for line in file:
		comment = re.search('^\s*(p|c).*(\n)*$', line)
		header = re.search('^\s*(p)\s+(cnf)\s+(\d+)\s+(\d+)(\n)*$', line)
		clause_input_cnf = re.search('^\s*((-)*\d+\s*)*(0)(\\n)*$', line)  # detect clause

		if header is not None:
			num_variables = int(line.split()[2])

		if comment is None and clause_input_cnf is None:
			print("Invalid input:", line)

		elif clause_input_cnf is not None:
			raw_clause = clause_input_cnf.group(0).split()
			raw_clause.pop()
			clause = [int(numeric_string) for numeric_string in raw_clause]
			cnf.append(clause)
	solver = SATSolverCDCL(cnf, num_variables, heuristic)
	file.close()
	del file, filename, num_variables, comment, header, clause_input_cnf, raw_clause
	return solver


class SATSolverCDCL:
	def __init__(self, cnf, num_variables, heuristic):
		self.cnf = cnf
		self.count = 0
		self.literals = np.full(num_variables, -1)
		self.clause_list = []
		self.variable_frequency = np.zeros(num_variables, dtype=int)
		self.literal_count = 0
		self.clause_count = 0
		self.conflict_antecedent = -1
		self.literal_decision_level = np.full(num_variables, -1)
		self.literal_antecedent = np.full(num_variables, -1)
		self.unsatisfied = False
		self.previous_var = None

		# Heuristics for pick-branching
		self.literal_frequency = np.zeros(num_variables, dtype=int)
		self.literal_polarity = np.zeros(num_variables, dtype=int)
		self.two_clause = []
		self.two_clause_previous_state = []
		self.vsids_frequency = {}
		self.choice = heuristic

		for clause in self.cnf:
			if not clause:
				self.unsatisfied = True
			self.clause_list.append(clause)

		for i in range(num_variables):
			self.vsids_frequency[-i-1] = 0
			self.vsids_frequency[i+1] = 0

		for clause in self.cnf:
			if len(clause) == 2:
				self.two_clause.append(clause)
			for literal in clause:
				if literal > 0:
					self.literal_frequency[literal-1] += 1
					self.literal_polarity[literal-1] += 1
					self.vsids_frequency[literal] += 1
				else:
					self.literal_frequency[-literal-1] += 1
					self.literal_polarity[-literal-1] -= 1
					self.vsids_frequency[literal] += 1

		self.variable_frequency = [abs(num) for num in self.literal_frequency]
		self.two_clause_previous_state = self.two_clause
		self.literal_count = num_variables
		self.clause_count = len(self.cnf)

	def unit_propagate(self, decision_level):
		"""
		Carries out iterative application of unit clause rule.
		If unit clauses found, assigns variable.
		If conflict found, stores the conflict antecedent.
		:return: Satisfiability status (unresolved or unsat)
		"""
		while True:
			unit_clause_found = False
			for id,clause in enumerate(self.clause_list):
				assigned = 0
				unit_clause_unassigned_lit = None
				conflict = True
				unassigned_clause = True
				for lit in clause:
					if(self.literals[abs(lit)-1]!=-1):
						assigned += 1
						if(self.literals[abs(lit)-1]>0 and lit>0) or (self.literals[abs(lit)-1]==0 and lit<0): #check if the clause is already satisfied
							conflict = False
							unassigned_clause = False
					if(self.literals[abs(lit)-1]==-1):
						unit_clause_unassigned_lit = lit

				if(len(clause)==assigned+1 and unassigned_clause == True): #all except one variable is assigned and clause is not satisfied yet, unit clause found
					self.assign_var(unit_clause_unassigned_lit, decision_level, id)
					unit_clause_found = True
					break

				if(len(clause) == assigned): #all variables assigned, do satisfiability check
					if(conflict == True):
						self.conflict_antecedent = id
						return 'unsatisfied'

			if(unit_clause_found == False):
				break


		self.conflict_antecedent = -1
		return 'unresolved'

	def assign_var(self, variable, decision_level, antecedent):
		"""
		Assigns literal to ensure satisfiability of clause at current decision level
		:return: None
		"""
		literal_id = abs(variable)-1
		value = 1 if variable > 0 else 0
		self.literals[literal_id] = value
		self.literal_decision_level[literal_id] = decision_level
		self.literal_antecedent[literal_id] = antecedent
		self.literal_frequency[literal_id] = -1
		del literal_id, value

	def learn_conflict_backtrack(self, conflict_decision_level):
		"""
		Analyzes conflict and learns a new clause using resolution
		:return: decision level to backtrack to
		"""
		conflict_clause = self.clause_list[self.conflict_antecedent]

		learnt_clause, resolver_literal = self.cut_graph_UIP(conflict_clause, conflict_decision_level)
		self.clause_list.append(learnt_clause)

		self.update_parameters_pickbranching(learnt_clause)

		self.clause_count += 1
		backtrack_to_decision_level = 0
		for lit in learnt_clause:
			literal_id = abs(lit)-1
			literal_decision_level = self.literal_decision_level[literal_id]
			if literal_decision_level != conflict_decision_level and literal_decision_level > backtrack_to_decision_level:
				backtrack_to_decision_level = literal_decision_level
			del lit

		for i, lit in enumerate(self.literals):
			if self.literal_decision_level[i] > backtrack_to_decision_level:
				# Un-assigning literals till the level we backtrack to
				self.literals[i] = -1
				self.literal_decision_level[i] = -1
				self.literal_antecedent[i] = -1
				self.literal_frequency[i] = self.variable_frequency[i]
			del i, lit

		del conflict_clause, learnt_clause, conflict_decision_level, resolver_literal
		return backtrack_to_decision_level

	def cut_graph_UIP(self, conflict_clause, conflict_decision_level):
		"""
		Analyzes implication graph to get cut
		If there is a UIP, uses UIP as resolver literal
		and its antecedents to learn new clause
		:return: learnt clause and resolver literal
		"""
		resolver_literal = None
		while True:
			num_literal_assigned_at_level = 0
			for l in conflict_clause:
				literal = abs(l) - 1
				current_decision_level = self.literal_decision_level[literal]
				current_antecedent = self.literal_antecedent[literal]

				# if the literal's decision level is same as that of conflict
				if self.literal_decision_level[literal] == conflict_decision_level:
					num_literal_assigned_at_level += 1

				# if there's no UIP, use this as resolver
				if current_decision_level == conflict_decision_level and current_antecedent != -1:
					resolver_literal = literal

			if num_literal_assigned_at_level == 1:  # if there is exactly one literal assigned here, this is a UIP
				break

			conflict_clause = self.resolution(conflict_clause, resolver_literal)

		learnt_clause = conflict_clause

		return learnt_clause, resolver_literal


	def update_parameters_pickbranching(self, learnt_clause):
		"""
		Updates frequencies for pick-branching heuristics
		:return: None
		"""
		if len(learnt_clause) == 2:
			self.two_clause.append(learnt_clause)
		self.initiate_vsids_decay()
		for lit in learnt_clause:
			literal_id = abs(lit) - 1
			update = 1 if lit > 0 else -1
			self.literal_polarity[literal_id] += update
			if self.literal_frequency[literal_id] != -1:
				self.literal_frequency[literal_id] += 1
			self.variable_frequency[literal_id] += 1
			self.vsids_frequency[lit] += 2

	def resolution(self, current_clause, resolver_literal):
		"""
		Resolves two clauses on a resolver literal to learn a new clause
		:return: learnt clause
		"""
		conflict_clause = self.clause_list[self.literal_antecedent[resolver_literal]]
		learnt_clause = current_clause + conflict_clause
		learnt_clause[:] = filterfalse(lambda x: x == resolver_literal + 1 or x == -resolver_literal - 1, learnt_clause)
		learnt_clause = list(set(learnt_clause))
		del conflict_clause
		return learnt_clause

	def pick_branching_choice(self):
		"""
		Pick branching based on selected heuristic
		:return: variable of heuristic's choice
		"""
		options = {'random': self.random_choice(),
				   'random_frequency': self.random_frequency(),
				   '2-clause': self.two_clause_choice(),
				   'DLIS': self.DLIS(),
				   'VSIDS_nodecay': self.VSIDS_nodecay(),
				   'VSIDS': self.VSIDS()}
		return options[self.choice]

	def random_choice(self):
		"""
		Lists all the unassigned variables and picks randomly
		:return: randomly picked variable
		"""
		unassigned_list = {}
		for i in range(0, self.literal_count):
			if self.literals[i] == -1:
				unassigned_list[i+1] = 1

		choose = random.choice(list(unassigned_list))
		if self.literal_polarity[choose-1] >= 0:
			return choose
		else:
			return -choose

	def random_frequency(self):
		"""
		Lists all the unassigned variables based on frequency and picks randomly
		:return: randomly picked variable
		"""
		unassigned_list = []
		for i in range(0, self.literal_count):
			if self.literals[i] == -1:
				for j in range(0, self.literal_frequency[i]):
					unassigned_list.append(i)

		if(not unassigned_list):
			return self.first_unassigned_variable()
		else:
			variable = random.choice(unassigned_list)
			if self.literal_polarity[variable] >= 0:
				return variable + 1
			else:
				return -variable - 1

	def two_clause_choice(self):
		"""
		Returns the most frequently appearing literal in two clauses.
		To avoid picking the same variable repeatedly,
		if there are no changes in the number of two clauses,
		random heuristic will be chosen.
		:return: two-clause variable
		"""

		# if the number of two clauses haven't changed, select randomly
		if self.count != 0 and self.two_clause == self.two_clause_previous_state:
			variable = self.random_frequency()
			return variable
		else:
			variable = self.most_frequent_literal_in_two_clause()
			return variable

	def most_frequent_literal_in_two_clause(self):
		"""
		Two-clause helper method, finds the
		most frequently appearing literal in two-clauses.
		Breaks ties randomly.
		:return: 2-clause literal
		"""
		self.two_clause_previous_state = self.two_clause
		two_clause_lit_frequency = np.zeros(self.literal_count+1)
		for clause in self.two_clause:
			for l in clause:
				two_clause_lit_frequency[abs(l)] += 1

		max_value = np.amax(two_clause_lit_frequency)
		indices = [i for i, j in enumerate(two_clause_lit_frequency) if j == max_value]
		return random.choice(indices)

	def DLIS(self):
		"""
		Dynamic Largest Individual Sum picks the most
		frequently appearing literal in unresolved clauses.
		Due to the nature of deepcopy, if the number of
		assigned literals is past a certain threshold,
		VSIDS_nodecay will be used.
		:return: DLIS variable
		"""
		if self.count > self.literal_count/2:
			return self.VSIDS_nodecay()

		unresolved_clauses = copy.deepcopy(self.clause_list)
		literal_list = range(-self.literal_count, self.literal_count+1)
		current_literal_count = dict.fromkeys(literal_list, 0)
		current_literal_count.pop(0)

		for clause in unresolved_clauses:
			for lit in clause:
				if(lit > 0 and self.literals[lit-1] == 1) or (lit < 0 and self.literals[-lit-1] == 0):
						unresolved_clauses.remove(clause)
						break
		for clause in unresolved_clauses:
			for lit in clause:
				current_literal_count[lit] += 1
		for i in range(0, self.literal_count):
			if self.literals[i] != -1:
				current_literal_count.pop(i+1)
				current_literal_count.pop(-i-1)

		max_count = max(current_literal_count.values())
		keys_list = [k for k, v in current_literal_count.items() if v == max_count]

		variable = random.choice(keys_list)
		if variable != self.previous_var:
			return variable
		else:
			return self.first_unassigned_variable()

	def VSIDS_nodecay(self):
		"""
		Picks the most frequently appearing literal.
		:return: VSIDS non-decayed variable
		"""
		unassigned_list = {}
		for i in range(0, self.literal_count):
			if self.literals[i] == -1:
					unassigned_list[i+1] = self.literal_frequency[i]

		max_frequency_value = max(unassigned_list.values())
		keys_list = [k for k, v in unassigned_list.items() if v == max_frequency_value]
		variable = random.choice(keys_list)
		if variable != self.previous_var:
			return variable
		else:
			return self.first_unassigned_variable()

	def VSIDS(self):
		"""
		Uses VSIDS heuristic to find the literal with max value.
		:return: VSIDS literal
		"""
		unassigned_list = {}
		for i in range(0, self.literal_count):
			if self.literals[i] == -1:
				unassigned_list[i+1] = self.vsids_frequency[i+1]
				unassigned_list[-i-1] = self.vsids_frequency[-i-1]

		max_decay_count = max(unassigned_list.values())
		keys_list = [k for k, v in unassigned_list.items() if v == max_decay_count]
		variable = random.choice(keys_list)
		if variable != self.previous_var:
			return variable
		else:
			return self.first_unassigned_variable()

	def initiate_vsids_decay(self):
		"""
		Pick decay constant and update frequencies for VSIDS heuristic
		:return:
		"""
		decay_constant = np.random.uniform()
		self.vsids_frequency.update((x, y * decay_constant) for x, y in self.vsids_frequency.items())

	def first_unassigned_variable(self):
		"""
		:return: The first unassigned variable,
		used if a heuristic repeatedly picks the same variable.
		"""
		for i in range(0, self.literal_count):
			if self.literals[i] == -1:
				return i + 1

	def check_all_assigned(self):
		"""
		Checks if all literals are assigned
		:return: boolean
		"""
		for i in range(0, self.literal_count):
			if self.literals[i] == -1:
				return False
		return True

	def CDCL(self):
		"""
		To perform the CDCL algo
		:return: satisfiability status
		"""
		decision_level = 0
		if self.unsatisfied:
			return 'unsatisfied'

		unit_propagate_result = self.unit_propagate(decision_level)
		if unit_propagate_result == 'unsatisfied':
			del decision_level
			return unit_propagate_result

		while not self.check_all_assigned():
			picked_variable = self.pick_branching_choice()
			self.previous_var = picked_variable
			self.count += 1
			decision_level += 1
			self.assign_var(picked_variable, decision_level, -1)

			while True:
				unit_propagate_result = self.unit_propagate(decision_level)
				if unit_propagate_result == 'unsatisfied':
					if decision_level == 0:
						return unit_propagate_result

					decision_level = self.learn_conflict_backtrack(decision_level)
				else:
					break
			del picked_variable
		del decision_level, unit_propagate_result
		return 'satisfied'

	def solve(self):
		"""
		solve problem and display result
		:return: void
		"""
		result_status = self.CDCL()
		if result_status == 'satisfied':
			print("SAT")
			for i in range(len(self.literals)):
				if self.literals[i] == -1:
					print(i+1, ":0 or 1")
				elif self.literals[i] == 0:
					print((i+1), ":", 0)
				else:
					print(i+1, ":", 1)
		else:
			print("UNSAT")

	def solve_test(self):
		"""
		Returns result status of CDCL solving
		:return: sat status
		"""
		return self.CDCL()

	def get_num_pick_branch(self):
		"""
		:return: number of pick-branching calls
		"""
		return self.count
