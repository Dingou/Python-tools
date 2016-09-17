#!/usr/bin/python

class student(object):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print "name: %s" % self.name

s = student('Michael')
s()