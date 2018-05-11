import argparse
from itertools import combinations
import os.path
import pickle
import random
import gc

N = 150


def parse_input():
	"""
	Get the input file with clauses in DIMACS format.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('outfile')
	parser.add_argument('K', default=3)
	parser.add_argument('R', default=1)
	return parser.parse_args().outfile, \
		   int(parser.parse_args().K), \
		   int(parser.parse_args().R)


def generate_clause(num_variables, num_lits):
	"""
	Generate clauses with number of variables and K.
	:return: generated clause
	"""
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
	"""
	Check if a clause contains a literal with its own negation
	:return: Boolean
	"""
	original_length = len(combi)
	if original_length != len(set(map(abs, combi))):
		del original_length, combi
		gc.collect()
		return False
	del original_length, combi
	gc.collect()
	return True

if __name__ == '__main__':

	filename, K, R = parse_input()
	num_clauses_required = N * R

	literals = []
	for i in range(-N, N+1):
		literals.append(i)
	literals.remove(0)
	print(literals)

	with open(filename, "w") as file:
		file.write("c {0}\n".format(filename))
		file.write("p cnf N:{0}  K:{1}  R:{2}  Number of Clauses{3}:\n".format(150, K, R, num_clauses_required))
		cnf = set()
		while len(cnf) < num_clauses_required:
			new_clause = generate_clause(N, K)
			if check_negation(new_clause):
				cnf.add(new_clause)

		for clause in cnf:
			file.write(' '.join(str(elem) for elem in clause) + " ")
			file.write("0\n")
	print("Done")
