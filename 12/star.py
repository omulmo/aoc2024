#! /usr/bin/env python3
from collections import defaultdict
import sys

SCAN_DIRECTIONS = { 'N': (0,-1), 'W': (-1,0) }

OPPOSITE = { 'N':'S', 'E':'W', 'S':'N', 'W':'E' }

BORDER = {'N':(1,0), 'E':(0,1), 'W': (0,1), 'S':(1,0)}

class Tile:
    def __init__(self,x,y,region,id):
        self.x = x
        self.y = y
        self.region = region
        self.id = id
        self.sides = dict( (dir,True) for dir in 'NEWS' )

    def __repr__(self):
        return f"({self.pos}:{self.region}:{self.sides})"

def make_world(inputs):
    world = defaultdict(lambda:Tile(-1,-1,'.',None))
    for y,row in enumerate(inputs):
        for x,c in enumerate(row):
            world[x,y] = Tile(x,y,c,None)
    return world, len(inputs[0]), len(inputs)

def identify_regions(world, w, h):
    region_id = 0
    regions = defaultdict(lambda:set())
    for y in range(h):
        for x in range(w):
            me = world[x,y]
            for dir,(dx,dy) in SCAN_DIRECTIONS.items():
                other = world[x+dx,y+dy]
                if other.region == '.': continue
                if me.region == other.region:
                    me.sides[dir] = False
                    other.sides[OPPOSITE[dir]] = False

                    if me.id is None:
                        me.id = other.id
                    elif me.id == other.id:
                        continue
                    else:
                        s1 = regions[me.id]
                        s2 = regions.pop(other.id)
                        for tile in s2:
                            tile.id = me.id
                        s1.update(s2)

            if me.id is None:
                me.id = region_id
                region_id += 1
            regions[me.id].add(me)

    return [ r for r in regions.values() ]

def region_score(region):
    area = len(region)
    perimeter = sum(sum(tile.sides.values()) for tile in region)
    return area * perimeter

def one(inputs):
    regions = identify_regions(*make_world(inputs))
    return sum(region_score(r) for r in regions)

def region_price(world, region):
    area = len(region)
    sides = 0
    for tile in region:
        for side in 'NEWS':
            if not tile.sides[side]:
                continue
            tile.sides[side] = False
            sides += 1
            dx,dy = BORDER[side]
            for dir in -1,1:
                n = dir
                more = True
                while more:
                    other = world[tile.x+n*dx, tile.y+n*dy]
                    if other.id == tile.id and other.sides[side]:
                        other.sides[side] = False
                        n += dir
                    else:
                        more = False

    tile = region.pop()
    print(f'{tile.region} : {area} * {sides} = {area*sides}')
    return area * sides

def two(inputs):
    world, w, h = make_world(inputs)
    return sum(region_price(world, region) for region in identify_regions(world, w, h))    


if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: line.strip()

    inputs = [ parse(line) for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
