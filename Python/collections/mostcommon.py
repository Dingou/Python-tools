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
