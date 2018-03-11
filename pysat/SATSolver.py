import argparse
import re
import copy
from collections import OrderedDict

def parse_input(): #open input file from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    return parser.parse_args().file

def add_clauses(filename):
    file = open(filename, "r")
    for line in file:
        p = re.search('^\s*(p|c).*(\n)*$',line)
        m = re.search('^\s*((-)*\d+\s*)*(0)(\\n)*$', line) #detect clause
        if p == None and m == None:
            print(line," is invalid!")
            break;
        elif m != None:
            raw_clause = m.group(0).split()
            size =  len(raw_clause)
            if (raw_clause[size-1]=='0'):
                raw_clause.pop()

            clause = [int(numeric_string) for numeric_string in raw_clause]
            clauses.append(clause)
    return clauses

def unit_propagation(clause, clause_set, literal_values, index_clause):


    pure_literal = clause[0]
    if (pure_literal < 0): #if negative
        literal_values[-1 * pure_literal] = 0
    else:
        literal_values[pure_literal] = 1 #if positive
    clause_set.pop(index_clause) #remove clause containing the pure literal

    index = 0
    while (index != len(clause_set)):
        is_solved = False

        for lit in clause_set[index]:
            if (lit == pure_literal):
                is_solved = True
                break
            elif (lit == (-1 * pure_literal)):
                clause_set[index].remove(lit) #remove the pure-literal's negation from a clause

        if (is_solved): #remove the clause (which is now true by default due to pure-literal) from F
            clause_set.pop(index)
            index-=1
        index+=1


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

    shortest_clause = clause_set[0]
    for clause in clause_set:  # choose a variable by shortest remaining
        if len(shortest_clause) > len(clause):
            shortest_clause = clause
    first_element = shortest_clause[0]
    temp_clauseset = clause_set
    temp_clauseset.remove(shortest_clause)

    index = 0
    while (index != len(temp_clauseset)):
        is_solved = False
        for lit in temp_clauseset[index]:
            if lit == first_element:
                is_solved = True
                break
            elif (lit == (-1 * first_element)):
                temp_clauseset[index].remove(lit)
        if is_solved:
            temp_clauseset.pop(index)
            index = index - 1
        index = index + 1
    temp_literal_values = literal_values
    done = DPLL(temp_clauseset, literal_values)

    if done:
        if first_element < 0:
            literal_values[-1 * first_element] = 0
        else:
            literal_values[first_element] = 1
        return done
    else:
        literal_values = temp_literal_values
        first_element = (-1 * first_element)
        temp_clauseset = copy.deepcopy(clause_set)
        index = 0
        while (index != len(temp_clauseset)):
            is_solved = False
            for lit in temp_clauseset[index]:
                if lit == first_element:
                    is_solved = True
                    break
                elif (lit == (-1 * first_element)):
                    temp_clauseset[index].remove(lit)
            if is_solved:
                temp_clauseset.pop(index)
                index = index - 1
            index = index + 1
        if first_element < 0:
            literal_values[-1 * first_element] = 0
        else:
            literal_values[first_element] = 1
    return DPLL(temp_clauseset)

clauses = []
literal_values = {}
clauses = add_clauses(parse_input())
can_solve = DPLL(clauses, literal_values)
literal_values = OrderedDict(sorted(literal_values.items()))

if can_solve:
    for s in literal_values:
        print(s, literal_values[s])
else:
    for s in literal_values:
        print(s, literal_values[s])
    print("UNSATISFIABLE")

