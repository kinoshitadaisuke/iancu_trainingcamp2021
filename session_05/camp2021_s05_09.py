#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/07 22:01:08 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'listing object and flatfield frames'
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

# declaring an empty dictionary for storing FITS file information
dict_target = {}

# processing FITS files
for file_fits in files:
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
    datatype = header[datatype_keyword]
    # exptime
    exptime = header[exptime_keyword]

    # if the data type is not "LIGHT" or "FLAT", the we skip the file
    if not ( (datatype == 'LIGHT') or (datatype == 'FLAT') ):
        continue

    # filter name
    filter_name = header[filter_keyword]

    # appending file name to the dictionary
    dict_target[file_fits] = {}
    dict_target[file_fits]['filter'] = filter_name
    dict_target[file_fits]['exptime'] = exptime

# printing FITS file list
print ("List of FITS files for dark subtraction:")
for file_fits in sorted (dict_target.keys () ):
    print ("  %s (%s, %d sec)" % (file_fits, \
                                  dict_target[file_fits]['filter'],
                                  dict_target[file_fits]['exptime']) )
print ("Total number of FITS files for dark subtraction:")
print ("  %d files" % len (dict_target) )
