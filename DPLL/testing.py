import unittest
import time
from DPLL.cdcl_donald import add_clauses

class TestStringMethods(unittest.TestCase):

	def test_upper(self):
		self.assertEqual('foo'.upper(), 'FOO')

	# Sat = 0, Unsat = 1

	def test_hoge(self):
		print()
		print("Testing hoge.cnf")
		filename = "../sample_cnf/hoge.cnf"
		solver = add_clauses(filename)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 0)
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)

	def test_input(self):
		print()
		print("Testing input.cnf")
		filename = "../sample_cnf/input.cnf"
		solver = add_clauses(filename)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 0)
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)

	def test_test(self):
		print()
		print("Testing test.cnf")
		filename = "../sample_cnf/test.cnf"
		solver = add_clauses(filename)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 0)
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)

	def test_test1(self):
		print()
		print("Testing test1.cnf")
		filename = "../sample_cnf/test1.cnf"
		solver = add_clauses(filename)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 0)
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)

	def test_unsat(self):
		print()
		print("Testing unsat.cnf")
		filename = "../sample_cnf/unsat.cnf"
		solver = add_clauses(filename)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 1)
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)

	def test_unsat1(self):
		print()
		print("Testing unsat1.cnf")
		filename = "../sample_cnf/unsat1.cnf"
		solver = add_clauses(filename)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 1)
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)

	def test_unsat_complex(self):
		print()
		print("Testing unsat_complex.cnf")
		filename = "../sample_cnf/unsat_complex.cnf"
		solver = add_clauses(filename)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 1)
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)

	def test_unsat_simple(self):
		print()
		print("Testing unsat_simple.cnf")
		filename = "../sample_cnf/unsat_simple.cnf"
		solver = add_clauses(filename)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 1)
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)

	def test_variables(self):
		print()
		print("Testing variable.cnf")
		filename = "../sample_cnf/variables.cnf"
		solver = add_clauses(filename)
		start = time.clock()
		self.assertEqual(solver.solve_test(), 1)
		end = time.clock()
		print("Num times pick-branching", solver.get_num_pick_branch())
		print("Time taken is", end - start)


if __name__ == '__main__':
	unittest.main()
