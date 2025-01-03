#! /usr/bin/env python3

import unittest
from star import one, two, make_world, shortest_paths, find_cheats

WORLD = '''###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############'''.splitlines()

class Test1(unittest.TestCase):
    def testOne(self):
        world,start,stop = make_world(WORLD)
        dist = shortest_paths(world, stop)
        self.assertEqual(dist[start], 84)
        self.assertEqual(find_cheats(world, start, stop, lambda dist: dist==2), 14)
        self.assertEqual(find_cheats(world, start, stop, lambda dist: dist==4), 14)
        self.assertEqual(find_cheats(world, start, stop, lambda dist: dist==12), 3)
        self.assertEqual(find_cheats(world, start, stop, lambda dist: dist==64), 1)


        self.assertEqual(find_cheats(world, start, stop, lambda dist: dist==50, mode=2), 32)
        self.assertEqual(find_cheats(world, start, stop, lambda dist: dist==52, mode=2), 31)
        self.assertEqual(find_cheats(world, start, stop, lambda dist: dist==76, mode=2), 3)


class Test2(unittest.TestCase):
    def testTwo(self):
        pass

if __name__ == '__main__':
    unittest.main()
