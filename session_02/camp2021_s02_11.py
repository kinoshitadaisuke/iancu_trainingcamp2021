#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 13:44:14 (CST) daisuke>
#

# importing math module
import math

# angle in degree
a_deg = 30.0

# angle in radian
a_rad = math.radians (a_deg)

# sin (a_rad)
sin_a = math.sin (a_rad)

# printing result
print ("sin (%f deg) = %f" % (a_deg, sin_a) )

# cos (a_rad)
cos_a = math.cos (a_rad)

# printing result
print ("cos (%f deg) = %f" % (a_deg, cos_a) )

# cos (a_rad)
tan_a = math.tan (a_rad)

# printing result
print ("tan (%f deg) = %f" % (a_deg, tan_a) )

# sin^2 (a_rad) + cos^2 (a_rad)
b = math.pow (sin_a, 2) + math.pow (cos_a, 2)

# printing result
print ("sin^2 (%f deg) + cos^2 (%f deg) = %f" % (a_deg, a_deg, b) )

# calculation of atan2 (1, 1)
x = 1.0
y = 1.0
c_rad = math.atan2 (y, x)
c_deg = math.degrees (c_rad)

# printing result
print ("atan2 (%f, %f) = %f deg" % (y, x, c_deg) )
