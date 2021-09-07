#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 14:44:58 (CST) daisuke>
#

# importing numpy module
import numpy

# importing matplotlib module
import matplotlib
import matplotlib.figure
import matplotlib.backends.backend_agg

# output file name
file_output = 'camp2021_s03_03.png'

# number of data points
n = 21

# range of x
x_min =  0.0
x_max = 20.0

# parameters for a straight line a*x+b
a = 2.0
b = 3.0

# x
data_x = numpy.linspace (x_min, x_max, n)

# y
data_y = a * data_x + b

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# labels
label_x = 'X [arbitrary unit]'
label_y = 'Y [arbitrary unit]'
ax.set_xlabel (label_x)
ax.set_ylabel (label_y)

# plotting a figure
ax.set_xlim (-1.0, 21.0)
ax.set_ylim (0.0, 50.0)
ax.plot (data_x, data_y, 'ro', label='data')
ax.legend (loc='upper right')

# saving the figure to a file
fig.savefig (file_output, dpi=225)
