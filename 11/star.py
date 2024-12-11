#! /usr/bin/env python3
from collections import defaultdict
import sys

class Stone:
    def __init__(self, value):
        self.value = value
        self.next = None

    def append(self,stone):
        stone.next = self.next
        self.next = stone

    def split(self, value_as_str):
        half = len(value_as_str)//2
        l,r = value_as_str[:half], value_as_str[half:]
        self.value = int(l)
        self.append(Stone(int(r)))
        return self.next

    def doit(self):
        n = self.next
        if self.value == 0:
            self.value = 1
            return self.next

        s = str(self.value)
        if len(s) % 2 == 0:
            stone = self.split(s)
            return stone.next

        self.value *= 2024
        return self.next

def blink(first):
    cur = first
    while cur is not None:
        cur = cur.doit()

def length(first):
    cur = first
    n = 0
    while cur is not None:
        cur = cur.next
        n += 1
    return n    

def array(first):
    a = []
    cur=first
    while cur is not None:
        a.append(cur.value)
        cur = cur.next
    return a


def attempt_one(inputs):
    first = Stone(inputs[0])
    cur = first
    for i in inputs[1:]:
        cur.append(Stone(i))

    for _ in range(25):
        blink(first)

    return length(first)


def attempt_two(inputs, rounds=25):
    '''
        0 -> 1
        1 -> 2024
        2024 -> 20, 24
        20, 24 -> 2, 0, 2, 4

        and so on. we always end up with single digits after multiplying
        with 2024 until we get a number with even digits
    '''

    cache = defaultdict(lambda:None)
    candidates = set(inputs)
    while len(candidates) > 0:
        i = candidates.pop()
        if cache[i] is not None:
            continue
        first = Stone(i)
        blink(first)
        cache[i] = array(first)
        candidates.update(cache[i])

    stones = defaultdict(lambda: 0)
    for i in inputs:
        stones[i] += 1

    for _ in range(rounds):
        counter = defaultdict(lambda: 0)
        for (i,n) in stones.items():
            for j in cache[i]:
                counter[j] += n
        stones = counter

    return sum(stones.values())


def one(inputs):
    return attempt_two(inputs, 25)

def two(inputs):
    return attempt_two(inputs, 75)


if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: list(map(int,line.strip().split()))

    inputs = [ parse(line) for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs[0]))
