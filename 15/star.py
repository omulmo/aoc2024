#! /usr/bin/env python3
import sys

def make_world(inputs, double=False):
    robot = None
    world = []
    for y,row in enumerate(inputs):
        if len(row) == 0:
            commands = ''.join(inputs[y+1:])
            return world, robot, commands

        line = ''
        for x in row:
            if x == '#': line += '##' if double else '#'
            if x == 'O': line += '[]' if double else 'O'
            if x == '.': line += '..' if double else '.'
            if x == '@':
                robot = (len(line),y)
                line += '..' if double else '.'
        world.append([c for c in line])

DXDY = { '<':(-1,0), '^':(0,-1), '>':(1,0), 'v':(0,1)}

def move(world,x,y,nx,ny,tile):
    assert(world[ny][nx] != '#')
    world[ny][nx] = tile
    world[y][x] = '.'

def try_move(world, x,y, dx, dy):
    to_check = [ (x,y) ]
    visited = set()
    moves = []

    while len(to_check) > 0:
        x,y = to_check.pop(0)  # important that this is FIFO so that moves is an ordered list
        if (x,y) in visited:
            continue
        visited.add((x,y))
        nx,ny = x+dx,y+dy
        tile = world[ny][nx]
        if tile=='#':
            raise Exception()

        moves.append( (x,y,nx,ny,world[y][x]) )
        if tile=='.':
            continue

        to_check.append((nx,ny))
        if tile in '[]' and dy != 0:
            to_check.append( (nx+1 if tile == '[' else nx-1, ny) )

    return reversed(moves) # do last move first

def do_command(world,x,y,command):
    (dx,dy) = DXDY[command]
    try:
        for args in try_move(world,x,y,dx,dy):
            move(world,*args)
        return x+dx,y+dy
    except:
        return x,y

def gps_score(world,x,y):
    return 100*y + x if world[y][x] in 'O[' else 0

def print_world(world,x,y):
    world[y][x] = '@'
    print('\n'.join( ''.join(row) for row in world))
    print('')
    world[y][x] = '.'


def doit(inputs, double=False):
    world,robot,commands = make_world(inputs,double)
    x,y = robot
    for command in commands:
        x,y = do_command(world,x,y,command)
        # print_world(world,x,y)

    print_world(world,x,y)

    return sum(gps_score(world,x,y) for y,row in enumerate(world) for x,_ in enumerate(row)) 


def one(inputs):
    return doit(inputs, double=False)

def two(inputs):
    return doit(inputs, double=True)


if __name__ == '__main__':
    task = '2' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: line.strip()

    inputs = [ parse(line) for line in open('15/large.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
