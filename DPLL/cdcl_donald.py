import random
import argparse
import re
from itertools import filterfalse
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

array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 59, 39, -39, 59, 20, -39, -59, 19, -20, -19, 32, -19, -47, -48, -49, -57, -50, -51, -52, -53, -54, -56, -17, -55, -39, -56, -55, -55, -18, 23, -55, -55, 55, -56, -56, -55, -14, 24, 21, -14, 56, -14, -55, -56, -58, -14, 13, 13, -14, 17, 60, 15, -26, 56, -55, -52, -56, -14, 25, -15, 60, -12, 13, -54, 14, 13, 40, -14, 56, 14, -12, 13, -14, -15, -12, -12, -56, 14, 17, -53, 60, -52, 58, 40, -52, 18, 40, 25, -14, -17, 55, 56, 14, -26, 11, -12, 11, 52, 60, 11, -52, -12, -39, -12, 14, -39, 14, 11, 56, -56, 11, 52, 56, -56, -54, 55, -26, -28, 14, -14, -28, 14, -14, 14, 55, -14, 14, 54, 25, 55, -14, 57, 11, 56, 57, 11, -53, -14, -53, -22, 55, -14, 57, 11, 60, -51, -22, 13, 55, -51, 60, 55, 40, -15, -16, 57, 11, 22, -17, -56, 55, -14, 54, 40, 13, 57, 11, -50, 56, -28, 10, 57, 11, 40, -29, 11, -17, 57, 11, -12, -28, 59, 10, 57, 59, 57, 11, -28, 56, 54, 54, -56, 54, -49, -50, 11, 11, -14, 57, 11, 25, 54, 11, -24, 11, 56, 16, 40, 57, -51, 59, 27, 11, 27, 57, -29, 57, -11, -54, -28, 54, -11, 60, -28, -55, -14, 57, -11, 56, -28, -50, -54, 9, -54, 9, 56, -28, 56, -49, -54, 10, 56, -54, 9, -11, -28, -11, 9, 57, -28, -54, -28, -14, -11, 57, 56, 40, 54, -50, 57, -28, -54, -28, 57, -11, 54, -11, -28, -55, -14, 57, -11, -28, 56, -54, 9, -30, 13, 10, 59, 10, -39, -51, 13, -8, 56, 59, 27, -54, -53, 10, -8, 56, -54, 54, -28, -56, -54, 54, 56, -54, 9, -30, 10, 56, -54, 11, -28, -56, 54, -54, -56, 54, -56, -54, 57, -11, -56, 54, -54, -28, 56, 54, -54, -56, 54, -30, -11, -56, 54, -54, -28, 56, 54, -54, -14, 57, -11, -56, 54, -54, -28, 56, 54, -54, 11, -28, -56, 54, -54, 56, 54, 57, 11, -28, -56, -54, 54, -56, -54, 54, -11, 56, -54, 54, -28, -56, -54, 54, -55, 19, -14, 57, -11, -28, 56, -54, 9, 10, 34, -55, 19, -14, 57, -11, -28, 56, -54, 60, 9, 10, 40, -7, -6, 13, -47, 10, 13, 52, -8, -45, 56, -54, 10, -7, 32, 13, -12, -48, 13, 52, -47, 60, -45, 56, -54, 9, 56, -54, -11, -56, 54, 57, -11, -56, -54, -30, -11, 14, 57, 11, -56, -54, 11, 57, 11, -11, 19, -14, 57, 11, -11, 57, 11, -11, -14, 57, 11, -11, 57, 11, -11, 55, 19, -14, -57, 11, -56, 54, 9, -7, 34, 10, 32, -8, 34, 10, 13, 52, -45, 34, 10, 13, 52, -8, -45, -56, 54, 34, -45, 10, -7, -7, 54, -28, -56, -54, 9, -11, -56, -54, 57, -11, 56, 54, -30, -11, 14, -57, -11, 11, 57, -11, 11, 19, 14, -57, -11, 11, 57, -11, 11, 14, -57, -11, 11, 57, -11, -55, 19, 14, -57, 11, 56, 5, 14, -57, 11, 56, 54, 9, 37, -55, 19, 14, -57, 11, 56, -5, 54, 9, 34, -42, -43, -53, -7, -42, -43, 54, -30, 56, 9, 54, -42, -43, -28, 56, 5, 56, 9, 54, 34, 11, 57, -11, 11, -14, -57, -11, 11, 57, -11, 19, 14, -57, 11, -11, 57, 11, -11, -14, -57, 11, -11, 57, 11, -11, 56, 9, -55, 19, 14, -57, -11, -28, 56, 5, 9, 54, -42, -43, 9, 54, -43, 56, 9, 54, -42, -43, 54, -43, 56, 5, -14, 57, 11, 56, 9, 56, 54, -11, -56, -54, -57, -56, 54, -30, -11, 14, -57, -11, -56, 5, -11, -56, 5, 57, -11, -56, 5, -56, 5, 19, 14, 57, -11, -56, 5, -11, -56, 5, 14, -57, -11, 11, 14, -57, -11, 5, -56, 9, -11, 57, -11, 11, 55, 19, 14, -57, -11, -28, -41, 5, -56, 9, 54, -42, -26, -43, -47, -49, 52, -7, -45, 59, -39, -56, 9, 54, -43, -56, 9, 54, -42, 54, -43, 5, -56, 9, 54, -42, -43, -56, 9, 54, -43, -56, 9, 54, -42, -43, 54, -43, -41, 5, -56, 9, -56, 54, 34, 5, -56, 9, 11, 57, 11, 11, 14, -57, -11, -41, 5, -56, 9, 5, -56, 9, -11, 57, -11, -11, 19, -14, -57, -11, -41, 5, 5, -11, 57, -11, -41, 5, 5, -11, -41, 5, 5, 14, -57, -11, -41, -5, 5, -11, -41, -5, -57, -41, -11]

value_count = 0

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
		unit_clause_found = False
		false_count = 0
		unset_count = 0
		literal_index = None
		satisfied_flag = False
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
					return RetVal['unsatisfied']

			if unit_clause_found is False:
				break


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
		if variable > 0:
			return variable - 1
		else:
			return -variable - 1

	def conflict_analysis_and_backtrack(self, decision_level):
		learnt_clause = self.literal_list_per_clause[self.kappa_antecedent]
		conflict_decision_level = decision_level
		this_level_count = 0
		resolver_literal = None
		literal = None

		# TODO: Current implementation is not do while loop
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

		return backtracked_decision_level

	def resolve(self, input_clause, literal):
		second_input = self.literal_list_per_clause[self.literal_antecedent[literal]]
		new_clause = input_clause + second_input
		new_clause[:] = filterfalse(lambda x: x == literal + 1 or x == -literal - 1, new_clause)
		return sorted(list(set(new_clause)))

	def pick_branching_variable(self):

		picked_variable = array[0]
		array.pop(0)
		return picked_variable
		# picked_variable = random.randint(0,self.literal_count-1)
		# while(True):
		# 	picked_variable = random.randint(0, self.literal_count-1)
		# 	if(self.literals[picked_variable]==-1):
		# 		if(self.literal_frequency[picked_variable]>0):
		# 			if(self.literal_polarity[picked_variable]>=0):
		# 				picked_variable+=1
		# 			else:
		# 				picked_variable=-picked_variable-1
		# 		break
		#
		# return picked_variable
		# for i in range(len(self.literals)):
		# 	if(self.literals[i]==-1):
		# 		self.pick_counter+=1
		# 		if(self.literal_polarity[i]>0):
		# 			return (i+1)
		# 		else:
		# 			return (-1-i)

		# random_value = random.randint(1, 10)
		# too_many_attempts = False
		# attempt_counter = 0
		#
		# while True:
		# 	if random_value > 4 or self.assigned_literal_count < self.literal_count or too_many_attempts:
		# 		self.pick_counter += 1
		# 		if self.pick_counter == 20 * self.literal_count:
		# 			for i in range(len(self.literals)):
		# 				self.original_literal_frequency[i] /= 2
		# 				if self.literal_frequency[i] != -1:
		# 					self.literal_frequency[i] /= 2
		# 			self.pick_counter = 0
		#
		# 		variable = self.literal_frequency.index(max(self.literal_frequency))
		# 		if self.literal_polarity[variable] >= 0:
		# 			return variable + 1
		# 		return -variable - 1
		# 	else:
		# 		while attempt_counter < 10 * self.literal_count:
		# 			variable = random.randint(0, self.literal_count - 1)
		# 			if self.literal_frequency[variable] != -1:
		# 				if self.literal_polarity[variable] >= 0:
		# 					return variable + 1
		# 				return -variable - 1
		# 			attempt_counter += 1
		# 		too_many_attempts = True
		#
		# 	if too_many_attempts is False:
		# 		break

	def all_variable_assigned(self):
		return self.literal_count == self.assigned_literal_count

	def show_result(self, result_status):
		if result_status == RetVal['satisfied']:
			print("SAT")
			print("Satisfying clauses",cnf)
			for i in range(len(self.literals)):
				if(self.literals[i]==-1):
					print(i+1,"can be 0 or 1")
				elif(self.literals[i]==0):
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
			if(not(clause)):
				self.already_unsatisfied = True
			clause_negated = [-l for l in clause]
			if(clause_negated in cnf):
				self.already_unsatisfied = True


		for i in range(num_variables):
			self.literals.append(-1)
			self.literal_decision_level.append(-1)
			self.literal_antecedent.append(-1)
			self.literal_frequency.append(0)
			self.literal_polarity.append(0)

		for clause in cnf:
			for literal in clause:
				if(literal > 0):
					self.literal_frequency[literal-1]+=1
					self.literal_polarity[literal-1]+=1
				else:
					self.literal_frequency[-literal-1]+=1
					self.literal_polarity[-literal-1]-=1

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
			return unit_propagate_result

		while not self.all_variable_assigned():
			picked_variable = self.pick_branching_variable()
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

print("Time taken is", end-start)