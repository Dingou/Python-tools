#!/usr/bin/python

class Student(object):
    """
    s = Student("hehe")
    print s
    s = prints when setting __repr__
    __getitem__ and __setitem__ useful in dict
    """
    def __init__(self, name):
        self.name = name
        print "Init"
    def __str__(self):
        return "Str"
    __repr__ = __str__


class Fib(object):
    def __init__(self):
        self.a , self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        self.a , self.b = self.b , self.a + self.b
        if self.a > 1000:
            raise StopIteration()
        return self.a

    def __getitem__(self, n):
        if isinstance(n, int):
            a , b = 1, 1
            for x in range(n):
                a , b = b , a+b
            return a
        if isinstance(n, slice):
            start = n.start
            stop = n.stop
            if start == None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                    a, b = b ,a+b
            return L

    class WPUnit(object):
        def __init__(self):
            self._res = {}

        def __setitem__(self, key, val):
            self._res[key] = val

        def __getitem__(self, key):
            if self._res.has_key(key):
                return self._res[key]
            else:
              r = WPUnit()
              self.__setitem__(key, r)
              return r
