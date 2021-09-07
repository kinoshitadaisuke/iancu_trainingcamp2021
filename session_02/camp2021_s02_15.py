#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 13:44:36 (CST) daisuke>
#

# importing math module
import math

# counter
i = 1

# max value
i_max = 10

# a loop using "while" statement
while (i < i_max):
    sqrt_i = math.sqrt (i)
    print ("sqrt (%d) = %f" % (i, sqrt_i) )
    i += 1
