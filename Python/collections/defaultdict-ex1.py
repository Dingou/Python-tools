# *.* coding: utf-8 -*-
from collections import defaultdict
dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'abc'
dd['key1'] # 'abc'
dd['key2'] # 'N/A'

s1 = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]

d1 = defaultdict(list)
for k, v in s1:
    d1[k].append(v)


d2 = defaultdict(set)
for k,v in s1:
    d2[k].add(v)

s2 = 'hello world'
d3 = defaultdict(int)

for k in s2:
    d3[k] += 1