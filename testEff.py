#-*-coding:utf-8-*-

import random
from timeit import timeit

class Efficiency:
    def __init__(self):
        self.hash1 = {(10, 42): 3, (20, 45): 6, (34, 20): 3, (32, 10): 7, (55, 8): 0, (20, 20): 4,
                      (10, 44): 2, (9, 32): 10, (1, 2): 4, (30, 17):5, (40, 20):8, (50, 50):6}
        self.hash2 = {(10, 42): 3, (20, 45): 6, (34, 20): 3, (32, 10): 7, (55, 8): 0, (20, 20): 4,
                      (10, 44): 2, (9, 32): 10, (1, 2): 4, (30, 17):5, (40, 20):8, (50, 50):6}
        for i in range(64):
            for j in range(42):
                self.hash2.setdefault((i, j), 0)

    def search1(self, x, y):
        try:
            res=self.hash1[(x, y)]
        except KeyError:
            return 0
        return res

    def search2(self, x, y):
        return self.hash2[(x, y)]

    def search3(self, x, y):
        if (x, y) in self.hash1: return self.hash1[(x, y)]
        return 0

    def random1(self):
        x=random.randint(0, 63)
        y=random.randint(0, 41)
        return self.search1(x, y)

    def random2(self):
        x=random.randint(0, 63)
        y=random.randint(0, 41)
        return self.search2(x, y)

    def random3(self):
        x=random.randint(0, 63)
        y=random.randint(0, 41)
        return self.search3(x, y)

if __name__=="__main__":
    ef=Efficiency();
    for i in range(10):
        print("Time elapsed in method1 with default set:" +
              str(timeit("ef.random1()", "from __main__ import ef", number=1000000)))
        print("Time elapsed in method2 with try&except:" +
              str(timeit("ef.random2()", "from __main__ import ef", number=1000000)))
        print("Time elapsed in method3 with only search:" +
              str(timeit("ef.random3()", "from __main__ import ef", number=1000000)))
        print("\n")