import random
import gc

N = 150


def generate_clause(num_variables, num_lits):
	clause = set()
	count = 0
	while count < num_lits:
		# Randomly general variable
		variable = random.randint(1, num_variables)

		# Randomly negate literal value
		variable_literal = (2 * variable * random.randint(-1, 0) + variable)

		if variable_literal not in clause and -variable_literal not in clause:
			clause.add(variable_literal)
			count += 1
	return frozenset(clause)


def check_negation(combi):
	original_length = len(combi)
	if original_length != len(set(map(abs, combi))):
		del original_length, combi
		gc.collect()
		return False
	del original_length, combi
	gc.collect()
	return True


def gen_cnf(N, K, R):
	num_clauses_required = int(N*R)
	literals = []
	for i in range(-N, N + 1):
		literals.append(i)
	literals.remove(0)
	cnf = set()
	while len(cnf) < num_clauses_required:
		new_clause = generate_clause(N, K)
		if check_negation(new_clause):
			cnf.add(new_clause)
	return list(map(list, cnf))
