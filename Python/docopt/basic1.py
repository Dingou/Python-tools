"""Usage: my_program.py [-hsdo FILE] [--quiet | --verbose] [INPUT ...]

-d --date    set date
-h --help    show this
-s --sorted  sorted output
-o FILE      specify output file [default: ./test.txt]
--quiet      print less text
--verbose    print more text

"""

from docopt import docopt

if __name__ == "__main__":
    arguments = docopt(__doc__,version="1.1")
    print(arguments)
    print(arguments['--help'])

#first: Usage line should include all option
# uses brackets "[ ]", parens "( )", pipes "|" and ellipsis "..." to describe optional,
# - required, mutually exclusive, and repeating elements
#


