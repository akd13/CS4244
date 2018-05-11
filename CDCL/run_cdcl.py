from CDCL.cdcl_routine import add_arguments
import argparse


def parse_input():
	"""
	Get the input file with clauses in DIMACS format.
	:return: generated clause
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('file')
	parser.add_argument('pick_branching', choices=['random', 'random_frequency', '2-clause', 'DLIS', 'VSIDS_nodecay', 'VSIDS'])
	return parser.parse_args().file, parser.parse_args().pick_branching

if __name__ == '__main__':
	filename, heuristic = parse_input()
	solver = add_arguments(filename, heuristic)
	solver.solve()
