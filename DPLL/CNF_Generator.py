import os
import datetime
import random

num_lits = 3


def generate_clause(N, num_lits):
	clause = []
	count = 0
	while count < num_lits:
		# Randomly general variable
		variable = random.randint(1, N)

		# Randomly negate literal value
		variable_literal = (2 * variable * random.randint(-1, 0) + variable)

		if variable_literal not in clause and -variable_literal not in clause:
			clause.append(variable_literal)
			count += 1

	return clause


def generate_cnf(N, L, num):
	"""
		Generates CNF formulas and store them in DIMACs format in specified file path
		Input: N number of variables, L number of clauses to be produced
		:return: void
	"""
	# Check and create file directory if file path do not exist
	directory = "../sample_cnf/"
	try:
		os.stat(directory)
	except:
		os.mkdir(directory)

	# Use current time as filename
	# filename = datetime.datetime.now().strftime("%B_%d_%Y_%I_%M_%p")
	filename = str(num)

	with open(directory + filename + ".cnf", "w") as file:
		file.write("c filename\n")
		file.write("p cnf {0} {1}\n".format(N, L))

		# Create L number of clauses
		for clause_num in range(L):
			clause = generate_clause(N, num_lits)
			for lit in clause:
				file.write(str(lit) + " ")
			file.write("0\n")


for i in range(50):
	generate_cnf(100, 150, i)
