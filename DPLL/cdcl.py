# CDCL(ϕ, ν)
# 1 if (UnitPropagation(ϕ, ν) == CONFLICT)
# 2 then return UNSAT
# 3 dl ← 0 ✄ Decision level
# 4 while (not AllVariablesAssigned(ϕ, ν))
# 5 do (x, v) = PickBranchingVariable(ϕ, ν) ✄ Decide stage
# 6 dl ← dl + 1 ✄ Increment decision level due to new decision
# 7 ν ← ν ∪ {(x, v)}
# 8 if (UnitPropagation(ϕ, ν) == CONFLICT) ✄ Deduce stage
# 9 then β = ConflictAnalysis(ϕ, ν) ✄ Diagnose stage
# 10 if (β < 0)
# 11 then return UNSAT
# 12 else Backtrack(ϕ, ν, β)
# 13 dl ← β ✄ Decrement decision level due to backtracking
# 14 return SAT

import argparse
import re
from conflict_graph.objects import Clause, Node, Graph

# CNF clauses in clause object form
clause_list = []

# CNF clauses in list form
cnf = []

# Set of unique literals in CNF
set_literals = set()

# Literal Assignments


# Literal assignment based on decision levels
lit_assignments = {}


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
	id_count = 0
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
			clause_list.append(Clause(clause, id_count))
			id_count += 1
			for lit in clause:
				set_literals.add(abs(lit))
			cnf.append(clause)

	return cnf, num_variables


def get_clauses_of_literal(input_cnf, num_variables):
	"""
	Get clauses associated with each literal
	"""

	literal_clause = [[] for _ in range(1, num_variables+2)]

	for clause in input_cnf:
		for i in clause:
			if i > 0:
				literal_clause[i].append(clause)
			else:
				literal_clause[-i].append(clause)

	return literal_clause


def build_graph(current_graph):
	if current_graph is None:
		current_graph = Graph()


cnf, max_value = add_clauses(parse_input())
literals = get_clauses_of_literal(cnf, max_value)

# verify clauses for each literal
for i in range(1,max_value+1):
	print(i, ":", literals[i])

print(sorted(set_literals))

print("\nClause Object Breakdown")
for clause in clause_list:
	print(clause.get_id(), clause.get_literal_list(), clause.lit_exists(30), clause.get_num_assigned())

# Begin graph plotting at decision level 0
decision_level = 0

