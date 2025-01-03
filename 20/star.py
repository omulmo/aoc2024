#! /usr/bin/env python3
from collections import defaultdict
import sys

from sortedcontainers import SortedSet

class State:
    def __init__(self, pos, dist):
        self.pos = pos
        self.dist = dist
    def __repr__(self):
        return f"{self.pos} ({self.dist})"

def nbors(pos):
    x,y = pos
    for nbor in (x+1,y),(x-1,y),(x,y-1),(x,y+1):
        yield nbor

def cheat_iterator(world,pos,max_dist=20):
    x,y = pos
    for dx in range(max_dist+1):
        for dy in range(max_dist-dx+1):
            if dx+dy < 2: continue
            for (i,j) in (x-dx,y-dy),(x+dx,y-dy),(x-dx,y+dy),(x+dx,y+dy):
                if world[i,j]=='.':
                    yield (x,y),(i,j),dx+dy


def shortest_paths(world, start):
    distances = defaultdict(lambda:sys.maxsize)
    queue = SortedSet(key=lambda x:x.dist)
    queue.add(State(start,0))
    while len(queue) > 0:
        state = queue.pop()
        if distances[state.pos] < state.dist:
            continue
        distances[state.pos] = state.dist
        for other in nbors(state.pos):
            if world[other]=='.':
                queue.add(State(other,state.dist+1))

    return distances


def find_cheats(world,start,stop, distance_check, mode=1):
    distances_from_start = shortest_paths(world,start)
    distances_from_stop = shortest_paths(world,stop)
    # cheats = set()
    # for pos in [pos for (pos,tile) in world.items() if pos != stop and tile=='.']:
    #     for step1 in nbors(pos):
    #         if world[step1]!='#': continue
    #         for step2 in nbors(step1):
    #             if step2 == pos or world[step2]!='.': continue
    #             cheats.add( (pos,step2) )

    shortest = distances_from_stop[start]
    ncheats = 0
    cheats = set()
    for pos in [pos for (pos,tile) in world.items() if pos != stop and tile=='.']:
        cheats.update(  cheat_iterator(world, pos, 2 if mode==1 else 20) )

    for a,b,steps in cheats:
        dist = distances_from_start[a] + steps + distances_from_stop[b]
        if distance_check(shortest-dist):
            ncheats += 1
    return ncheats

def make_world(inputs):
    world = defaultdict(lambda:'x')
    start = None
    stop = None
    for y,row in enumerate(inputs):
        for x,tile in enumerate(row):
            if tile == 'S':
                start = (x,y)
                tile = '.'
            if tile == 'E':
                stop = (x,y)
                tile = '.'
            world[x,y] = tile
    return world,start,stop

def one(inputs):
    world,start,stop = make_world(inputs)
    return find_cheats(world, start, stop, lambda dist: dist >= 100)

def two(inputs):
    world,start,stop = make_world(inputs)
    return find_cheats(world, start, stop, lambda dist: dist >= 100, mode=2)

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: line.strip()

    inputs = [ parse(line) for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
