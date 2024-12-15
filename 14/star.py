#! /usr/bin/env python3
from functools import reduce
from operator import mul
import sys
import re

def one(inputs):
    w,h = 101,103
    # w,h = 11,7
    mx, my = (w-1)//2, (h-1)//2
    quad = [0]*4
    for (x,y,vx,vy) in inputs:
        for _ in range(100):
            x = (w + x + vx) % w
            y = (h + y + vy) % h
        if x == mx or y == my: continue
        q = 0
        if x > mx: q += 1
        if y > my: q += 2
        quad[q] += 1
    print(quad)
    return reduce(mul, quad)

def two(inputs):
    pass

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: list(int(x) for r in re.findall(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line.strip()) for x in r)

    inputs = [ parse(line) for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
