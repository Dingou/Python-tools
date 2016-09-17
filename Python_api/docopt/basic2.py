#!/usr/bin/python
'''Greeter.

Usage:
  basic.py hello <name>
  basic.py goodbye <name>
  basic.py (-h | --help)

Options:
  -h --help     Show this screen.

'''

from docopt import docopt


def hello(name):
    print('Hello, {0}'.format(name))


def goodbye(name):
    print('Goodbye, {0}'.format(name))

if __name__ == '__main__':
    arguments = docopt(__doc__)
    # if an argument called hello was passed, execute the hello logic.
    if arguments['hello']:
        hello(arguments['<name>'])
    elif arguments['goodbye']:
        goodbye(arguments['<name>'])


