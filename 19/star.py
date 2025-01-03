#! /usr/bin/env python3
from collections import defaultdict
from sortedcontainers import SortedSet
import sys

def test(orig, tokens):
    candidates = set([orig])
    visited = set()
    while len(candidates) > 0:
        str = candidates.pop()
        if str in visited: continue
        visited.add(str)
        for t in tokens:
            n = len(t)
            if n > len(str): continue
            if all(x == str[i] for i,x in enumerate(t)):
                if n == len(str):
                    return True
                candidates.add(str[n:])
    return False


def test2(orig, tokens):
    '''
    m = 0
    gbbr -> g+bbr,gb+br
    bbr(1) -> b+br
    br(2) -> b+r, br*  m=2
    r(2) -> r*  m=4

    m = 0
    rrbgbr -> r+rbgbr
    rbgbr(1) -> r+bgbr, rb+gbr
    bgbr(1) -> b + gbr
    gbr(1+1) -> g+br, gb+r
    br(2) -> b+r, br* -> m=2
    r(2+2) -> r* -> m=6

    '''
    candidates = SortedSet([0])
    rank = defaultdict(lambda:0)
    rank[0] = 1
    n = len(orig)
    m = 0
    while len(candidates) > 0:
        i = candidates.pop(0)
        for token in tokens:
            tn = len(token)
            if i+tn > n: continue
            if all(x == orig[i+j] for j,x in enumerate(token)):
                if i+tn == n:
                    m += rank[i]
                else:
                    candidates.add(i+tn)
                    rank[i+tn] += rank[i]
    print(f"{orig} -> {m}")
    return m



def one(inputs):
    tokens = set(map(lambda x:x.strip(), inputs[0].split(',')))
    return sum(test(str, tokens) for str in inputs[2:])

def two(inputs):
    tokens = set(map(lambda x:x.strip(), inputs[0].split(',')))
    return sum(test2(str, tokens) for str in inputs[2:])

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: line.strip()

    inputs = [ parse(line) for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
