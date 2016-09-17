#!/usr/bin/python
from fabric.api import *

env.user = "django"
env.hosts=['10.1.6.186','10.1.6.159']
env.password='xxxxxx'
env.exclude_hosts=['10.1.6.159']






@hosts('host1', 'host2')
def mytask():
    run('ls /var/www')