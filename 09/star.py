#! /usr/bin/env python3
import sys
import re

def one(layout):
    assert(len(layout) % 2 == 1)
    layout.append(0)
    blocks = []
    fileid=0
    for i in range(0,len(layout),2):    
        blocks.extend( [fileid]*layout[i])
        fileid += 1
        blocks.extend( [None]*layout[i+1])

    j=len(blocks)-1
    i=0
    while i<j:
        #print(''.join(map(lambda x: '.' if x is None else str(x), blocks)))
        while blocks[j] == None:
            j-=1
        while blocks[i] is not None:
            i+=1
        if i<j:
            blocks[i] = blocks[j]
            blocks[j] = None

    return sum( i*fileid for i,fileid in enumerate(blocks) if fileid is not None)


def find_empty(array, stop, size):
    i = 0
    while i<stop:
        while array[i] is not None:
            i+=1
        if i+size > stop:
            return -1
        n = 0
        while array[i+n] is None:
            n+=1
        if n>=size:
            return i
        i += n
    return -1


def two(layout):
    assert(len(layout) % 2 == 1)
    layout.append(0)
    blocks = []
    fileid=0
    files = []
    for i in range(0,len(layout),2):
        files.append( (len(blocks), layout[i]) )
        blocks.extend( [fileid]*layout[i])
        fileid += 1
        blocks.extend( [None]*layout[i+1])

    files.reverse()
    for offset,filesize in files:
        idx = find_empty(blocks, offset, filesize)
        if idx < 0:
            continue
        assert(idx + filesize <= offset)
        for i in range(filesize):
            blocks[idx+i] = blocks[offset+i]
            blocks[offset+i] = None
                
    return sum( i*fileid for i,fileid in enumerate(blocks) if fileid is not None)



if __name__ == '__main__':
    task = '2' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: list(map(int,re.findall(r"\d", line.strip())))

    inputs = [ parse(line) for line in open('09/input.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs[0]))
