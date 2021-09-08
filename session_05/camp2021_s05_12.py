#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/07 22:29:21 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing datetime module
import datetime

# importing numpy module
import numpy
import numpy.ma

# importing astropy module
import astropy.io.fits
import astropy.stats

# construction of parser object
desc = 'combining flatfield frames'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
list_datatype  = ['BIAS', 'DARK', 'FLAT', 'LIGHT']
list_rejection = ['NONE', 'sigclip']
list_cenfunc   = ['mean', 'median']
parser.add_argument ('-f', '--filter', default='', help='filter name')
parser.add_argument ('-d', '--datatype', default='BIAS', \
                     choices=list_datatype, help='data type')
parser.add_argument ('-r', '--rejection', default='NONE', \
                     choices=list_rejection, \
                     help='rejection algorithm (default: NONE)')
parser.add_argument ('-t', '--threshold', type=float, default=4.0, \
                     help='threshold for sigma clipping (default: 4.0)')
parser.add_argument ('-n', '--maxiters', type=int, default=10, \
                     help='maximum number of iterations (default: 10)')
parser.add_argument ('-c', '--cenfunc', choices=list_cenfunc, \
                     default='median', \
                     help='method to estimate centre value (default: median)')
parser.add_argument ('-o', '--output', default='', help='output file name')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
filter0     = args.filter
datatype0   = args.datatype
rejection   = args.rejection
threshold   = args.threshold
maxiters    = args.maxiters
cenfunc     = args.cenfunc
file_output = args.output
list_files  = args.files

# examination of output file name
if (file_output == ''):
    print ("Output file name must be given.")
    sys.exit ()
if not (file_output[-5:] == '.fits'):
    print ("Output file must be a FITS file.")
    sys.exit ()

# command name
command = sys.argv[0]
    
# date/time
now = datetime.datetime.now ().isoformat ()

# declaring an empty dictionary for storing FITS file information
dict_target = {}

# printing information
print ("# Data search condition:")
print ("#   data type = %s" % datatype0)
print ("#   filter    = \"%s\"" % filter0)
print ("# Input parameters")
print ("#   rejection algorithm = %s" % rejection)
print ("#   threshold of sigma-clipping = %f" % threshold)
print ("#   maximum number of iterations = %d" % maxiters)

# printing status
print ("#")
print ("# Now scanning data...")

# processing FITS files
for file_fits in list_files:
    # if the extension of the file is not '.fits', the we skip
    if not (file_fits[-5:] == '.fits'):
        continue

    # opening FITS file
    hdu_list = astropy.io.fits.open (file_fits)

    # header of primary HDU
    header = hdu_list[0].header

    # closing FITS file
    hdu_list.close ()

    # data type
    datatype = header['IMAGETYP']
    # exptime
    exptime  = header['EXPTIME']
    # date-obs
    date_obs = header['DATE-OBS']
    # time-obs
    time_obs = header['TIME-OBS']

    # if the data type is not "FLAT", the we skip the file
    if not (datatype == 'FLAT'):
        continue

    # filter name
    filter_name = header['FILTER']

    # appending FITS header information to the dictionary
    if not (filter_name in dict_target):
        dict_target[filter_name] = {}
    dict_target[filter_name][file_fits] = {}
    dict_target[filter_name][file_fits]['exptime']  = exptime
    dict_target[filter_name][file_fits]['date-obs'] = date_obs
    dict_target[filter_name][file_fits]['time-obs'] = time_obs

# printing status
print ("#")
print ("# Finished scanning files")
print ("#   %d files are found for combining" \
       % len (dict_target[filter0]) )

# checking number of target files
if ( len (dict_target) < 2 ):
    print ("number of target files must be greater than 1.")
    sys.exit ()

print ("#")
print ("# Target files:")
for file_fits in dict_target[filter0]:
    print ("#   %s" % file_fits)

# counter
i = 0

# list for median pixel values
list_median = []

# printing status
print ("#")
print ("# Reading image data...")

# reading dark frames
for file_fits in dict_target[filter0]:
    # opening FITS file
    hdu_list = astropy.io.fits.open (file_fits)

    # header of primary HDU (only for the first file)
    if (i == 0):
        header = hdu_list[0].header
    
    # image of primary HDU
    # reading the data as float64
    data = hdu_list[0].data.astype (numpy.float64)

    # closing FITS file
    hdu_list.close ()

    # median pixel value of first image
    if (i == 0):
        median_ref = numpy.median (data)

    # median pixel value
    median = numpy.median (data)
    list_median.append (median)

    # scaling
    data_scaled = data / median * median_ref
    
    # constructing a data cube
    if (i == 0):
        data_tmp = data_scaled
    elif (i == 1):
        cube = numpy.concatenate ( ([data_tmp], [data_scaled]), axis=0 )
    else:
        cube = numpy.concatenate ( (cube, [data_scaled]), axis=0 )

    # incrementing "i"
    i += 1

    # printing status
    print ("#   %04d: \"%s\" (median: %8.2f ADU)" % (i + 1, file_fits, median) )
    
# printing status
print ("#")
print ("# Finished reading image data")

# printing status
print ("#")
print ("# Combining image...")

# combining flat frames
if (rejection == 'sigclip'):
    # sigma clipping
    clipped_cube = \
        astropy.stats.sigma_clip (cube, sigma=threshold, \
                                  maxiters=maxiters, cenfunc=cenfunc, \
                                  axis=0, masked=True)
    # combining using average
    combined = numpy.ma.average (clipped_cube, weights=list_median, axis=0)
elif (rejection == 'NONE'):
    # combining using average
    combined = numpy.ma.average (cube, weights=list_median, axis=0)

# printing status
print ("#")
print ("# Finished combining image")

# printing status
print ("#")
print ("# Writing image into a new FITS file...")
print ("#   output file = %s" % file_output)

# mean of combined image
mean_combined = numpy.ma.mean (combined)
    
# adding comments to the header
header['history'] = "FITS file created by the command \"%s\"" % (command)
header['history'] = "Updated on %s" % (now)
header['comment'] = "multiple FITS files are combined into a single FITS file"
header['comment'] = "List of combined files:"
for file_fits in dict_target[filter0]:
    header['comment'] = "  %s" % (file_fits)
header['comment'] = "Options given:"
header['comment'] = "  rejection = %s" % (rejection)
header['comment'] = "  threshold = %f sigma" % (threshold)
header['comment'] = "  maxiters  = %d" % (maxiters)
header['comment'] = "  cenfunc   = %s" % (cenfunc)

# writing a new FITS file
astropy.io.fits.writeto (file_output, \
                         numpy.ma.filled (combined, fill_value=mean_combined), \
                         header=header)

# printing status
print ("#")
print ("# Finished writing image into a new FITS file")
print ("#")
