import argparse
import re

def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    return parser.parse_args().file


def add_clauses(filename):
    file = open(filename, "r")
    first_line = file.readline()

    print(first_line)
    for line in file:
        print(line)


add_clauses(parse_input())