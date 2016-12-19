import concurrent.futures
import os
import shlex
import subprocess
from collections import Counter
'''
use subprocess
'''


def git_fetch(cmd):
    counter = Counter()
    args = shlex.split(cmd)
    p = subprocess.Popen(args)

def conc():
    git_fail_counter = Counter()
    cmd = "git fetch ylly HEAD &> git.log"
    with concurrent.futures.ProcessPoolExecutor(max_workers=15) as executor:
        executor.map(git_fetch, [cmd]*100)

if __name__ == "__main__":
    os.chdir("/home/web")
    os.chdir("./workspace/youlun/")
    conc()


cmd = 'tail -n 500 /var/log/nginx/access.log|grep -E -v \"ELB-HealthChecker/1.0|HEAD\"|head -n 1|awk \'{ print $4 }\'|sed \'s/\[//g\''