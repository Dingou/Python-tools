#!/usr/bin/env python
'''
-1: do not change position
1:  change position
'''
class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __str__(self):
        return '(%s: %s)' % (self.name, self.score)

    __repr__ = __str__

    def __cmp__(self, s):
        if isinstance(s, Student):
            if self.score < s.score:
                return 1
            elif self.score > s.score:
                return -1
            else:
                if self.name.lower() > s.name.lower():
                    return 1
                else:
                    return -1


L = [Student('Tim', 99), Student('Bob', 88), Student('Alice', 99)]
print sorted(L)