#!/usr/bin/python
'''
local: run local
run: run with host

'''
from fabric.api import run,local,settings,abort

def host_type(message="Linux"):
    run('uname -s')
    print("System type: %s" % message)


def new_user(username, admin='no', comment="No comment provided"):
    print("New User (%s): %s, admin: %s" % (username, comment,admin))
    pass

def git_push(command="git commit"):
    with settings(warn_only=True):
        result1 = local("git add . && git commit -m %s" % command)
        result2 = local("git push")
        if result1.failed or result2.failed and not confirm("Tests failed. Continue anyway?"):
            abort("Aborting at user request.")

