#!/usr/bin/python
from copy import deepcopy

x = 1

def global_ex():
    global x
    x +=1


if __name__ == "__main__":
    items = [('name', 'leo'), ('age', 12)]
    itemsdict = dict(items)  #{'age': 12, 'name': 'leo', 'sex': 'man'}
    len(itemsdict)  #2
    del itemsdict['age']
    y = itemsdict.copy()  #改变y影响x
    y = itemsdict.deepcopy()  #改变y不影响x
    y.get('name','none')
    itemsdict.clear()  #类似于sort无返回值的清空
    list1 = ['name', 'age']
    dict.fromkeys(list1)  #{'age': None, 'name': None}
    dict.has_key('name')
    a = {'age': 12, 'name': 'leo', 'sex': 'man'}
    it = a.items()  #get a list
    ite = a.iteritems() #get a inter of a list
    list(ite)
    b = 10
    assert 0 < b < 100
    c = ['leo','feng','page']
    d = ['12','13','14']
    zip(c,d)  #[('leo', '12'), ('feng', '13'), ('page', '14')]
    list(enumerate(c))  #<enumerate object at 0x1021e3a00>  [(0, 'leo'), (1, 'feng'), (2, 'page')]
    list(reversed(c))
    #map(function=,seq) every args use function
    #reduce(functoin.seq) function(function(seq[0],seq[1]),seq[2])
    








