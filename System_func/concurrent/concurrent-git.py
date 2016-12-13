import concurrent.futures
import os
import shlex
import subprocess

def git_fetch(cmd):
    args = shlex.split(cmd)
    p = subprocess.Popen(args)
    if p.returncode != None:
        print "\nreturncode: %s\n" % p.returncode

def conc():
    cmd = "git fetch ylly HEAD"
    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:
        executor.map(git_fetch, [cmd]*100)

if __name__ == "__main__":
    os.chdir("/home/web")
    os.chdir("./workspace/youlun/")
    conc()



