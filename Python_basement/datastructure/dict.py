#!/usr/bin/python
from copy import deepcopy

if __name__ == "__main__":
    items = [('name', 'leo'), ('age', 12)]
    itemsdict = dict(items)  #{'age': 12, 'name': 'leo'}
    len(itemsdict)  #2
    del itemsdict['age']
    y = itemsdict.copy()  #改变y影响x
    y = itemsdict.deepcopy()  #改变y不影响x
    y.get('name','none')
    itemsdict.clear()  #类似于sort无返回值的清空
    list1 = ['name', 'age']
    dict.fromkeys(list1)  #{'age': None, 'name': None}


