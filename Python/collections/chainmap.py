from collections import ChainMap
a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}
m = ChainMap(a, b)
# 构造一个ChainMap对象
m
m['a']
'A'
m['b']
'B'
# 将m变成一个list
m.maps
[{'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'}]