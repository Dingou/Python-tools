# !/usr/bin/python
#https://realpython.com/blog/python/comparing-python-command-line-parsing-libraries-argparse-docopt-click/
import argparse

# prog - The name of the program (default: sys.argv[0])
# usage - The string describing the program usage (default: generated from arguments added to parser)
# description - Text to display before the argument help (default: none)
# epilog - Text to display after the argument help (default: none)
# parents - A list of ArgumentParser objects whose arguments should also be included
# formatter_class - A class for customizing the help output
# prefix_chars - The set of characters that prefix optional arguments (default: ‘-‘)
# fromfile_prefix_chars - The set of characters that prefix files from which additional arguments should be read (default: None)
# argument_default - The global default value for arguments (default: None)
# conflict_handler - The strategy for resolving conflicting optionals (usually unnecessary)
# add_help - Add a -h/–help option to the parser (default: True)
# allow_abbrev - Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
# Changed in version 3.5: allow_abbrev parameter was added.


# The first step in using the argparse is creating an ArgumentParser object:


parser = argparse.ArgumentParser(description='Process some integers.')

# ArgumentParser parses arguments through the parse_args()


#name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
#action - The basic type of action to be taken when this argument is encountered at the command line.
#nargs - The number of command-line arguments that should be consumed.
#const - A constant value required by some action and nargs selections.
#default - The value produced if the argument is absent from the command line.
#type - The type to which the command-line argument should be converted.
#choices - A container of the allowable values for the argument.
#required - Whether or not the command-line option may be omitted (optionals only).
#help - A brief description of what the argument does.
#metavar - A name for the argument in usage messages.
#dest - The name of the attribute to be added to the object returned by parse_args().


#subparsers

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--foo', action='store_true', help='foo help')
subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "a" command
parser_a = subparsers.add_parser('a', help='a help')
parser_a.add_argument('bar', type=int, help='bar help')

# create the parser for the "b" command
parser_b = subparsers.add_parser('b', help='b help')
parser_b.add_argument('--baz', choices='XYZ', help='baz help')

# parse some argument lists
parser.parse_args(['a', '12'])

parser.parse_args(['--foo', 'b', '--baz', 'Z'])


