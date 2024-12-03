#! /usr/bin/env python3
import sys

def check(v,a,b):
    diff = v[a]-v[b]
    safe = 1 <= abs(diff) and abs(diff) <= 3
    sign = 1 if diff > 0 else -1
    return safe, sign

def issafe(v):
    safe,sign = check(v,0,1)
    if not safe:
        return False
    i = 1
    for j in range(2,len(v)):
        safe,s = check(v,i,j)
        if not safe or s != sign:
            return False
        i=j
    return True

def issafe2(v):
    if issafe(v):
        return True
    for i in range(len(v)):
        if issafe(v[0:i]+v[i+1:]):
            return True
    return False

def one(inputs):
    return sum(issafe(v) for v in inputs)

def two(inputs):
    return sum(issafe2(v) for v in inputs)

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: list(map(int,line.strip().split()))

    inputs = [ parse(line) for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
