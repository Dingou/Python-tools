#!/usr/bin/python
'''
    namedtuple: self designed tuple type
'''
from collections import namedtuple
Point = namedtuple('Point',['x', 'y'])
Circle = namedtuple('Circle', ['x', 'y', 'z'])
p = Point(1,2)
print p

#namedtuple是一个函数，它用来创建一个自定义的tuple对象，并且规定了tuple元素的个数，并可以用属性而不是索引来引用tuple的某个元素。