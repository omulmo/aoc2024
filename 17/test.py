#! /usr/bin/env python3

import re
import unittest
from star import one, two, computer

class Test1(unittest.TestCase):
    def test1(self):
        a,b,c,outputs = computer(0,0,9,[2,6])
        self.assertEqual(b,1)
    def test2(self):
        a,b,c,outputs = computer(10,0,0,[5,0,5,1,5,4])
        self.assertEqual(outputs,[0,1,2])
    def test3(self):
        a,b,c,outputs = computer(2024,0,0,[0,1,5,4,3,0])
        self.assertEqual(a, 0)
        self.assertEqual(outputs,[4,2,5,6,7,7,7,7,3,1,0])
    def test4(self):
        a,b,c,outputs = computer(0,29,0,[1,7])
        self.assertEqual(b,26)
    def test5(self):
        a,b,c,outputs = computer(0,2024,43690,[4,0])
        self.assertEqual(b,44354)
    # def test6(self):
    #     program = [0,3,5,4,3,0]
    #     goal=117440
    #     for i in range(goal-10,goal+11):
    #         a,b,c,outputs = computer(i,0,0,program)
    #         outstr = "".join(map(lambda x:f"{x:03b}",outputs))
    #         istr = f"{i:3b}".rjust(len(outstr),"0")
    #         iarr = list(map(lambda x:int(x,2), re.findall('.{3}', istr)))
    #         print(i,a,b,c, istr, iarr, outputs, outstr)

    def test7(self):
        program = [2,4,1,2,7,5,0,3,1,7,4,1,5,5,3,0]
        goal=2**30 + 2**20 + 2**10 + 4372
        for i in range(goal-10,goal+11):
            a,b,c,outputs = computer(i,0,0,program)
            outstr = "".join(map(lambda x:f"{x:03b}",outputs))
            istr = f"{i:3b}".rjust(len(outstr),"0")
            iarr = list(map(lambda x:int(x,2), re.findall('.{3}', istr)))
            print(i,a,b,c, istr, iarr, outputs, outstr)




if __name__ == '__main__':
    unittest.main()
