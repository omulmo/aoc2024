#! /usr/bin/env python3
from collections import defaultdict
import itertools
import sys

def find_antennas(inputs):
    antennas=defaultdict(lambda:set())
    for y,row in enumerate(inputs):
        for x,c in enumerate(row):
            if c != ".":
                antennas[c].add((x,y))
    return antennas

def one(inputs):
    w,h = len(inputs[0]),len(inputs)
    inside = lambda pos: 0<=pos[0] and pos[0]<w and 0<=pos[1] and pos[1]<h

    antinodes=set()
    for array in map(list,find_antennas(inputs).values()):
        for i,p1 in enumerate(array):
            for p2 in array[i+1:]:
                (x1,y1),(x2,y2) = p1, p2
                dx = x2-x1
                dy = y2-y1
                for pos in (x1-dx,y1-dy), (x2+dx,y2+dy):
                    if inside(pos):
                        antinodes.add(pos)

    return len(antinodes)

def two(inputs):
    w,h = len(inputs[0]),len(inputs)
    inside = lambda pos: 0<=pos[0] and pos[0]<w and 0<=pos[1] and pos[1]<h

    antinodes=set()
    for array in map(list,find_antennas(inputs).values()):
        for i,p1 in enumerate(array):
            for p2 in array[i+1:]:
                (x1,y1),(x2,y2) = p1, p2
                dx = x2-x1
                dy = y2-y1
                i=0
                more=True
                while more:
                    more=False
                    for pos in (x1-i*dx,y1-i*dy), (x2+i*dx,y2+i*dy):
                        if inside(pos):
                            more = True
                            antinodes.add(pos)
                    i += 1

    return len(antinodes)

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: line.strip()

    inputs = [ parse(line) for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
