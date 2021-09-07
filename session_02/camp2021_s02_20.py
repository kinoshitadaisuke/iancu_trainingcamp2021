#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 13:45:03 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing pathlib module
import pathlib

# description of the program
desc = 'reading file'

# construction of a parser
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-f', default='', help='file name')
parser.add_argument ('-n', type=int, default=-1, help='number of lines to read')

# parsing arguments
args = parser.parse_args ()

# input parameters
file_input = args.f
nline      = args.n

# check of file name
if (file_input == ''):
    print ("The input file name must be given. Stopping the script.")
    sys.exit ()
path_input = pathlib.Path (file_input)
if not (path_input.exists ()):
    print ("The input file \"%s\" does not exist. Stopping the script." \
           % file_input)
    sys.exit ()
if not (path_input.is_file ()):
    print ("The input file is not a regular file. Stopping the script.")
    sys.exit ()
    
# check of nline
if (nline < 1):
    print ("A positive number must be given for number of lines to read.")
    sys.exit ()

# counter
i = 0

# opening file
with path_input.open () as fh_input:
    # reading file
    for line in fh_input:
        # printing line
        print (line, end='')
        # incrementing counter
        i += 1
        # stop reading file if enough number of lines are read
        if (i >= nline):
            break
