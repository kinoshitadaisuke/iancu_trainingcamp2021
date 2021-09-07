#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 13:44:04 (CST) daisuke>
#

# importing math module
import math

# pi
pi = math.pi

# angle in degree
a_deg = 180.0

# conversion from degree to radian
a_rad = math.radians (a_deg)

# printing result
print ("%12.8f deg = %12.10f rad" % (a_deg, a_rad) )

# angle in radian
b_rad = pi / 6

# conversion from radian to degree
b_deg = math.degrees (b_rad)

# printing result
print ("%12.10f rad = %12.8f deg" % (b_rad, b_deg) )
