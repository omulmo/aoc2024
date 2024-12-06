#! /usr/bin/env python3
from collections import defaultdict
from functools import cmp_to_key
import sys
import re

def parse(inputs):
    rules=defaultdict(lambda:set())
    pagelists=[]
    do_rules = True
    for line in inputs:
        if line=="":
            do_rules = False
            continue
        if do_rules:
            a,b = map(int, re.findall(r"\d+", line))
            rules[a].add(b)
        else:
            pagelist = list(map(int,line.split(",")))
            assert(len(pagelist) % 2 == 1) # assumption when finding the middle item
            pagelists.append(pagelist)

    return rules, pagelists

def validate_pagelist(rules, pagelist):
    '''returns middle page number if order is valid, or 0 if invalid'''
    v = set()
    for page in pagelist:
        if any(s in v for s in rules[page]):
            return 0
        v.add(page)
    return pagelist[len(pagelist)//2]

def one(rules, pagelists):
    return sum(validate_pagelist(rules, p) for p in pagelists)

def order_pagelist(rules,pagelist):
    page_cmp = lambda a,b: -1 if b in rules[a] else 1
    valid_order = sorted(pagelist, key=cmp_to_key(page_cmp))
    return valid_order[len(valid_order)//2]

def two(rules, pagelists):
    return sum(order_pagelist(rules,pl) for pl in pagelists if validate_pagelist(rules,pl)==0)

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    rules, pagelists = parse([ line.strip() for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])])
    print(function(rules, pagelists))
