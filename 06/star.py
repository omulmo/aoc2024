#! /usr/bin/env python3
from collections import defaultdict
import sys

N = (0,-1)
S = (0,1)
E = (1,0)
W = (-1,0)

DIRECTIONS = [N,E,S,W]

def step(world,pos,dir):
    (x,y),(a,b) = pos, DIRECTIONS[dir]
    next = (x+a,y+b)
    if world[next] == "#":
        dir = (dir+1)%4
    else:
        pos = next
    return pos,dir

def walk(world, pos, dir=0):
    visited=set()
    while world[pos] == ".":
        visited.add(pos)
        pos,dir = step(world,pos,dir)

    return len(visited)

def is_loop(world,pos,dir=0):
    x,y = pos
    walked = set((x,y,dir))
    while world[x,y] == ".":
        (x,y),dir = step(world,(x,y),dir)
        if (x,y,dir) in walked:
            return True
        walked.add((x,y,dir))
    return False


def place_obstacles(world,start_pos):
    obstacles = set()
    pos = start_pos
    dir = 0
    while world[pos] == ".":
        x,y = pos
        npos,ndir = step(world,pos,dir)
        if npos != pos and world[npos]=="." and npos not in obstacles:
            world[npos]="#"
            if is_loop(world, start_pos):
                obstacles.add(npos)
            world[npos]="."
        pos,dir = npos,ndir
    return len(obstacles)


def make_world(inputs):
    world = defaultdict(lambda: " ")
    start = None
    for y,row in enumerate(inputs):
        for x,c in enumerate(row):
            if c == "^":
                start=(x,y)
                c = "."
            world[x,y] = c
    return world, start

def one(inputs):
    return walk(*make_world(inputs))

def two(inputs):
    return place_obstacles(*make_world(inputs))

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: line.strip()

    inputs = [ parse(line) for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
