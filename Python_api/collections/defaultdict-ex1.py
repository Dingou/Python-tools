# *.* coding: utf-8 -*-
from collections import defaultdict
dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'abc'
dd['key1'] # 'abc'
dd['key2'] # 'N/A'

