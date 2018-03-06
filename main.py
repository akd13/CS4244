import argparse
import sys
from sat_solver import solve


# Reading and parsing .cnf file line by line
# Returns list of clauses
def read_file(filename):
	cnf = []
	try:
		with open(filename, 'r') as f:
			for line in f:
				tokens = line.split()
				if tokens[0] not in ("p", "c"):
					clause = []
					for token in tokens:
						literal = int(token)
						if literal == 0:
							break
						else:
							clause.append(literal)
					cnf.append(clause)
		return cnf
	except Exception:
		print('Error: Could not open file "{0}"'.format(filename))
		sys.exit(0)


# Main solver
def main(filename):
	print("Running")
	# Reading .cnf file
	cnf = read_file(filename)
	print(cnf)

	# Run DPLL algorithm
	return solve(cnf)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Filename input")
	parser.add_argument('name', help='Input your cnf filename here.')
	args = parser.parse_args()

	main(args.name)

