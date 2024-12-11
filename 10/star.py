#! /usr/bin/env python3
from collections import defaultdict
import sys

def make_world(inputs):
    world = defaultdict(lambda:-1)
    trailheads = []
    for y,row in enumerate(inputs):
        for x,h in enumerate(map(int,row)):
            world[x,y] = h
            if h==0: trailheads.append((x,y))
    return world, trailheads

def find_peaks(world, trailheads):
    peaks = dict( (pos,set([(pos)])) for pos in trailheads )
    for h in range(1,10):
        candidates = defaultdict(lambda:set())
        for (x,y), trailheads in peaks.items():
            for nbor in (x-1,y),(x+1,y),(x,y-1),(x,y+1):
                if world[nbor] == h:
                    candidates[nbor].update(trailheads)
        peaks = candidates
    return peaks


def find_all_paths(world, start, dest):
    if start == dest: return 1
    h = world[start]
    x,y = start
    count = 0
    for nbor in (x-1,y),(x+1,y),(x,y-1),(x,y+1):
        if world[nbor] == h+1:
            count += find_all_paths(world, nbor, dest)
    return count

def one(inputs):
    world, trailheads = make_world(inputs)
    peaks = find_peaks(world, trailheads)
    return sum(len(v) for v in peaks.values())

def two(inputs):
    world, trailheads = make_world(inputs)
    peaks = find_peaks(world, trailheads)
    return sum(find_all_paths(world, start, dest) for dest, starts in peaks.items() for start in starts)

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: line.strip()

    inputs = [ parse(line) for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
