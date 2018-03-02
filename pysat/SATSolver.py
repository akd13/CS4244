import argparse
import re
import sys, copy

clauseSet = []
solved = {}

def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    return parser.parse_args().file

def add_clauses(filename,clauseSet):
    file = open(filename, "r")
    for line in file:
        m = re.search('^\s*((-)*\d+\s*)*(0)(\\n)$', line)
        if m!=None:
            clauseSet.append(map(int, m.group(0).split()))

def DPLL(set):
    if (len(set) == 0):  # clause set empty
        return True
    for clause in set:  # contains an empty clause
        if (len(clause) == 1):
            return False
    global solved
    for clause in set:  # unit prop on unit clause
        index = 0
        if (len(clause) == 2):
            item = clause[0]
            if item < 0:
                solved[-1 * item] = 0
            else:
                solved[item] = 1
            set.pop(index)
            index = 0
            while (index != len(set)):
                marked = False
                for lit in set[index]:
                    if lit == item:
                        marked = True
                        break
                    elif (lit == (-1 * item)):
                        set[index].remove(lit)
                if marked:
                    set.pop(index)
                    index = index - 1
                index = index + 1
            return DPLL(copy.deepcopy(set))

    shortClause = set[0]
    for clause in set:  # choose a variable by shortest remaining
        if len(shortClause) > len(clause):
            shortClause = clause
    item = shortClause[0]
    tempSet = copy.deepcopy(set)
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
        tempSet = copy.deepcopy(set)
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

add_clauses(parse_input(),clauseSet)
solver = DPLL(copy.deepcopy(clauseSet))
if solver:
    for set in solved:
        print(set, solved[set])
else:
    print "UNSATISFIABLE"

