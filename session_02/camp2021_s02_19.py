#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 13:44:58 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# description of the program
desc = 'arithmetic operations'

# list of available operators
list_operator = ['+', '-', 'x', '/']

# construction of a parser
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('num1', type=float, nargs=1, help='number 1')
parser.add_argument ('operator', choices=list_operator, help='opeartor')
parser.add_argument ('num2', type=float, nargs=1, help='number 2')

# parsing arguments
args = parser.parse_args ()

# input parameters
num1     = args.num1[0]
num2     = args.num2[0]
operator = args.operator[0]

# calculation
if (operator == '+'):
    result = num1 + num2
elif (operator == '-'):
    result = num1 - num2
elif (operator == 'x'):
    result = num1 * num2
elif (operator == '/'):
    result = num1 / num2
else:
    print ("Something is wrong. Stopping the program.")
    sys.exit ()

# printing result
print ("%f %s %f = %f" % (num1, operator, num2, result) )
