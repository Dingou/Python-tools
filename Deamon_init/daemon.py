#!/usr/bin/python
# coding: utf-8
import os,sys,atexit,commands
import logging,time
from signal import SIGTERM

'''
Deamon Class
'''

class Daemon(object):
	def __init__(self,pidfile,logfile,logname):
		self.pidfile = pidfile
		self.logfile = logfile
		self.logname = logname

	def _set_logging(self):
		logger = logging.getLogger(self.logname)
		logger.setLevel(logging.INFO)
		event_fh = logging.FileHandler(self.logfile)
		event_fh.setLevel(logging.INFO)
		formatter = logging.Formatter('%(name)s - %(levelname)s  %(message)s')
		event_fh.setFormatter(formatter)
		logger.addHandler(event_fh)
		return logger

	def _daemonize(self):
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError, e:
			with open(self.logfile,'w+') as fp:
				fp.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))
			sys.exit(1)
		os.chdir("/")
		os.setsid()
		os.umask(0)
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError, e:
			with open(self.logfile,'w+') as fp:
				fp.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))
			sys.exit(1)
		atexit.register(self.delpid)
		pid = str(os.getpid())
		file(self.pidfile, 'w+').write('%s\n' % pid)

	def delpid(self):
		os.remove(self.pidfile)

	def start(self):
		try:
			with open(self.pidfile,'r') as start_fp:
				pid = int(start_fp.read().strip())
		except IOError:
			pid = None
		if pid:
			message = 'pidfile %s already exist. Daemon already running!\n'
			with open(self.logfile, 'w+') as start_fp:
				start_fp.write(message % self.pidfile)
			sys.exit(1)
		self._daemonize()
		self._run()

	def stop(self):
		try:
			with open(self.pidfile,'r') as stop_fp:
				pid = int(stop_fp.read().strip())
		except IOError:
			pid = None
		if not pid:
			message = 'pidfile %s does not exist. Daemon not running!\n'
			with open(self.logfile, 'w+') as stop_fp:
				stop_fp.write(message % self.pidfile)
			return
		try:
			while 1:
				os.kill(pid, SIGTERM)
				time.sleep(0.1)
		except OSError, err:
			err = str(err)
			if err.find('No such process') > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print str(err)
				sys.exit(1)

	def restart(self):
		self.stop()
		self.start()

	def _run(self):
		pass