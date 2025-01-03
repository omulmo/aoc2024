#! /usr/bin/env python3

import unittest
from star import find_best_typing, one, two, make_world, NUMPAD, KEYPAD, typing, shortest_paths, precompute

SAMPLE = '''029A
980A
179A
456A
379A'''.splitlines()

class Test1(unittest.TestCase):
    def test1(self):
        numpad = make_world(NUMPAD)
        keypad = make_world(KEYPAD)

        results = shortest_paths(numpad, numpad['2'], numpad['9'])
        for seq in '>^^', '^>^', '^^>':
            self.assertTrue(seq in results, f"not in results: {seq}")

        results = typing(numpad,'029A')
        for seq in '<A^A>^^AvvvA', '<A^A^>^AvvvA', '<A^A^^>AvvvA':
            self.assertTrue(seq in results, f"not in results: {seq}")

    def test2(self):
        self.assertEqual(one([ "029A"]), 68*29)
        self.assertEqual(one(SAMPLE), 126384)

class Test2(unittest.TestCase):
    def testTwo(self):
        pass

if __name__ == '__main__':
    unittest.main()
