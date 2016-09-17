#!/usr/bin/python
'''
local: run local
run: which is similar to local but runs remotely instead of locally.
abort: used to manually abort execution
contrib.console submodule, containing the confirm function, used for simple yes/no prompts
'''


from fabric.api import run, local, settings, abort, cd, env, lcd
from fabric.contrib.console import confirm
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


env.hosts = ['ec2-user@rhev-1']

def local():
    env.run = run
    env.local = local
    env.host_sting = 'localhost'



def host_type(message="Linux"):
    run('uname -s')
    print("System type: %s" % message)


def new_user(username, admin='no', comment="No comment provided"):
    print("New User (%s): %s, admin: %s" % (username, comment,admin))
    pass

def git_push(commit="git commit"):
    with settings(warn_only=True):
        result1 = local("git add . && git commit -m %s" % commit)
        result2 = local("git push")
        if result1.failed or result2.failed and not confirm("Tests failed. Continue anyway?"):
            abort("Aborting at user request.")

'''
Remote interactivity
fab -f fab1.py -H ec2-user@rhev-1 deploy1
'''

"""
env.put(localfile,remotefile)  sftp put
"""

def deploy1():
    code_dir = '/home/ec2-user/py-study/'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git@github.com:Dingou/Python-tools.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")

def _checkout_branch(branchname=None):
    with lcd('/srv/devops/salt/salt-master/salt'):
        local('pwd')
        try:
            local('git checkout %s' % branchname)
        except Exception:
            logging.error("No branch %s found, try to create " % branchname)
            local('git checkout -b %s' % branchname)




