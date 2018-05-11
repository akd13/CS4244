from DPLL.stage2_generator import gen_cnf
from Stage2.stage2_generator import gen_cnf
import numpy as np
import gc
import pycosat
import pickle

N = 150
R = np.arange(0.2, 10, 0.2)
K = [3, 4, 5]

file = "stats.csv"

with open(file, 'w') as f:
	f.write("K,R,Prob of Sat")
	for k in K:
		for r in R:
			num_total = 0
			num_sat = 0

			# Generate 50 formulas
			for i in range(50):
				cnf = gen_cnf(N, k, r)
				print("CNF generated")
				result = pycosat.solve(cnf)
				num_total += 1
				if result != 'UNSAT':
					num_sat += 1
			probability = num_sat/num_total
			print("K:{0}     R:{1}".format(k, r), "  Stats: {0}".format(probability))
			f.write('{0},{1},{2}'.format(k, r, probability))
print("Done")
