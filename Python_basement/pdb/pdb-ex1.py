#!/usr/bin/python
#There are two ways to pdb
#logging is recommanded
#First:
# err.py
s = '0'
n = int(s)
print(10 / n)

# l to print code
# n to run next cmd
# p s / p n to show the parameter
#Second:
#pdb.set_trace()
import pdb
s = '0'
n = int(s)
pdb.set_trace() # stop here p to overview c to continue
print(10 / n)