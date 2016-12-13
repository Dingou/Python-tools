from collections import Counter
from concurrent import futures
import glob
import gzip
import itertools
import subprocess

def count_urls(filename):
    counter = Counter()
    p = subprocess.Popen(["gzcat", filename],
                         stdout = subprocess.PIPE)
    for line in p.stdout:
        request = line.split('"')[1]
        path = request.split(" ")[1]
        if path.endswith(".html"):
            counter[path] += 1
    return counter

filenames = glob.glob("www_logs/www.*.gz")

merged_counter = Counter()
with futures.ProcessPoolExecutor(max_workers=4) as executor:
    for counter in executor.map(count_urls, filenames):
        merged_counter.update(counter)

for path, count in merged_counter.most_common(10):
    print count, path


'''
15830 /Python/PyRSS2Gen.html
13722 /writings/NBN/python_intro/command_line.html
11739 /writings/NBN/threads.html
10663 /writings/NBN/validation.html
6635 /writings/diary/archive/2007/06/01/lolpython.html
4525 /writings/NBN/writing_html.html
3756 /writings/NBN/generators.html
3465 /writings/NBN/parsing_with_ply.html
2958 /writings/diary/archive/2005/04/21/screen_scraping.html
2786 /writings/NBN/blast_parsing.html

'''