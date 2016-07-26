#!/usr/bin/python

import os
import sys

dirlist = []


def search(pathname, searchname):
	if os.path.isfile(pathname) and pathname.find(searchname) >= 0:
		print pathname
		dirlist.append(pathname)
	elif os.path.isdir(pathname):
		for items in os.listdir(pathname):
			npathname = os.path.join(pathname,items)
			search(npathname,searchname)


if __name__ == "__main__":
	pathname = sys.argv[1]
	searchname = sys.argv[2]
	search(pathname,searchname)
	print dirlist


