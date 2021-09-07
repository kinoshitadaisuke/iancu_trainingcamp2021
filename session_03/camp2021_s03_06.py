#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 15:33:42 (CST) daisuke>
#

# importing numpy module
import numpy

# importing matplotlib module
import matplotlib
import matplotlib.figure
import matplotlib.backends.backend_agg

# output file name
file_output = 'camp2021_s03_06.png'

# parameters for random number generation
n         = 10**6
mean      = 100.0
stddev    = 10.0
x_min     = 50.0
x_max     = 150.0
bin_width = 5.0
bin_n     = int ( (x_max - x_min) / bin_width )  + 1

# numpy array for histogram
bins = numpy.linspace (x_min, x_max, bin_n)

# generating random numbers of Gaussian distribution
numpy.random.seed ()
data = numpy.random.normal (mean, stddev, n)

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# labels
label_x = 'X [arbitrary unit]'
label_y = 'Number of random numbers'
ax.set_xlabel (label_x)
ax.set_ylabel (label_y)

# plotting a figure
ax.set_xlim (x_min, x_max)
ax.hist (data, bins=bins, align='mid', histtype='bar', \
         linewidth=0.3, edgecolor='black', label='Gaussian distribution')
ax.legend (loc='upper right')

# saving the figure to a file
fig.savefig (file_output, dpi=225, bbox_inches="tight")
