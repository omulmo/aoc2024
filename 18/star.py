#! /usr/bin/env python3
from collections import defaultdict
import os
import re
import sys
from sortedcontainers import SortedSet

def manhattan(a,b):
    (x1,y1),(x2,y2) = a,b
    return abs(x1-x2) + abs(y1-y2)

class State:
    def __init__(self, pos, cost, stop):
        self.pos = pos
        self.cost = cost
        self.heur = cost + manhattan(pos,stop)

def a_star(inputs, count, dim):
    world = defaultdict(lambda:'.')
    for pos in inputs[:count]:
        world[pos]='#'

    stop = (dim,dim)
    visited=set()
    states=SortedSet([State((0,0),0,stop)], key=lambda x:x.heur)
    shortest = sys.maxsize

    while len(states) > 0:
        curr = states.pop(0)
        if curr.pos in visited or curr.cost > shortest:
            continue
        if curr.pos == stop:
            shortest = min(shortest,curr.cost)
            continue
        visited.add(curr.pos)
        x,y = curr.pos
        for i,j in (x-1,y),(x+1,y),(x,y-1),(x,y+1):
            if i<0 or j<0 or i>dim or j>dim: continue
            if world[i,j]=='.':
                states.add(State((i,j),curr.cost+1,stop))
    
    return shortest if shortest < sys.maxsize else None 

def one(inputs):
    count,dim = (12,6) if os.environ.get("TEST",None) != None else (1024,70)
    return a_star(inputs,count,dim)
    
def two(inputs):
    _,dim = (12,6) if os.environ.get("TEST",None) != None else (1024,70)

    n = len(inputs)
    a,b = 0,n-1
    while b-a > 1:
        count = a + (b-a) // 2
        shortest = a_star(inputs,count,dim)
        if shortest == None:
            b = min(count,b)
        else:
            a = max(count,a)
        print(f"count={count} a={a} b={b}")

    x,y = inputs[a]
    return f"{x},{y}"

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: tuple(map(int,re.findall(r"(\d+),(\d+)", line.strip()).pop()))

    inputs = [ parse(line) for line in open('18/sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
