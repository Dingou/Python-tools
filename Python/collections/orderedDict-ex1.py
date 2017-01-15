# *.* coding: utf-8 *.*
'''
iteritems: transfer dict each element into key and value
items: transfer dict each element into tuple k, thus k[0], k[1]
'''
from collections import OrderedDict
od = OrderedDict()
od['z'] = 1
od['y'] = 2
od['x'] = 3


d1 = {'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}
d1o = OrderedDict()
# 将d按照key来排序
OrderedDict(sorted(d1.items(), key=lambda t: t[0]))
OrderedDict([('apple', 4), ('banana', 3), ('orange', 2), ('pear', 1)])
# 将d按照value来排序
OrderedDict(sorted(d1.items(), key=lambda t: t[1]))
OrderedDict([('pear', 1), ('orange', 2), ('banana', 3), ('apple', 4)])
# 将d按照key的长度来排序
OrderedDict(sorted(d1.items(), key=lambda t: len(t[0])))
OrderedDict([('pear', 1), ('apple', 4), ('orange', 2), ('banana', 3)])

d = { 'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2 }
d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
OrderedDict([('apple', 4), ('banana', 3), ('orange', 2), ('pear', 1)])
d.popitem()
('pear', 1)
d.popitem(last=False) #移除第一个
('apple', 4)


d = OrderedDict.fromkeys('abcde', 0)

# 进入字典的顺序
d2 =  OrderedDict()
d2['leo'] = 1
d2['bob'] = 2
d2['kaka'] = 3
