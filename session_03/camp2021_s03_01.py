#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 13:45:30 (CST) daisuke>
#

# importing numpy module
import numpy

# constant
pi = numpy.pi
print ("pi =", pi)

# number of data points
n = 13

# range of x
x_min =   0.0
x_max = 360.0

# x
data_x = numpy.linspace (x_min, x_max, n)
print (data_x)

# y
data_y = numpy.sin (data_x / 180.0 * pi)
print (data_y)

# printing sine curve
for i in range ( len (data_x) ):
    print ("x = %5.1f deg ==> sin(x) = %5.3f" % (data_x[i], data_y[i]) )
