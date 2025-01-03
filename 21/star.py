#! /usr/bin/env python3
from collections import defaultdict
import json
import sys

from sortedcontainers import SortedSet

def manhattan(a,b):
    (i1,j1),(i2,j2) = a,b
    return abs(i1-i2) + abs(j1-j2)

def directions(world,pos):
    x,y = pos
    for d,i,j in ('>',x+1,y),('<',x-1,y),('^',x,y-1),('v',x,y+1):
        if world[i,j] != '#':
            yield d,(i,j)

def shortest_paths(world,start,stop):
    min_costs=defaultdict(lambda:sys.maxsize)
    queue = SortedSet(key=lambda x:x[2])
    queue.add( ("",start,manhattan(start,stop)) )
    result = []

    while len(queue) > 0:
        path,pos,_ = queue.pop(0)
        cost = len(path)
        if cost > min_costs[pos] or cost > min_costs[stop]:
            continue
        if cost < min_costs[pos]:
            min_costs[pos] = cost
            if pos == stop:
               result = []
        if pos == stop:
            result.append( path )
            continue
        for dir,other in directions(world,pos):
            if min_costs[other] < cost+1: continue
            queue.add( (path+dir, other, len(path) + 1 + manhattan(other,stop)) )

    return result

def make_world(inputs):
    world = defaultdict(lambda:'#')
    for y,row in enumerate(inputs):
        for x,key in enumerate(row):
            world[x,y] = key
            world[key] = x,y
    return world

NUMPAD = '''789
456
123
#0A'''.splitlines()

KEYPAD = '''#^A
<v>'''.splitlines()

numpad = make_world(NUMPAD)
keypad = make_world(KEYPAD)

def get_min_length_strings(iterator):
    n, result = sys.maxsize, []
    for s in iterator:
        sn = len(s)
        if sn < n:
            n, result = sn, [s]
        elif sn == n:
            result.append(s)
    print(f"string length: {n}")
    return result

def precompute(nrobots=2):
    keystrokes = {}
    for start in '0123456789A':
        for stop in '0123456789A':
            if start==stop: continue
            # n,result = sys.maxsize, None
            # for path in shortest_paths(numpad, numpad[start], numpad[stop]):
            #     for robot1 in get_min_length_strings(typing(keypad, path+'A')):
            #         for robot2 in get_min_length_strings(typing(keypad, robot1)):
            #             if len(robot2) < n:
            #                 result, n = robot2, len(robot2)
            #                 #print(f"min length = {n} for robot1 length {len(robot1)}")

            paths = shortest_paths(numpad, numpad[start], numpad[stop])
            sequences = get_min_length_strings(x for path in paths for x in typing(keypad, path+'A'))
            for i in range(nrobots-1):
                sequences = get_min_length_strings(x for seq in sequences for x in typing(keypad, seq) )

            result = sequences.pop(0)

            keystrokes[start,stop] = result
    return keystrokes

def typing(world,sequence):
    result = [ '' ]
    pos = world['A']
    for seq in sequence:
        stop = world[seq]
        result = [ x+path+'A' for x in result for path in shortest_paths(world,pos,stop) ]
        pos = stop
    return result

def find_best_typing(start, stop):
    result, n = None, sys.maxsize
    for path in shortest_paths(numpad,start,stop):
        r = typing(keypad, path+'A')
        if len(r) < n:
            result, n = r, len(r)
    return result

def one(inputs):
    keystrokes=precompute(nrobots=25)
    sum = 0
    for code in inputs:
        pos = 'A'
        keys = ''
        for nxt in code:
            keys += keystrokes[pos,nxt]
            pos=nxt
        sum += len(keys) * int(code[:-1])
    return sum

def two(inputs):
    pass

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: line.strip()

    inputs = [ parse(line) for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
