#!/usr/bin/python
#{0} is the first place of the argument
import argparse

def hello(args):
    print('Hello, {0}!'.format(args.name))


def goodbye(args):
    print('Goodbye, {0}!'.format(args.name))

