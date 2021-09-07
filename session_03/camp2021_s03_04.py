#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 15:15:23 (CST) daisuke>
#

# importing numpy module
import numpy

# importing matplotlib module
import matplotlib
import matplotlib.figure
import matplotlib.backends.backend_agg

# output file name
file_output = 'camp2021_s03_04.png'

# x
data_x = numpy.array ( [1.2, 3.4, 5.6, 7.8, 9.0] )

# y
data_y = numpy.array ( [10.9, 8.7, 6.5, 4.3, 2.1] )

# y error
data_yerr = numpy.array ( [1.5, 1.2, 1.7, 0.8, 1.1] )

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
ax.set_xlim (0.0, 10.0)
ax.set_ylim (0.0, 15.0)
ax.errorbar (data_x, data_y, yerr=data_yerr, fmt='bo', \
             ecolor='black', capsize=5, label='data with error')
ax.legend (loc='upper right')

# saving the figure to a file
fig.savefig (file_output, dpi=225)
