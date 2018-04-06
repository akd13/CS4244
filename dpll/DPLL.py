#Source: http://www.dis.uniroma1.it/~liberato/ar/dpll/dpll.html
# https://en.wikipedia.org/wiki/DPLL_algorithm

import argparse
import re
from collections import OrderedDict
import time
num_branches = 0

def parse_input():
    """
    Get the input file with clauses in DIMACS format.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    return parser.parse_args().file

def add_clauses(filename):
    """
    Check validity of each clause and add to clause set
    """
    max_literal = 0
    file = open(filename, "r")
    for line in file:
        comment = re.search('^\s*(p|c).*(\n)*$',line)
        header = re.search('^\s*(p)\s+(cnf)\s+(\d+)\s+(\d+)(\n)*$',line)
        clause_input_cnf = re.search('^\s*((-)*\d+\s*)*(0)(\\n)*$', line) #detect clause

        if(header!=None):
            max_literal = int(line.split()[2])

        if comment == None and clause_input_cnf == None:
            print(line," is invalid!")
            break;

        elif clause_input_cnf != None:
            raw_clause = clause_input_cnf.group(0).split()
            raw_clause.pop()
            clause = [int(numeric_string) for numeric_string in raw_clause]
            clauses.append(clause)
    return clauses,max_literal

####################
## Helper Methods ##
####################

def assign_remaining_literal(literal_values):
    """
    Assign 0 or 1 to literals not assigned in the satisfiable clause
    """
    for i in range(max_value):
        if (i + 1) not in literal_values:
            literal_values[i + 1] = '0 or 1'
    literal_values = OrderedDict(sorted(literal_values.items()))
    return literal_values

##################
## CDCL Methods ##
##################


def unit_propagation(clause, cnf, literal_values):
    """
    Assign unit clause truth value, and for each clause in clause set, do
    1. remove the clauses already satisfied
    2. remove literals already assigned in the clause
    """
    pure_literal = clause[0]

    if (pure_literal > 0): #if positive clause
        literal_values[pure_literal] = 1
    else:                  #if negative clause
        literal_values[-1 * pure_literal] = 0

    cnf.remove(clause)  #remove the clause containing the pure literal

    i = 0
    while (i != len(cnf)):
        for lit in cnf[i]:
            if (lit == pure_literal):
                cnf.pop(i) #remove the entire clause (which is now true by default due to pure-literal) from F
                i-= 1
            elif (lit == (-1 * pure_literal)):
                cnf[i].remove(lit) #remove the assigned literal from a clause
        i+=1

                # for clause in cnf:
                #     if (not(clause)):  # if there is an empty clause
                #         #add_conflict_clause(literal_values,original_clauses)
                #         #backtrack_decision_level(cnf, decision_level, conflict_clause)


def backtrack_decision_level(cnf, decision_level, conflict_clause):
    """
    TODO: Perform back-tracking for CDCL
    """

def add_conflict_clause(literal_values,original_clauses):
    """
    Add conflict clause to the original clause set
    """
    cnf = original_clauses
    conflict_clause = []
    #decision_level = literal_values.get_decision_level()
    #conflict_values = literal_values.track_cut

    for s in literal_values:
        if(literal_values[s]==1):
            conflict_clause.append(-1*s)
        elif(literal_values[s]==0):
            conflict_clause.append(s)
    cnf.append(conflict_clause)

    #return conflict_clause
    return DPLL(cnf,literal_values)

def backtrack_firstbranch(cnf, literal_values, literal):
    """
    Assign literal a value of 1
    """
    #print("first branch")
    global num_branches
    num_branches+=1
    temp_clauseset = cnf
    i = 0
    while (i != len(temp_clauseset)):
        for current_literal in temp_clauseset[i]:
            if (current_literal == literal):
                temp_clauseset.pop(i)
                i-=1
            elif (current_literal == (-1 * literal)):
                temp_clauseset[i].remove(current_literal) #remove negative literal from clause
        i+=1

    solve_recursive = DPLL(temp_clauseset, literal_values)

    return solve_recursive

def backtrack_secondbranch(cnf, literal_values, literal):
    """
    Assign literal a value of 0
    """
    #print("Second branch")

    global num_branches
    num_branches+=1
    literal = -1 * literal
    temp_clauseset = cnf
    i = 0
    while (i != len(temp_clauseset)):
        for current_literal in temp_clauseset[i]:
            if (current_literal == literal):
                temp_clauseset.pop(i)
                i-=1
                break
            elif (current_literal == (-1 * literal)):
                temp_clauseset[i].remove(current_literal)
        i+=1

    if (current_literal < 0):
        literal_values[-1 * literal] = 0
    else:
        literal_values[literal] = 1

    solve_recursive = DPLL(temp_clauseset, literal_values)

    return solve_recursive

def DPLL(cnf, literal_values):

    if (not(cnf)): # set of clauses is empty, everything is satisfied
        return True

    for clause in cnf:
        if (not(clause)):  # if there is an empty clause, unsat
            return False

    for clause in cnf:  #perform unit propagation
        if (len(clause) == 1):
            unit_propagation(clause, cnf, literal_values)
            return DPLL(cnf, literal_values)

    shortest_clause = min(cnf, key=len)
    first_element = shortest_clause[0]

    #assign first literal from shortest clause and check satisfiability

    first_branch = backtrack_firstbranch(cnf, literal_values, first_element)

    if (first_branch == True): #no need to solve second branch :)
        if (first_element < 0):
            literal_values[-1 * first_element] = 0 #assign it 0
        else:
            literal_values[first_element] = 1 #assign it 1
        return True

    else: #check second branch's satisfiability
        cnf = backtrack_secondbranch(cnf,literal_values,first_element)

    return DPLL(cnf,literal_values)


clauses = list()
literal_values = dict()

clauses,max_value = add_clauses(parse_input())
time_start = time.time()
can_solve = DPLL(clauses, literal_values)
time_end = time.time()
literal_values = assign_remaining_literal(literal_values)

if (can_solve):
    print("SATISFIABLE! Assignments are given below-")
    for s in literal_values:
        print("x"+str(s),":",literal_values[s])
    print("Total time taken is ",time_end-time_start, "seconds")
    print("Total number of branches are", num_branches)
else:
    print("UNSATISFIABLE!")

for i in range(254):
    print('a')