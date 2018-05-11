from DPLL.cdcl import SATSolverCDCL
from DPLL.stage2_generator import gen_cnf
import numpy as np
import gc
import pycosat

N = 150
R = np.arange(0.2, 10.2, 0.2)
K = [3, 4, 5]

for k in K:
	for r in R:
		print("K:{0}     R:{1}".format(k, r))
		num_total = 0
		num_sat = 0

		# Generate 50 formulas
		for i in range(50):
			cnf = gen_cnf(N, k, r)
			result = pycosat.solve(cnf)
			num_total += 1
			if result != 'UNSAT':
				num_sat += 1
		print("Stats: {0}".format(num_sat/num_total))

print(gen_cnf(N, 0.2, 3))
