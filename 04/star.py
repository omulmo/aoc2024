#! /usr/bin/env python3
import sys

NW = (-1,-1)
NE = (1,-1)
SW = (-1,1)
SE = (1,1)

DIRECTIONS = ((1,0),(-1,0),(0,1),(0,-1),NW,NE,SW,SE)

def one(inputs):
    h = len(inputs)
    w = len(inputs[0])

    x_positions = ( (x,y) for y,row in enumerate(inputs) for x,c in enumerate(row) if c=="X" )

    count = 0
    for x,y in x_positions:
        for dx,dy in DIRECTIONS:
            i,j = x+3*dx, y+3*dy
            if 0<=i and i<w and 0<=j and j<h:
                xmas = [ inputs[y+n*dy][x+n*dx] for n in range(4) ]
                if xmas == ['X','M','A','S']:
                    count += 1
    return count


ROT = [ NW,NE,SE,SW ]

ROTATIONS = [( ROT[x%4], ROT[(x+1)%4], ROT[(x+2)%4], ROT[(x+3)%4] ) for x in range(4)]


def two(inputs):
    '''find all A, then look for MM+SS combos in cornering places'''
    h = len(inputs)
    w = len(inputs[0])

    # ignore any A placed on boundary
    a_positions = ( (x+1,y+1) for y,row in enumerate(inputs[1:-1]) for x,c in enumerate(row[1:-1]) if c=="A" )

    count = 0
    for x,y in a_positions:
        for rot in ROTATIONS:
            arr = [ inputs[y+j][x+i] for (i,j) in rot ]
            if arr == ['M','M','S','S'] or arr == ['S','S','M','M']:
                count += 1
                break
    return count


if __name__ == '__main__':
    task = '2' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: line.strip()

    inputs = [ parse(line) for line in open('04/sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
