#! /usr/bin/env python3
import sys
import re

def one(inputs):
    return sum(sum(int(a)*int(b) for (a,b) in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)",line)) for line in inputs)

def calc2(line,state):
    sum=0
    do=state
    for (op,a,b) in re.findall(r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))", line):
        if op=="do()":
            do=True
        elif op=="don't()":
            do=False
        elif do:
            print(f"adding {a}*{b}")
            sum += int(a)*int(b)
    return sum,do

def two(inputs):
    sum, state = 0, True
    for line in inputs:
        s, state = calc2(line, state)
        sum += s
    return sum

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: line.strip()

    inputs = [ parse(line) for line in open('03/sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
