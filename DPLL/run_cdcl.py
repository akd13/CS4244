from DPLL.cdcl import add_arguments
import argparse
import time

def parse_input():
	"""
	Get the input file with clauses in DIMACS format.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('file')
	parser.add_argument('pick_branching',choices = ['random', 'random_frequency', '2-clause', 'DLIS','VSIDS'], default = 'DLIS')
	return parser.parse_args().file, parser.parse_args().pick_branching

filename, heuristic = parse_input()
solver = add_arguments(filename,heuristic)
start = time.clock()
solver.solve()
end = time.clock()
print("Num times pick-branching", solver.get_num_pick_branch())
print("Time taken is", end-start)
