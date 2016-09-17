#!/usr/bin/python

import types
from types import MethodType

type('a') == types.StringType
type(u'a') == types.UnicodeType


def set_age(self, age):
    self.age = age

def set_score(self, score):
    self.score = score

class Student(object):
    """
    use __slots__ to restrict our class method,only in current class,but child class
    s.score = 99 error!!!
    s.name and s.age success
    """
    __slots__ = ('name', 'age', 'set_age')
    pass

if __name__ == "__main__":
    s = Student()
    s.name = "Leo"
    print s.name
    s.set_age = MethodType(set_age, s, Student)  #give s a new method
    s.set_age(25)
    s.age
    Student.set_score = MethodType(set_score, None, Student)




