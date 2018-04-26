from DPLL.cdcl_donald import add_clauses
from DPLL import cdcl_donald
import random
import argparse
import re
from itertools import filterfalse,repeat
import time
import random


def parse_input():
	"""
	Get the input file with clauses in DIMACS format.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('file')
	return parser.parse_args().file

solver = add_clauses(parse_input())
start = time.clock()
solver.solve()
end = time.clock()
print("Num times pick-branching", solver.get_num_pick_branch())
print("Time taken is", end-start)
