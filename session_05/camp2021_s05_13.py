#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/07 22:36:04 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing datetime module
import datetime

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'normalising FITS file'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
parser.add_argument ('-o', '--output', default='', help='output file name')
parser.add_argument ('file_input', nargs=1, help='input FITS file')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
file_output = args.output
file_input  = args.file_input[0]

# checking input file name
if not (file_input[-5:] == '.fits'):
    print ("Input file must be a FITS file.")
    sys.exit ()

# checking output file name
if (file_output == ''):
    print ("Output file name has to be given.")
    sys.exit ()
if not (file_output[-5:] == '.fits'):
    print ("Output file must be a FITS file.")
    sys.exit ()

# command name
command = sys.argv[0]

# date/time
now = datetime.datetime.now ().isoformat ()

# printing status
print ("#")
print ("# input file  = %s" % file_input)
print ("# output file = %s" % file_output)
print ("#")

# opening FITS file
hdu_list = astropy.io.fits.open (file_input)

# header of primary HDU
header = hdu_list[0].header

# image of primary HDU
# reading the data as float64
data = hdu_list[0].data.astype (numpy.float64)

# closing FITS file
hdu_list.close ()

# mean of pixel values
mean = numpy.mean (data)

# printing status
print ("# mean value of input file = %f" % mean)

# normalisation
data_normalised = data / mean

# adding comments to the header
header['history'] = "FITS file created by the command \"%s\"" % (command)
header['history'] = "Updated on %s" % (now)
header['comment'] = "normalisation of a FITS file"
header['comment'] = "Input file: %s" % (file_input)
header['comment'] = "Mean of pixel values of input file = %f" % (mean)

# writing a new FITS file
astropy.io.fits.writeto (file_output, data_normalised, header=header)
