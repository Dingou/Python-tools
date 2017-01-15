import re
from collections import Counter
c3 = Counter(re.split('\W+', 'a/b'))
c3.most_common(3)

# \W none word
