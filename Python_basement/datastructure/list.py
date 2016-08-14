#!/usr/bin/python
'''
Leak filling
'''
if __name__ == "__main__":
    names_1 = ['a','b','c']
    names_2 = ['c','d','e']
    numbers_1 = [1,2,3,4,1,2,3,4,5]
    numbers_2 = [5,6,7,8]
    del names_1[2] #delete item
    numbers_1.count(1) #count numbers
    numbers_1.extend(numbers_2) #change numbers_1
    numbers_1 + numbers_2 #no changes,low efficiency
    numbers_2.index(5) #get index of 5 = 1
    numbers_2.insert(-1,9) #insert at location of -1
    numbers_2.reverse()
    numbers_2.sorted() #recommand
    numbers_2.sort(key=len) #len,reverse=true,cmp




