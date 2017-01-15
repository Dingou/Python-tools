#!/usr/bin/env python
'''
ipython timeit
'''

from random import randint

data = [randint(-10, 10) for _ in xrange(10)]

s = set(data)

{x for x in s if x%3 == 0}

filter(lambda x: x>=0, data)

[x for x in data if x >= 0]

dictdata = { x: randint(0, 100) for x in xrange(20) }

print dictdata

newdictdata = {k:v for k,v in dictdata.iteritems() if v > 60 }

print newdictdata