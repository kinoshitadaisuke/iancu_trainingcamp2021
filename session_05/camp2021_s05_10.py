#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/07 22:04:18 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing sys module
import sys

# importing datetime module
import datetime

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'carrying out dark subtraction'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_filter_keyword   = 'FILTER'
default_datatype_keyword = 'IMAGETYP'
default_exptime_keyword  = 'EXPTIME'
parser.add_argument ('-f', '--filter', default=default_filter_keyword, \
                     help='FITS keyword for filter name')
parser.add_argument ('-d', '--datatype', default=default_datatype_keyword, \
                     help='FITS keyword for data type')
parser.add_argument ('-e', '--exptime', default=default_exptime_keyword, \
                     help='FITS keyword for exposure time')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
filter_keyword   = args.filter
datatype_keyword = args.datatype
exptime_keyword  = args.exptime
files            = args.files

# command name
command = sys.argv[0]

# date/time
now = datetime.datetime.now ().isoformat ()

# declaring an empty dictionary for storing FITS file information
dict_target = {}

# processing FITS files
for file_raw in files:
    # if the extension of the file is not '.fits', the we skip
    if not (file_raw[-5:] == '.fits'):
        continue

    # opening FITS file
    hdu_list = astropy.io.fits.open (file_raw)

    # header of primary HDU
    header = hdu_list[0].header

    # closing FITS file
    hdu_list.close ()

    # data type
    datatype = header[datatype_keyword]
    # exptime
    exptime = header[exptime_keyword]

    # if the data type is not "LIGHT" or "FLAT", the we skip the file
    if not ( (datatype == 'LIGHT') or (datatype == 'FLAT') ):
        continue

    # filter name
    filter_name = header[filter_keyword]

    # appending file name to the dictionary
    dict_target[file_raw] = {}
    dict_target[file_raw]['filter'] = filter_name
    dict_target[file_raw]['exptime'] = exptime

# printing FITS file list
print ("# List of FITS files for dark subtraction:")
for file_raw in sorted (dict_target.keys () ):
    print ("#   %s (%s, %d sec)" % (file_raw, \
                                  dict_target[file_raw]['filter'],
                                  dict_target[file_raw]['exptime']) )
print ("# Total number of FITS files for dark subtraction:")
print ("#   %d files" % len (dict_target) )

# dark subtraction

print ("#")
print ("# Processing each FITS file...")
print ("#")

# processing each FITS file
for file_raw in sorted (dict_target.keys () ):
    # file names
    file_subtracted = file_raw.split ('/') [-1] [:-5] + '_d.fits'
    
    print ("# subtracting dark from %s..." % file_raw)
    print ("#   %s ==> %s" % (file_raw, file_subtracted) )
    
    
    # opening FITS file (raw data)
    hdu_list = astropy.io.fits.open (file_raw)

    # header of primary HDU
    header = hdu_list[0].header

    # printing status
    print ("#     reading raw data from \"%s\"..." % file_raw)
    
    # image of primary HDU
    # reading the data as float64
    data_raw = hdu_list[0].data.astype (numpy.float64)

    # closing FITS file
    hdu_list.close ()

    # exptime
    exptime = header[exptime_keyword]

    # dark file name
    file_dark = "dark_%04d.fits" % (int (exptime) )

    # checking whether dark file exists
    # if dark file does not exist, then stop the script
    path_dark = pathlib.Path (file_dark)
    if not (path_dark.exists () ):
        print ("The dark file \"%s\" is NOT found." % file_dark)
        print ("Check the data!")
        sys.exit ()

    # opening FITS file (dark)
    hdu_list = astropy.io.fits.open (file_dark)

    # header of primary HDU
    header_dark = hdu_list[0].header

    # checking exptime of dark frame
    exptime_dark = header_dark[exptime_keyword]

    # if exptime_dark is not the same as exptime, then stop the script
    if not (exptime == exptime_dark):
        print ("The exposure time of raw frame and dark frame are NOT same.")
        print ("Check the data!")
        sys.exit ()
    
    # printing status
    print ("#     reading dark data from \"%s\"..." % file_dark)

    # image of primary HDU
    # reading the data as float64
    data_dark = hdu_list[0].data.astype (numpy.float64)

    # closing FITS file
    hdu_list.close ()

    # printing status
    print ("#     subtracting dark from \"%s\"..." % file_raw)

    # dark subtraction
    data_subtracted = data_raw - data_dark

    # adding comments to new FITS file
    header['history'] = "FITS file created by the command \"%s\"" % (command)
    header['history'] = "Updated on %s" % (now)
    header['comment'] = "dark subtraction was carried out"
    header['comment'] = "raw data: %s" % (file_raw)
    header['comment'] = "dark data: %s" % (file_dark)
    header['comment'] = "dark subtracted data: %s" % (file_subtracted)

    # printing status
    print ("#     writing new file \"%s\"..." % file_subtracted)

    # writing a new FITS file
    astropy.io.fits.writeto (file_subtracted, data_subtracted, header=header)
