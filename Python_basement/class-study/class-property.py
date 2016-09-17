#!/usr/bin/python
"""
@property,use getter and setter to set function as a attribute
"""

class Student(object):

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2016 - self._birth





