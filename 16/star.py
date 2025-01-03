#! /usr/bin/env python3
from collections import defaultdict
import sys
from sortedcontainers import SortedSet

def find_start_stop(world):
    start = None
    stop = None
    for y,row in enumerate(world):
        x = row.find("S")
        if x >= 0:
            start = (x,y)
        x = row.find("E")
        if x >= 0:
            stop = (x,y)
    return start,stop

N,E,S,W = 0,1,2,3

DIRECTIONS = { N:(0,-1), W:(-1,0), S:(0,1), E:(1,0)}

def one(world):
    (i,j),stop = find_start_stop(world)
    queue = SortedSet([(0,(i,j,E))], key=lambda x:x[0])
    visited = set()
    costs = defaultdict(lambda:sys.maxsize)
    stop_cost = sys.maxsize

    while len(queue) > 0:
        (cost,state) = queue.pop(0)
        if state in visited:
            continue
        visited.add(state)
        if costs[state] < cost:
            continue
        costs[state] = cost
        x,y,facing = state
        if (x,y) == stop:
            if cost <= stop_cost:
                stop_cost = cost
            continue
        dx,dy = DIRECTIONS[facing]
        if world[y+dy][x+dx] != '#':
            queue.add((cost+1,(x+dx,y+dy,facing)))

        for turn in ((4+facing+i) % 4 for i in (-1,1)):
            dx,dy = DIRECTIONS[turn]
            if world[y+dy][x+dx] != '#':
                queue.add((cost+1000,(x,y,turn)))
    return stop_cost


def best_paths(world):
    (i,j),stop = find_start_stop(world)
    start_state = (i,j,E)
    queue = SortedSet([(0,start_state,None)], key=lambda x:x[0])
    costs = defaultdict(lambda:sys.maxsize)
    stop_cost = sys.maxsize
    best_paths = defaultdict(lambda:[])
    stop_states = []
    
    while len(queue) > 0:
        (cost,state,prev) = queue.pop(0)
        if costs[state] < cost:
            continue
        costs[state] = cost
        best_paths[state].append(prev)
        x,y,facing = state
        if (x,y) == stop:
            stop_states.append(state)
            stop_cost = min(cost, stop_cost)
            continue
        dx,dy = DIRECTIONS[facing]
        if world[y+dy][x+dx] != '#':
            queue.add((cost+1,(x+dx,y+dy,facing), state))

        for turn in ((4+facing+i) % 4 for i in (-1,1)):
            dx,dy = DIRECTIONS[turn]
            if world[y+dy][x+dx] != '#':
                queue.add((cost+1000,(x,y,turn), state))

    tile_set = set()
    queue = set( filter(lambda state:costs[state]==stop_cost, stop_states))

    while len(queue) > 0:
        state = queue.pop()
        if state is None: continue
        (x,y,facing) = state
        tile_set.add((x,y))
        queue.update(best_paths[state])

    return len(tile_set)


def two(inputs):
    return best_paths(inputs)

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: line.strip()

    inputs = [ parse(line) for line in open('16/7036.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
