import random
from itertools import filterfalse

# Enum of exit states
RetVal = {'satisfied': 0, 'unsatisfied': 1, 'unresolved': 2}


class SATSolverCDCL:
	def __init__(self):
		self.literals = []
		self.literal_list_per_clause = [[]]
		self.literal_frequency = []
		self.literal_polarity = []
		self.original_literal_frequency = []
		self.literal_count = 0
		self.clause_count = 0
		self.kappa_antecedent = -1
		self.literal_decision_level = []
		self.literal_antecedent = []
		self.assigned_literal_count = 0
		self.already_unsatisfied = False
		self.pick_counter = 0

	def unit_propagate(self, decision_level):
		unit_clause_found = False
		false_count = 0
		unset_count = 0
		literal_index = None
		satisfied_flag = False
		last_unset_literal = -1

		do_while = True
		while do_while:
			unit_clause_found = False
			for i, lit_list in enumerate(self.literal_list_per_clause):
				false_count = 0
				unset_count = 0

				for j, lit in enumerate(lit_list):
					literal_index = self.literal_to_variable_index(lit)
					if self.literals[literal_index] == -1:
						unset_count += 1
						last_unset_literal = j
					elif (self.literals[literal_index] == 0 and self.literal_list_per_clause[i][j] > 0) or (self.literals[literal_index] == 1 and self.literal_list_per_clause[i][j] < 0):
						false_count += 1
					else:
						satisfied_flag = True
						break

				if satisfied_flag:
					continue

				if unset_count == 1:
					self.assigned_literal(self.literal_list_per_clause[i][last_unset_literal], decision_level, i)
					unit_clause_found = True
					break
				elif false_count == len(self.literal_list_per_clause[i]):
					self.kappa_antecedent = i
					return RetVal['unsatisfied']

			if unit_clause_found is False:
				do_while = False
		self.kappa_antecedent = -1
		return RetVal['unresolved']

	def assign_literal(self, variable, decision_level, antecedent):
		literal = self.literal_to_variable_index(variable)
		value = 1 if variable > 0 else 0
		self.literals[literal] = value
		self.literal_decision_level[literal] = decision_level
		self.literal_antecedent[literal] = antecedent
		self.literal_frequency[literal] = -1
		self.assigned_literal_count += 1

	def unassign_literal(self, literal_index):
		self.literals[literal_index] = -1
		self.literal_decision_level[literal_index] = -1
		self.literal_antecedent[literal_index] = -1
		self.literal_frequency[literal_index] = self.original_literal_frequency[literal_index]
		self.assigned_literal_count -= 1

	def literal_to_variable_index(self, variable):
		print("Lit to Var")
		if variable > 0:
			return variable - 1
		else:
			return -variable - 1

	def conflict_analysis_and_backtrack(self, decision_level):
		print("perform conflict analysis and backtrack")
		learnt_clause = self.literal_list_per_clause[self.kappa_antecedent]
		conflict_decision_level = decision_level
		this_level_count = 0
		resolver_literal = None
		literal = None

		# TODO: Current implementation is not do while loop
		while True:
			this_level_count = 0
			for clause in learnt_clause:
				literal = self.literal_to_variable_index(clause)
				if self.literal_decision_level[literal] == conflict_decision_level:
					this_level_count += 1

				if self.literal_decision_level[literal] == conflict_decision_level and self.literal_antecedent[literal] != 1:
					resolver_literal = literal

			if this_level_count == 1:
				break

			learnt_clause = self.resolve(learnt_clause, resolver_literal)

		self.literal_list_per_clause.append(learnt_clause)

		for lit in learnt_clause:
			literal_index = self.literal_to_variable_index(lit)
			update = 1 if lit > 0 else -1
			self.literal_polarity[literal_index] += update
			if self.literal_frequency[literal_index] != -1:
				self.literal_frequency[literal_index] += 1
			self.original_literal_frequency[literal_index] += 1

		self.clause_count += 1
		backtracked_decision_level = 0
		for lit in learnt_clause:
			literal_index = self.literal_to_variable_index(lit)
			decision_level_here = self.literal_decision_level[literal_index]
			if decision_level_here != conflict_decision_level and decision_level_here > backtracked_decision_level:
				backtracked_decision_level = decision_level_here

		for i, lit in enumerate(self.literals):
			if self.literal_decision_level[i] > backtracked_decision_level:
				self.unassign_literal(i)

		return backtracked_decision_level

	def resolve(self, input_clause, literal):
		second_input = self.literal_list_per_clause[self.literal_antecedent[literal]]
		input_clause += second_input
		input_clause[:] = filterfalse(lambda x: x == literal + 1 or x == -literal - 1)
		return list(set(input_clause))

	def pick_branching_variable(self):
		print("Get next free assignment")
		random_value = random.randint(1, 10)
		too_many_attempts = False
		attempt_counter = 0
		do_while = True

		while do_while:
			if random_value > 4 or self.assigned_literal_count < self.literal_count or too_many_attempts:
				self.pick_counter += 1
				if self.pick_counter == 20 * self.literal_count:
					for i in range(len(self.literals)):
						self.original_literal_frequency[i] /= 2
						if self.literal_frequency[i] != -1:
							self.literal_frequency[i] /= 2
					self.pick_counter = 0

				variable = self.literal_frequency.index(max(self.literal_frequency))
				if self.literal_polarity[variable] >= 0:
					return variable + 1
				return -variable - 1
			else:
				while attempt_counter < 10 * self.literal_count:
					variable = random.randint(0, self.literal_count - 1)
					if self.literal_frequency[variable] != -1:
						if self.literal_polarity[variable] >= 0:
							return variable + 1
						return -variable - 1
					attempt_counter += 1
				too_many_attempts = True

			if too_many_attempts is False:
				do_while = False

	def all_variable_assigned(self):
		return self.literal_count == self.assigned_literal_count

	def show_result(self, result_status):
		print("Displaying result of solver")
		if result_status == RetVal['satisfied']:
			print("SAT")
			for i, lit in enumerate(self.literals):
				if lit != -1:
					print(pow(-1, (lit + 1) * i + 1))
				else:
					print(i + 1)

		else:
			print("UNSAT")

	def initialize(self):
		"""
		To Initialize the solver
		:return: void
		"""
		# TODO

	def CDCL(self):
		"""
		To perform the CDCL algo
		:return: result state (int)
		"""
		decision_level = 0
		if self.already_unsatisfied:
			return RetVal['unsatisfied']

		unit_propagate_result = self.unit_propagate(decision_level)
		if unit_propagate_result == RetVal['unsatisfied']:
			return unit_propagate_result

		while not self.all_variable_assigned():
			picked_variable =self.pick_branching_variable()
			decision_level += 1
			self.assigned_literal(picked_variable, decision_level, -1)

			while True:
				unit_propagate_result = self.unit_propagate(decision_level)
				if unit_propagate_result == RetVal['unsatisfied']:
					if decision_level == 0:
						return unit_propagate_result
					decision_level = self.conflict_analysis_and_backtrack(decision_level)
				else:
					break
		return RetVal['satisfied']

	def solve(self):
		"""
		solve problem and display result
		:return: void
		"""
		result_status = self.CDCL()
		self.show_result(result_status)
