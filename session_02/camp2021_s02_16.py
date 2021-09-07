#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 13:44:41 (CST) daisuke>
#

# importing sys module
import sys

# input numbers
list_numbers = sys.argv[1:]

# a loop using for statement
for i in list_numbers:
    # conversion from string into integer
    n = int (i)
    # if the number is less than 2, then it is not a prime number
    if (n < 2):
        print ("%d is not a prime number." % n)
        continue
    # counter
    j = 2
    # prime number or not
    primenumber = 'YES'
    # a loop using while statement
    while (j < n):
        if (n % j == 0):
            primenumber = 'NO'
            break
        else:
            j += 1
    # printing result
    if (primenumber == 'YES'):
        print ("%d is a prime number." % n)
    else:
        print ("%d is not a prime number." % n)
