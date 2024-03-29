import unittest
import time
from CDCL.cdcl_routine import add_arguments

heuristic = "DLIS"


class TestStringMethods(unittest.TestCase):
	"""
	Performs unit testing of all the generated CNF files.
	:return: True/False
	"""

	def test_upper(self):
		self.assertEqual('foo'.upper(), 'FOO')

	def test_hoge(self):
		print()
		print("Testing hoge.cnf")
		filename = "sample_cnf/hoge.cnf"
		solver = add_arguments(filename,heuristic)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 'satisfied')
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)

	def test_input(self):
		print()
		print("Testing input.cnf")
		filename = "sample_cnf/input.cnf"
		solver = add_arguments(filename,heuristic)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 'satisfied')
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)

	def test_new(self):
		print()
		print("Generated.cnf")
		filename = "sample_cnf/Generated.cnf"
		solver = add_arguments(filename,heuristic)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 'satisfied')
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)

	def test_unsat_simple(self):
		print()
		print("Testing unsat_simple.cnf")
		filename = "sample_cnf/unsat_simple.cnf"
		solver = add_arguments(filename,heuristic)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 'unsatisfied')
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)

	def test_unsat_complex_1(self):
		print()
		print("Testing unsat_complex_1.cnf")
		filename = "sample_cnf/unsat_complex_1.cnf"
		solver = add_arguments(filename,heuristic)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 'unsatisfied')
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)

	def test_unsat_complex_2(self):
		print()
		print("Testing unsat_complex_2.cnf")
		filename = "sample_cnf/unsat_complex_2.cnf"
		solver = add_arguments(filename,heuristic)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 'unsatisfied')
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)


	def test_einstein(self):
		print()
		print("Testing einstein.cnf")
		filename = "sample_cnf/einstein.cnf"
		solver = add_arguments(filename,heuristic)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 'satisfied')
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)


if __name__ == '__main__':
	unittest.main()
