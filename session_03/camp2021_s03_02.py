#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 14:28:50 (CST) daisuke>
#

# importing numpy module
import numpy

# importing matplotlib module
import matplotlib
import matplotlib.figure
import matplotlib.backends.backend_agg

# output file name
file_output = 'camp2021_s03_02.png'

# constant
pi = numpy.pi

# number of data points
n = 7201

# range of x
x_min =   0.0
x_max = 720.0

# x
data_x = numpy.linspace (x_min, x_max, n)

# y
data_y = numpy.sin (data_x / 180.0 * pi)

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# labels
label_x = 'X [deg]'
label_y = 'Y [arbitrary unit]'
ax.set_xlabel (label_x)
ax.set_ylabel (label_y)

# plotting a figure
ax.set_xlim (-5.0, 725.0)
ax.set_ylim (-1.3, +1.3)
ax.plot (data_x, data_y, '-', label='sine curve')
ax.legend (loc='upper right')

# saving the figure to a file
fig.savefig (file_output, dpi=225)
