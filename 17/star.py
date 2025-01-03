#! /usr/bin/env python3
import sys

def computer(a,b,c,memory):
    A = a
    B = b
    C = c
    
    combo = lambda x: x if x < 4 else A if x==4 else B if x==5 else C if x==6 else None

    outputs = []

    ip = 0
    while 0 <= ip and ip <len(memory):
        opcode,operand = memory[ip],memory[ip+1]
        if opcode == 0:
            # adv
            A = A // (2**combo(operand))
        elif opcode == 1:
            # bxl
            B = B ^ operand
        elif opcode == 2:
            # bst
            B = combo(operand) % 8
        elif opcode == 3:
            # jnz
            if A != 0:
                ip = operand
                continue
        elif opcode == 4:
            # bxc
            B = B ^ C
        elif opcode == 5:
            # out
            outputs.append(combo(operand) % 8)
        elif opcode == 6:
            # bdv
            B = A // (2**combo(operand))
        elif opcode == 7:
            # cdv
            C = A // (2**combo(operand))
        else:
            raise Exception()
        ip += 2

    return A,B,C,outputs


def parse_input(inputs):
    a = int(inputs[0].split(' ')[-1])
    b = int(inputs[1].split(' ')[-1])
    c = int(inputs[2].split(' ')[-1])
    memory = list(map(int, inputs[-1].split(' ')[-1].split(',')))
    return a,b,c,memory


def one(inputs):
    a,b,c,outputs = computer(*parse_input(inputs))
    return ",".join(map(str,outputs))

def two(inputs):
    '''
    the program outputs an array that is of equal bit length to
    the octal representation of the input register A.
    '''
    a,b,c,program = parse_input(inputs)
    progstr = "".join(map(lambda x:f"{x:03b}",program))

    a1,a2 = 1, 2**(2+len(progstr))
    while a2-a1 > 1:
        a = a1 + (a2-a1)//2
        _,_,_,output = computer(a,0,0,program)
        if len(output)<len(program):
            a1 = a
        elif len(output)>len(program):
            a2 = a
        else:
            print(f"match length: {a}")

        print(f"A = [{a1},{a2}]")
    return a1

if __name__ == '__main__':
    task = '1' if len(sys.argv)<2 else sys.argv[1]
    function = one if task == '1' else two

    parse = lambda line: line.strip()

    inputs = [ parse(line) for line in open('sample.txt' if len(sys.argv)<3 else sys.argv[2])]
    print(function(inputs))
