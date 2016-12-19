import concurrent.futures
import os
import shlex
import commands
from collections import Counter
import re
from threading import Lock

lock = Lock()
error_msg = "^ssh_exchange_identification:"
error_pattern = re.compile(error_msg)
counter = Counter()

def git_fetch(cmd):
    (status, out) = commands.getstatusoutput(cmd)
    if error_pattern.match(out):
        with lock:
            print out
            counter["ssh_error"] = 1
            return counter

def conc():
    git_fail_counter = Counter()
    cmd = "git fetch ylly HEAD "
    with concurrent.futures.ProcessPoolExecutor(max_workers=15) as executor:
        for counter in executor.map(git_fetch, [cmd] * 200):
            git_fail_counter.update(counter)
    print "ssh_exchange_identification error happend %s times" % git_fail_counter['ssh_error']

if __name__ == "__main__":
    os.chdir("/home/web")
    os.chdir("./workspace/youlun/")
    conc()