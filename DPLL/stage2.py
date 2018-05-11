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
	parser.add_argument('clause_list_file')
	parser.add_argument('K', default=3)
	parser.add_argument('R', default=1)
	return parser.parse_args().outfile, \
		   parser.parse_args().clause_list_file, \
		   int(parser.parse_args().K), \
		   int(parser.parse_args().R)


def check_negation(combi):
	original_length = len(combi)
	if original_length != len(list(set(map(abs, combi)))):
		del original_length, combi
		gc.collect()
		return False
	del original_length, combi
	gc.collect()
	return True

filename, clause_file, K, R = parse_input()
num_clauses_required = N * R

literals = []
for i in range(-N, N+1):
	literals.append(i)
literals.remove(0)
print(literals)

all_clauses = []
if not os.path.isfile(clause_file):
	print("Clause File does not Exist")
	for combination in combinations(literals, K):
		all_clauses.append(list(combination))
		del combination
	with open(clause_file, 'wb') as f:
		pickle.dump(all_clauses, f)
	print("All clauses file created")
else:
	print("Clause File Exists")
	with open(clause_file, 'rb') as f:
		all_clauses = pickle.load(f)

total_number_clauses = len(all_clauses)
print(len(all_clauses))


with open(filename, "w") as file:
	file.write("c {0}\n".format(filename))
	file.write("p cnf N:{0}  K:{1}  R:{2}  Number of Clauses{3}:\n".format(150, K, R, num_clauses_required))
	random_set = set()
	count = 0
	while count < num_clauses_required:
		random_int = random.randint(0, total_number_clauses-1)
		if random_int not in random_set:
			random_set.add(random_int)
			picked_clause = all_clauses(random_int)
			if check_negation(picked_clause):
				file.write(' '.join(str(elem) for elem in all_clauses[random_int]) + " ")
				file.write("0\n")
		del random_int, picked_clause
print("Done")
