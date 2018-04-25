import random
import argparse
import re
from itertools import filterfalse,repeat
import time
import random

# Enum of exit states
RetVal = {'satisfied': 0, 'unsatisfied': 1, 'unresolved': 2}
# CNF clauses in clause object form
clause_list = []

# CNF clauses in list form
cnf = []

# Set of unique literals in CNF
set_literals = set()

# Literal assignment based on decision levels
lit_assignments = {}

pick_branched = []

count = 0


def parse_input():
	"""
	Get the input file with clauses in DIMACS format.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('file')
	return parser.parse_args().file


def add_clauses(filename):
	"""
	Check validity of each clause and add to clause set
	"""
	file = open(filename, "r")
	num_variables = 0

	for line in file:
		comment = re.search('^\s*(p|c).*(\n)*$', line)
		header = re.search('^\s*(p)\s+(cnf)\s+(\d+)\s+(\d+)(\n)*$', line)
		clause_input_cnf = re.search('^\s*((-)*\d+\s*)*(0)(\\n)*$', line)  # detect clause

		if header is not None:
			num_variables = int(line.split()[2])

		if comment is None and clause_input_cnf is None:
			print(line, " is invalid!")
			break

		elif clause_input_cnf is not None:
			raw_clause = clause_input_cnf.group(0).split()
			raw_clause.pop()
			clause = [int(numeric_string) for numeric_string in raw_clause]
			for lit in clause:
				set_literals.add(abs(lit))
			cnf.append(clause)
	solver = SATSolverCDCL()
	solver.initialize(cnf, num_variables)

	del file, filename, num_variables, comment, header, clause_input_cnf, raw_clause

	return solver


class SATSolverCDCL:
	def __init__(self):
		self.literals = []
		self.literal_list_per_clause = []
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
		last_unset_literal = -1

		while True:
			unit_clause_found = False
			for i, lit_list in enumerate(self.literal_list_per_clause):
				false_count = 0
				unset_count = 0
				satisfied_flag = False

				for j, lit in enumerate(lit_list):
					literal_index = self.literal_to_variable_index(lit)
					if self.literals[literal_index] == -1:
						unset_count += 1
						last_unset_literal = j
					elif (self.literals[literal_index] == 0 and lit > 0) or (self.literals[literal_index] == 1 and lit < 0):
						false_count += 1
					else:
						satisfied_flag = True
						break

				if satisfied_flag:
					continue

				if unset_count == 1:
					self.assign_literal(self.literal_list_per_clause[i][last_unset_literal], decision_level, i)
					unit_clause_found = True
					break
				elif false_count == len(self.literal_list_per_clause[i]):
					self.kappa_antecedent = i
					del last_unset_literal, false_count, unset_count, satisfied_flag, literal_index, unit_clause_found
					return RetVal['unsatisfied']

			if unit_clause_found is False:
				break

		self.kappa_antecedent = -1

		del last_unset_literal, false_count, unset_count, satisfied_flag, literal_index, unit_clause_found
		return RetVal['unresolved']

	def assign_literal(self, variable, decision_level, antecedent):
		literal = self.literal_to_variable_index(variable)
		value = 1 if variable > 0 else 0
		self.literals[literal] = value
		self.literal_decision_level[literal] = decision_level
		self.literal_antecedent[literal] = antecedent
		self.literal_frequency[literal] = -1
		self.assigned_literal_count += 1
		del literal, value

	def unassign_literal(self, literal_index):
		self.literals[literal_index] = -1
		self.literal_decision_level[literal_index] = -1
		self.literal_antecedent[literal_index] = -1
		self.literal_frequency[literal_index] = self.original_literal_frequency[literal_index]
		self.assigned_literal_count -= 1

	def literal_to_variable_index(self, variable):
		if variable > 0:
			return variable - 1
		else:
			return -variable - 1

	def conflict_analysis_and_backtrack(self, decision_level):
		learnt_clause = self.literal_list_per_clause[self.kappa_antecedent]
		conflict_decision_level = decision_level
		resolver_literal = None

		while True:
			this_level_count = 0
			for l in learnt_clause:
				literal = self.literal_to_variable_index(l)
				if self.literal_decision_level[literal] == conflict_decision_level:
					this_level_count += 1

				if self.literal_decision_level[literal] == conflict_decision_level and self.literal_antecedent[literal] != -1:
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

		del learnt_clause, conflict_decision_level, resolver_literal, this_level_count, literal, l, lit, update, literal_index, i
		return backtracked_decision_level

	def resolve(self, input_clause, literal):
		second_input = self.literal_list_per_clause[self.literal_antecedent[literal]]
		new_clause = input_clause + second_input
		new_clause[:] = filterfalse(lambda x: x == literal + 1 or x == -literal - 1, new_clause)
		new_clause = sorted(list(set(new_clause)))
		del second_input
		return new_clause

	def pick_branching_variable(self):

		unassigned_list = []
		for i in range(0, self.literal_count):
			if self.literals[i] == -1:
				unassigned_list.append(i)

		choose = random.choice(unassigned_list)
		if self.literal_polarity[choose]>=0:
			return choose+1
		else:
			return -choose-1

	def all_variable_assigned(self):
		for i in range(0,self.literal_count):
			if self.literals[i] == -1:
				return False
		return True

	def show_result(self, result_status):
		if result_status == RetVal['satisfied']:
			print("SAT")
			print("Satisfying clauses",cnf)
			for i in range(len(self.literals)):
				if self.literals[i]==-1:
					print(i+1,"can be 0 or 1")
				elif self.literals[i]==0:
					print((i+1)*-1)
				else:
					print(i+1)

		else:
			print("UNSAT")

	def initialize(self, cnf, num_variables):
		"""
		To Initialize the solver
		:return: void
		"""

		for clause in cnf:
			self.literal_list_per_clause.append(clause)
			if not clause:
				self.already_unsatisfied = True

		for i in range(num_variables):
			self.literals.append(-1)
			self.literal_decision_level.append(-1)
			self.literal_antecedent.append(-1)
			self.literal_frequency.append(0)
			self.literal_polarity.append(0)

		for clause in cnf:
			for literal in clause:
				if literal > 0:
					self.literal_frequency[literal-1] += 1
					self.literal_polarity[literal-1] += 1
				else:
					self.literal_frequency[-literal-1] += 1
					self.literal_polarity[-literal-1] -= 1

		self.original_literal_frequency = self.literal_frequency
		self.literal_count = num_variables
		self.clause_count = len(cnf)

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
			del decision_level, unit_propagate_result
			return unit_propagate_result

		while not self.all_variable_assigned():
			picked_variable = self.pick_branching_variable()
			global count
			count += 1
			decision_level += 1
			self.assign_literal(picked_variable, decision_level, -1)

			while True:
				unit_propagate_result = self.unit_propagate(decision_level)
				if unit_propagate_result == RetVal['unsatisfied']:
					if decision_level == 0:
						return unit_propagate_result

					decision_level = self.conflict_analysis_and_backtrack(decision_level)
				else:
					break
		del decision_level, unit_propagate_result, picked_variable
		return RetVal['satisfied']

	def solve(self):
		"""
		solve problem and display result
		:return: void
		"""
		result_status = self.CDCL()
		self.show_result(result_status)

solver = add_clauses(parse_input())
start = time.clock()
solver.solve()
end = time.clock()
print("Num times", count)
print("Time taken is", end-start)
