CDCL
====

SAT Solver in Python.

This submission contains the following files/folders inside the CDCL folder:

cdcl_routine.py
CNF_generator.py
run_cdcl.py
testing.py

sample_cnf contains 9 CNF files and our encoding for Einstein's puzzle (along with the original C code)

Usage instructions:

CNF_generator.py : python CNF_generator.py , then enter the number of variables and clauses
run_cdcl.py : python run_cdcl.py 'filename' 'heuristic' , heuristics = ['random', 'random_frequency', '2-clause', 'DLIS', 'VSIDS_nodecay', 'VSIDS']
testing.py : python testing.py






