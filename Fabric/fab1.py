#!/usr/bin/python
from fabric.api import run,local
def host_type(message="Linux"):
    run('uname -s')
    print("System type: %s" % message)


def new_user(username, admin='no', comment="No comment provided"):
    print("New User (%s): %s, admin: %s" % (username, comment,admin))
    pass

def git_push(command="git commit"):
    local("git add . && git commit -m %s" % command)
    local("git push")
