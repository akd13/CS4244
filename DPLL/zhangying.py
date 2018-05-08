import sys
import random
import time

start = time.time()

# Read in the file from input
with open(sys.argv[1]) as f:
	dimacs = f.read()

def enc(a=None):
	a = a or assignment
	return "".join("_10"[v] for v in a)

# filter the read-in file (input) based on dimacs formatting
stream = list(filter(None, ("  ".join(line for line in dimacs.split("\n") if line[:2] not in ("c", "c "))).split(" ")))
#print(stream)

#assigned the values to variables based on input
p, cnf, num_vars, num_clauses = stream[:4]
stream = stream[4:]
num_vars = int(num_vars)
num_clauses = int(num_clauses)
init_clauses = []
# print("No. of literals = ", num_vars)
# print("No. of clause = ", num_clauses)
#store the clauses into init_clauses
for ci in range(num_clauses):
	cl = []
	init_clauses.append(cl)
	while stream:
		v = stream.pop(0)
		v = int(v)
		if v == 0:
			break
		cl.append(v)

# print("Check init_clauses : ", init_clauses)
# Stores the value assigned to the literals, where 0=not assigned, 1=True, -1=False
assignment = [0] * num_vars

#returns the value of the literal in the assignment[]
def eval_literal(literal):
	# print("eval_literal(), literal = ", literal)
	# print("assignment[] = ", assignment)
	if literal > 0:
		# print("eval_literal() literal > 0 :", assignment[literal - 1])
		return assignment[literal - 1]
	else:
		# print("eval_literal() literal <=0 :", -assignment[-1 - literal])
		return -assignment[-1 - literal]

#Check if the clause evaluates to True (if maximum is 1)
def eval_clause(clause):
	maximum = max(eval_literal(literal) for literal in clause)
	# print("eval_clause :  maximum = ", maximum)
	return maximum

#Checks if the clauses evaluates to True (if min is 1)
def eval_all():
	return min(eval_clause(clause) for clause in clauses)


# stores the occurrence of the positive variable at which clause#
rp = {i: [] for i in range(num_vars)}
# stores the occurrence of the negative variable at which clause#
rn = {i: [] for i in range(num_vars)}
clauses = []
clause_ok = []
clause_unk = []
reason = {}

clauses_set = set()

#Adds input parameter clause to various arrays for further processing in the later stage
def add_clause(clause, doprint=True):
	fc = frozenset(clause)
	if fc in clauses_set:
		return
	clauses_set.add(fc)

	i = len(clauses)
	# print("Clauses = ", clauses)
	# if doprint: print(enc(), "         adding clause", i, clause)
	clauses.append(clause)
	for var in clause:
		if var > 0:
			rp[var-1].append(i)  # positive variables. eg 1 goes to index 0
		else:
			rn[-1-var].append(i)  # negative variables. eg -1 goes to index 0, -2 goes to index 1...etc
	# print("clause = ", clause)
	ev = [eval_literal(v) for v in clause]
	# print("add_clause(): ev = ", ev)
	# print("Before : clause_ok", clause_ok)
	clause_ok.append(sum(n == 1 for n in ev))
	# print("After : clause_ok", clause_ok)
	# print("Before : clause_unk", clause_unk)
	clause_unk.append(sum(n == 0 for n in ev))
	# print("After : clause_unk", clause_unk)

for clause in init_clauses:
	add_clause(clause)

# print("rp=", rp)
# print("rn=", rn)

def search():
	assert 0 in assignment
	# print("assignment value : ", assignment)

	i = assignment.index(0)  # gets lowest index in the assignment[] that contains '0'
	# print(enc(), "attempting both values for", i)
	# print("search(i, -1) i = ", i)
	# Attempt to assign as false
	yield from propagate(i, -1)
	# print("search(i, 1) i = ", i)
	# Attempt to assign as true
	yield from propagate(i,  1)

def propagate(i, v):
	# print("propagate(i, v) i = ", i, ", v = ", v)
	yield from propagate2([(i, v, None)])

def propagate2(assigns):
	# print("propagate2(assigns) assigns = ", assigns)
	found = False
	while assigns:
		i, v, r = assigns[0]
		assigns = assigns[1:]
		# print("WhileLOop: Assigns = ", assigns)
		if assignment[i] != v:
			found = True
			# print("FOUND ", found)
			break

	if not found:
		if 0 in assignment:
			yield from search()
		else:
			if eval_all() == 1:
				yield assignment[:]

	elif assignment[i] == -v:
		# print("elif assignment[", i, "] == -v: reason[i] = ", reason[i])
		both = reason[i] | r  # binary OR operation
		# print("both List =",list(both))
		add_clause(list(both))

	else:

		ok = [None, rp, rn][v][i]
		ng = [None, rn, rp][v][i]
		# print("Check ok = ", ok)
		# print("Check ng = ", ng)
		# DO
		assignment[i] = v
		# Set the decision reason for assigning the literal as v becuz of r
		reason[i] = r
		# print("else: reason[", i, "] = ", reason[i])
		# print("assignment[", i, "] = ", assignment[i])
		# print(enc(), "assigning", i, v, "ok=", ok, "ng=", ng)
		for ci in ok:
			clause_ok[ci] += 1
			clause_unk[ci] -= 1
		for ci in ng:
			clause_unk[ci] -= 1

		# CHECK
		contradiction = False
		# print("ok+ng = ", ok+ng)
		for ci in ok+ng:

			if clause_ok[ci] == 0:
				if clause_unk[ci] == 0:
					assert eval_clause(clauses[ci]) == -1
					# print(enc(), "clause", ci, "has become unsatisfiable")
					contradiction = True
					break

				elif clause_unk[ci] == 1:
					z = {j for j in clauses[ci] if assignment[abs(j)-1] == 0}
					assert len(z) == 1, (ci, clauses[ci], assignment, z,
						[(abs(j)-1, assignment[abs(j)-1]) for j in clauses[ci]])
					z, = z  # unpack z
					# print("clauses[ci] : ", clauses[ci])
					r = set(clauses[ci])
					# print("discard z = ", z)
					r.discard(z)
					if z > 0:
						l = (z-1, 1, r)
					else:
						l = (-1-z, -1, r)

					for pi, pv, pr in assigns:
						if pi == l[0] and pv != l[1]:
							both = pr | r
							# print("Both = ", both)
							# 0.0 very CDCL
							# 1.0 not very CDCL
							if random.random() > 0.0:
								add_clause(list(both), doprint=False)
							contradiction = True
							break

					assigns.append(l)
					#print(enc(), "assignment", assigns[-1][:2], "was implied")
			if contradiction: break

		if not contradiction:
			yield from propagate2(assigns)

		# UNDO
		ok = [None, rp, rn][v][i]
		ng = [None, rn, rp][v][i]
		assignment[i] = 0
		reason[i] = None
		# print(reason)
		for ci in ok:
			clause_ok[ci] -= 1
			clause_unk[ci] += 1
		for ci in ng:
			clause_unk[ci] += 1

allsols = []
for sol in search():
	print(enc(sol), "==== SAT ====")
	# stop the program once a satisfiable assignment is found
	allsols.append(sol)
	end = time.time()
	print("time taken =", end - start)

for sol in allsols:
	print(enc(sol))

if len(allsols) == 0:
	# if there are no solutions at all in all sols when program ends
	end = time.time()
	print("==== UNSAT ====")
	print("time taken =", end - start)
