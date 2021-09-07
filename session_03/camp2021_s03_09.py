#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/01 10:27:10 (CST) daisuke>
#

# importing sys module
import sys

# importing argparse module
import argparse

# importing numpy array
import numpy

# importing matplotlib module
import matplotlib
import matplotlib.figure
import matplotlib.backends.backend_agg

# argument analysis
desc = 'a Python script to generate a plot of solar spectrum using Matplotlib'
parser = argparse.ArgumentParser (description=desc)
parser.add_argument ('-i', default='', help='input file name')
parser.add_argument ('-o', default='', help='output file name')
args = parser.parse_args()

# catalogue file name
file_input  = args.i
file_output = args.o

# if input file name is not give, then quit
if (file_input == ''):
    print ("You have to specify the name of input file using -i option.")
    sys.exit ()

# if output file name is not give, then quit
if (file_output == ''):
    print ("You have to specify the name of output file using -o option.")
    sys.exit ()

# making empty numpy arrays for storing data
wavelength = numpy.array ([])
flux       = numpy.array ([])

# opening catalogue file
with open (file_input, 'r') as fh:
    # reading catalogue line-by-line
    for line in fh:
        # removing line feed at the end of line
        line = line.strip ()

        # if the line is empty, the skip
        if (line == ''):
            continue

        # splitting the line
        records = line.split ()

        # skipping header
        if (records[0] == 'nm'):
            continue
        
        # conversion from string to float
        nm      = float (records[0])
        W_m2_nm = float (records[1])

        wavelength = numpy.append (wavelength, nm)
        flux       = numpy.append (flux, W_m2_nm)

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# labels
label_x = 'Wavelength [nm]'
label_y = 'Flux [W/m^2/nm]'
ax.set_xlabel (label_x)
ax.set_ylabel (label_y)

# plotting a figure
ax.set_xlim (100, 2500)
ax.plot (wavelength, flux)

# saving the figure to a file
fig.savefig (file_output, dpi=225)
