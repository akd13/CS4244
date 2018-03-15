#Source: http://www.dis.uniroma1.it/~liberato/ar/dpll/dpll.html
# https://en.wikipedia.org/wiki/DPLL_algorithm

# Algorithm DPLL
#   Input: A set of clauses Φ.
#   Output: A Truth Value.
# function DPLL(Φ)
#    if Φ is a consistent set of literals
#        then return true;
#    if Φ contains an empty clause
#        then return false;
#    for every unit clause l in Φ
#       Φ ← unit-propagate(l, Φ);
#    for every literal l that occurs pure in Φ
#       Φ ← pure-literal-assign(l, Φ);
#    l ← choose-literal(Φ);
#    return DPLL(Φ ∧ l) or DPLL(Φ ∧ not(l));

import argparse
import re
import copy
from collections import OrderedDict

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

def get_shortest_clause(clause_set):
    """
    Get the shortest clause from the clause set
    """
    shortest_clause = clause_set[0]
    for clause in clause_set:
        if (len(shortest_clause) > len(clause)):
            shortest_clause = clause
    return shortest_clause

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


def unit_propagation(clause, clause_set, literal_values):
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

    clause_set.remove(clause)  #remove the clause containing the pure literal

    i = 0
    while (i != len(clause_set)):
        for lit in clause_set[i]:
            if (lit == pure_literal):
                clause_set.pop(i) #remove the entire clause (which is now true by default due to pure-literal) from F
                i-= 1
            elif (lit == (-1 * pure_literal)):
                clause_set[i].remove(lit) #remove the assigned literal from a clause
        i+=1

                # for clause in clause_set:
                #     if (not(clause)):  # if there is an empty clause
                #         #add_conflict_clause(literal_values,original_clauses)
                #         #backtrack_decision_level(clause_set, decision_level, conflict_clause)


def backtrack_decision_level(clause_set, decision_level, conflict_clause):
    """
    TODO: Perform back-tracking for CDCL
    """

def add_conflict_clause(literal_values,original_clauses):
    """
    Add conflict clause to the original clause set
    """
    clause_set = original_clauses
    conflict_clause = []
    #decision_level = literal_values.get_decision_level()
    #conflict_values = literal_values.track_cut

    for s in literal_values:
        if(literal_values[s]==1):
            conflict_clause.append(-1*s)
        elif(literal_values[s]==0):
            conflict_clause.append(s)
    clause_set.append(conflict_clause)

    #return conflict_clause
    return DPLL(clause_set,literal_values)

def backtrack_firstbranch(clause_set, literal_values, literal):
    """
    Assign literal a value of 1
    """
    #print("first branch")

    temp_clauseset = clause_set
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

def backtrack_secondbranch(clause_set, literal_values, literal):
    """
    Assign literal a value of 0
    """
    #print("Second branch")

    literal = -1 * literal
    temp_clauseset = clause_set

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

    if (first_element) < 0:
        literal_values[-1 * literal] = 0
    else:
        literal_values[literal] = 1

    solve_recursive = DPLL(temp_clauseset, literal_values)

    return solve_recursive

def DPLL(clause_set, literal_values):

    if (not(clause_set)): # set of clauses is empty, everything is satisfied
        return True

    for clause in clause_set:
        if (not(clause)):  # if there is an empty clause, unsat
            return False

    for clause in clause_set:  #perform unit propagation
        if (len(clause) == 1):
            unit_propagation(clause, clause_set, literal_values)
            return DPLL(clause_set, literal_values)

    shortest_clause = get_shortest_clause(clause_set)
    first_element = shortest_clause[0]

    #assign first literal from shortest clause and check satisfiability

    first_branch = backtrack_firstbranch(clause_set, literal_values, first_element)

    if (first_branch == True): #no need to solve second branch :)
        if (first_element < 0):
            literal_values[-1 * first_element] = 0 #assign it 0
        else:
            literal_values[first_element] = 1 #assign it 1
        return True

    else: #check second branch's satisfiability
        clause_set = backtrack_secondbranch(clause_set,literal_values,first_element)

    return DPLL(clause_set)


clauses = list()
literal_values = dict()

clauses,max_value = add_clauses(parse_input())
can_solve = DPLL(clauses, literal_values)
literal_values = assign_remaining_literal(literal_values)

if (can_solve):
    print("SATISFIABLE! Assignments are given below")
    for s in literal_values:
        print("x"+str(s),":",literal_values[s])
else:
    print("UNSATISFIABLE!")

