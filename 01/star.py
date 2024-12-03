#! /usr/bin/env python3
from collections import defaultdict
import sys

def parse(inputs):
    a=[]
    b=[]
    for line in inputs:
        v0, v1 = map(int, line.split())
        a.append(v0)
        b.append(v1)
    return a,b    

def dist(vals):
    a,b = vals
    return abs(a-b)

def one(inputs):
    a,b = parse(inputs)
    return sum(map(dist, zip(sorted(a),sorted(b))))

def two(inputs):
    a,b = parse(inputs)
    histogram = defaultdict(lambda: 0)
    for v in b:
        histogram[v] += 1

    similarity = lambda v: v*histogram[v]

    return sum(map(similarity, a))


if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    inputs = [ line.strip() for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
