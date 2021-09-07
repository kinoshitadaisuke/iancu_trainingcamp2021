#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 20:26:08 (CST) daisuke>
#

# importing sys module
import sys

# importing argparse module
import argparse

# importing numpy module
import numpy

# importing matplotlib module
import matplotlib
import matplotlib.figure
import matplotlib.backends.backend_agg
import matplotlib.dates

# importing datetime
import datetime

# argument analysis
desc = 'a Python script to make lightcurve using Matplotlib'
parser = argparse.ArgumentParser (description=desc)
parser.add_argument ('-i', default='', help='input file name')
parser.add_argument ('-o', default='', help='output file name')
args = parser.parse_args()

# output file name
file_input  = args.i
file_output = args.o

# if input file name is not given, then quit
if (file_input == ''):
    print ("You have to specify the name of input file using -i option.")
    sys.exit ()

# if output file name is not given, then quit
if (file_output == ''):
    print ("You have to specify the name of output file using -o option.")
    sys.exit ()

# making empty list and Numpy arrays
data_date  = numpy.array ([], dtype='datetime64[ms]')
data_mag   = numpy.array ([], dtype='float64')
data_error = numpy.array ([], dtype='float64')
    
# opening input file
with open (file_input, 'r') as fh_in:
    # reading data line-by-line
    for line in fh_in:
        # splitting data
        (date_str, mag_str, error_str, band, observer) = line.split ()
        # conversion from string to datetime, and then to datetime64
        date1 = datetime.datetime.strptime (date_str[:-4], '%Y-%m-%d')
        day   = float (date_str[-3:]) / 1000
        date2 = datetime.timedelta (days=day)
        date_datetime = date1 + date2
        date_datetime64 = numpy.datetime64 (date_datetime, 'ms')
        # conversion from string to float
        mag = float (mag_str)
        error = float (error_str)
        # appending data to list and Numpy arrays
        data_date  = numpy.append (data_date, date_datetime64)
        data_mag   = numpy.append (data_mag, mag)
        data_error = numpy.append (data_error, error)

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# labels
label_x = 'Date [YYYY-MM-DD]'
label_y = 'V-band Magnitude [mag]'
ax.set_xlabel (label_x)
ax.set_ylabel (label_y)

# range of x and y axes
x_min = numpy.datetime64 ('2019-12-20')
x_max = numpy.datetime64 ('2020-04-01')
y_min = +1.9
y_max = +0.9

# axis settings
ax.set_xlim (x_min, x_max)
ax.set_ylim (y_min, y_max)

# plotting data
ax.plot (data_date, data_mag, 'ro', markersize=5, label='Betelgeuse')
ax.legend (loc='upper right')

# formatting labels
fig.autofmt_xdate()

# saving the figure to a file
fig.savefig (file_output, dpi=225)
