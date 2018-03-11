#Source: http://www.dis.uniroma1.it/~liberato/ar/dpll/dpll.html, https://en.wikipedia.org/wiki/DPLL_algorithm

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

def parse_input(): #open input file from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    return parser.parse_args().file

def add_clauses(filename):
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
            size =  len(raw_clause)
            if (raw_clause[size-1]=='0'):
                raw_clause.pop()

            clause = [int(numeric_string) for numeric_string in raw_clause]
            clauses.append(clause)
    return clauses,max_literal

def get_shortest_clause(clause_set):
    shortest_clause = clause_set[0]
    for clause in clause_set:  # choose a variable by shortest remaining
        if (len(shortest_clause) > len(clause)):
            shortest_clause = clause
    return shortest_clause

def unit_propagation(clause, clause_set, literal_values, index_clause):

    pure_literal = clause[0]
    if (pure_literal > 0): #if positive
        literal_values[pure_literal] = 1
    else: #if negative
        literal_values[-1 * pure_literal] = 0
    clause_set.pop(index_clause) #remove clause containing the pure literal

    index = 0
    while (index != len(clause_set)):
        is_solved = False

        for lit in clause_set[index]:
            if (lit == pure_literal):
                is_solved = True
                clause_set.pop(index) #remove the clause (which is now true by default due to pure-literal) from F
                index -= 1
            elif (lit == (-1 * pure_literal)):
                clause_set[index].remove(lit) #remove the pure-literal's negation from a clause
        index += 1

def backtrack_firstbranch(first_element, literal_values, temp_clauseset):
    index = 0
    while (index != len(temp_clauseset)):
        does_literal_appear = False
        for lit in temp_clauseset[index]:
            if (lit == first_element):
                does_literal_appear = True
                break
            elif (lit == (-1 * first_element)):
                temp_clauseset[index].remove(lit) #remove negative literal from clause
        if (does_literal_appear):
            temp_clauseset.pop(index) #remove the clauses where literal appears as this clause is now true by default
            index = index - 1
        index = index + 1

    solve_recursive = DPLL(temp_clauseset, literal_values)

    return solve_recursive

def backtrack_secondbranch(clause_set,first_element):
    first_element = -1 * first_element
    temp_clauseset = clause_set
    index = 0
    while (index != len(temp_clauseset)):
        does_literal_appear = False
        for lit in temp_clauseset[index]:
            if (lit == first_element):
                does_literal_appear = True
                break
            elif (lit == (-1 * first_element)):
                temp_clauseset[index].remove(lit)
        if (does_literal_appear):
            temp_clauseset.pop(index)
            index = index - 1
        index = index + 1
    if (first_element) < 0:
        literal_values[-1 * first_element] = 0
    else:
        literal_values[first_element] = 1
    return temp_clauseset

def DPLL(clause_set, literal_values):

    if (not(clause_set)): # set of clauses are empty
        return True

    for clause in clause_set:
        if (not(clause)):  # if there is an empty clause
            return False

    for clause in clause_set:  # unit prop on unit clause
        index = 0
        if (len(clause) == 1):
            unit_propagation(clause, clause_set, literal_values, index)
            return DPLL(clause_set, literal_values)

    shortest_clause = get_shortest_clause(clause_set)
    first_element = shortest_clause[0]
    temp_clauseset = clause_set
    temp_clauseset.remove(shortest_clause)

    #assign first literal from shortest clause a value and check satisfiability
    first_branch = backtrack_firstbranch(first_element, literal_values, temp_clauseset)

    if (first_branch == True):
        if (first_element) < 0:
            literal_values[-1 * first_element] = 0 #assign it negative value
        else:
            literal_values[first_element] = 1 #assign it positive value
        return first_branch #satisfiable woohoo so stop here

    else:

        temp_clauseset = backtrack_secondbranch(clause_set,first_element)
    return DPLL(temp_clauseset) #check second branch's satisfiability

def assign_remaining_literal(literal_values):
    for i in range(max_value):
        if (i + 1) not in literal_values:
            literal_values[i + 1] = '0 or 1'
    literal_values = OrderedDict(sorted(literal_values.items()))
    return literal_values


clauses = list()
literal_values = dict()

clauses,max_value = add_clauses(parse_input())

can_solve = DPLL(clauses, literal_values)

literal_values = assign_remaining_literal(literal_values)

if (can_solve):
    for s in literal_values:
        print(s,":",literal_values[s])
else:
    print("UNSATISFIABLE!")

