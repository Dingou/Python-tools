#!/usr/bin/python

import os

print 'Process (%s) start' % os.getpid()

pid = os.fork()

if pid == 0:
	print "Child process (%d)." % pid
else:
	print "Parent process (%d)." % pid

