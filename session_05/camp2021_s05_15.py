#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/07 22:48:42 (CST) daisuke>
#

# importing argparse module
import argparse

# importing pathlib module
import pathlib

# importing sys module
import sys

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'listing dark subtracted object frames'
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
    # date-obs
    date_obs = header['DATE-OBS']
    # time-obs
    time_obs = header['TIME-OBS']

    # if the data type is not "LIGHT", then we skip the file
    if not (datatype == 'LIGHT'):
        continue

    # if the file name is not "*_d.fits", then we skip the file
    if not (file_fits[-7:] == '_d.fits'):
        continue

    # filter name
    filter_name = header[filter_keyword]

    # appending FITS header information to the dictionary
    if not (filter_name in dict_target):
        dict_target[filter_name] = {}
    dict_target[filter_name][file_fits] = {}
    dict_target[filter_name][file_fits]['exptime']  = exptime
    dict_target[filter_name][file_fits]['date-obs'] = date_obs
    dict_target[filter_name][file_fits]['time-obs'] = time_obs

# printing FITS file list
print ("List of FITS files for flatfielding:")
for filter_name in sorted (dict_target.keys () ):
    nflat = "nflat_%s.fits" % filter_name
    path_nflat = pathlib.Path (nflat)
    if not (path_nflat.exists () ):
        print ("The flatfield file \"%s\" does not exist." % nflat)
        print ("Check the data!")
        sys.exit ()
    print ("  %s band data:"% filter_name)
    print ("    normalised flatfield = %s" % nflat)
    for file_fits in sorted (dict_target[filter_name].keys () ):
        flatfielded = file_fits[:-5] + "f.fits"
        print ("      %s / %s" % (file_fits, nflat) )
        print ("          ==> %s" % flatfielded)
print ("Total number of files to be processed:")
total_files = 0
for filter_name in sorted (dict_target.keys () ):
    n_files = len (dict_target[filter_name].keys () )
    print ("  %s band data: %d files" % (filter_name, n_files) )
    total_files += n_files
print ("  Total number of files: %d files" % total_files)
