"""
if x = 1
	Substitution -> ignore all clauses with x
	unit prop -> after assessing x, if a  clause left a single unknown, assign that unknown to make clause SAT
	pure literal elimination -> assign variable if only X XOR -X
"""


# remove clauses with both var and its negate in same clause e.g(x, -x, y)
def remove_pointless(cnf):
	new_cnf = []
	for clause in cnf:
		new_clause = []
		find = False
		visited = []
		for literal in clause:
			if -literal in visited:
				find = True
				break
			else:
				new_clause.append(literal)
				visited.append(literal)
		if find:
			break
		new_cnf.append(new_clause)
	return new_cnf


# negated literals will return opposite boolean
def negate_literal(x):
	return not x


# takes in cnf and performs resolution to produce new clauses
def resolution(cnf):
	# TODO: Check through clauses to find resolution (if two clause have x and -x each then resolution performed)

	return cnf


# reads literals
def process_cnf(cnf, assigned):
	# TODO: Check for pure literals
	pure_literals = []
	literal_dict = {}
	# for clause in cnf:
	# 	for literal in clause:
	# 		# TODO: read through the clauses and record the literals accordingly


def solve(cnf):
	cnf = remove_pointless(cnf)

	# list of assigned literals (literal, T/F) in order
	assigned = []
	assignment = {}

	literals = process_cnf(cnf, assigned)
