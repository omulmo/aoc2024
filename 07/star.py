#! /usr/bin/env python3
from operator import add, mul
import sys
import re
import itertools

def evaluate(eq, operands):
    sum = eq[0]
    for combo in itertools.product(operands,repeat=len(eq)-2):
        x = eq[1]
        for i,op in enumerate(combo):
            x = op(x,eq[i+2])
            if x > sum:
                break
        if x==sum:
            return sum
    return 0

def one(inputs):
    return sum(evaluate(eq, [mul,add]) for eq in inputs)

def two(inputs):
    concat = lambda a,b: int(str(a)+str(b))
    return sum(evaluate(eq, [mul,add,concat]) for eq in inputs)

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: list(map(int,re.findall(r"(\d+)",line.strip())))

    inputs = [ parse(line) for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
