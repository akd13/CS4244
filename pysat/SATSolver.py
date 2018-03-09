import argparse
import re
import copy
from collections import OrderedDict

clauses = []
solved = {}

def parse_input(): #open input file from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    return parser.parse_args().file

def add_clauses(filename):
    file = open(filename, "r")
    for line in file:
        m = re.search('^\s*((-)*\d+\s*)*(0)(\\n)$', line) #detect clause
        if m!=None:
            raw_clause = m.group(0).split()
            size =  len(raw_clause)
            if (raw_clause[size-1]==0):
                raw_clause.remove(size-1)

            clause = [int(numeric_string) for numeric_string in raw_clause]
            clauses.append(clause)
    return clauses

class Clause(object):

    def __init__(self):
        self.id = self.make_id()

    @classmethod
    def make_id(cls):
        cls._num += 1
        return cls._num


def DPLL(clauseSet):
    if (len(clauseSet) == 0):  # clause set empty
        return True
    for clause in clauseSet:  # contains an empty clause
        if (len(clause) == 1):
            return False
    global solved
    for clause in clauseSet:  # unit prop on unit clause
        index = 0
        if (len(clause) == 2):
            item = clause[0]
            if item < 0:
                solved[-1 * item] = 0
            else:
                solved[item] = 1
            clauseSet.pop(index)
            index = 0
            while (index != len(clauseSet)):
                marked = False
                for lit in clauseSet[index]:
                    if lit == item:
                        marked = True
                        break
                    elif (lit == (-1 * item)):
                        clauseSet[index].remove(lit)
                if marked:
                    clauseSet.pop(index)
                    index = index - 1
                index = index + 1
            return DPLL(copy.deepcopy(clauseSet))

    shortClause = clauseSet[0]
    for clause in clauseSet:  # choose a variable by shortest remaining
        if len(shortClause) > len(clause):
            shortClause = clause
    item = shortClause[0]
    tempSet = copy.deepcopy(clauseSet)
    tempSet.remove(shortClause)

    index = 0
    while (index != len(tempSet)):
        marked = False
        for lit in tempSet[index]:
            if lit == item:
                marked = True
                break
            elif (lit == (-1 * item)):
                tempSet[index].remove(lit)
        if marked:
            tempSet.pop(index)
            index = index - 1
        index = index + 1
    tempSolve = copy.deepcopy(solved)
    done = DPLL(tempSet)
    if done:
        if item < 0:
            solved[-1 * item] = 0
        else:
            solved[item] = 1
        return done
    else:
        solved = copy.deepcopy(tempSolve)
        item = (-1 * item)
        tempSet = copy.deepcopy(clauseSet)
        index = 0
        while (index != len(tempSet)):
            marked = False
            for lit in tempSet[index]:
                if lit == item:
                    marked = True
                    break
                elif (lit == (-1 * item)):
                    tempSet[index].remove(lit)
            if marked:
                tempSet.pop(index)
                index = index - 1
            index = index + 1
        if item < 0:
            solved[-1 * item] = 0
        else:
            solved[item] = 1
    return DPLL(tempSet)

clauses = add_clauses(parse_input())
solver = DPLL(copy.deepcopy(clauses))
solved = OrderedDict(sorted(solved.items()))

if solver:
    for s in solved:
        print(s, solved[s])
else:
    print("UNSATISFIABLE")

