#!/usr/bin/env python
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def Fib(n):
    list = []
    for i in range(n):
        list.append(fib(i))
    yield list


class Fib(object):
    def __init__(self, num):
        self.num = num
        if self.num == 0:
            L = []
        elif self.num == 1:
            L = [0]
        else:
            L = [0, 1]
            for i in range(2, self.num):
                L.append(L[-1]+L[-2])
        self.lst = L
    def __len__(self):
        return len(self.lst)
    def __str__(self):
        return str(self.lst)
