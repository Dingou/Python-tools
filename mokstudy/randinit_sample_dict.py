from random import randint, sample
from collections import Counter
import re
from collections import OrderedDict
from time import time


data = [ randint(0, 20) for _ in range(30)]

d1 = dict.fromkeys(data,0)

for x in data:
    d1[x] += 1

c2 = Counter(data)

c2.most_common(3)

#TXT FILE TO FILTER

txt = open("1.txt").read()
re.split('\W+', txt)
c3 = Counter(re.split('\W+', txt))
c3.most_common(10)


d2 = { x: randint(0, 100) for x in 'zbcdefg'}
d2.keys()
d2.values()
zip(d2.values(), d2.keys())


sorted(d2.iteritems(), key = lambda x: x[1])


d3 = { x: randint(1,4) for x in sample('abcdefg', randint(1,5)) }
d4 = { x: randint(1,4) for x in sample('abcdefg', randint(1,5)) }
d5 = { x: randint(1,4) for x in sample('abcdefg', randint(1,5)) }

map(dict.viewkeys, [d3, d4 ,d5])

reduce(lambda a,b: a & b, map(dict.viewkeys, [d3, d4 ,d5]))

#让字典变的有序

