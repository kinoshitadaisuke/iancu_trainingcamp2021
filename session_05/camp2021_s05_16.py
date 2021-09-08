#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/07 22:51:30 (CST) daisuke>
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
desc = 'carrying out flatfielding'
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
for file_darksub in files:
    # if the extension of the file is not '.fits', the we skip
    if not (file_darksub[-5:] == '.fits'):
        continue

    # opening FITS file
    hdu_list = astropy.io.fits.open (file_darksub)

    # header of primary HDU
    header = hdu_list[0].header

    # closing FITS file
    hdu_list.close ()

    # data type
    datatype = header[datatype_keyword]
    # exptime
    exptime = header[exptime_keyword]

    # if the data type is not "LIGHT", then we skip the file
    if not (datatype == 'LIGHT'):
        continue

    # if the file name is not "*_d.fits", then we skip the file
    if not (file_darksub[-7:] == '_d.fits'):
        continue

    # filter name
    filter_name = header[filter_keyword]

    # appending file name to the dictionary
    dict_target[file_darksub] = {}
    dict_target[file_darksub]['filter'] = filter_name
    dict_target[file_darksub]['exptime'] = exptime

# dark subtraction

print ("#")
print ("# Processing each FITS file...")
print ("#")

# processing each FITS file
for file_darksub in sorted (dict_target.keys () ):
    # file names
    file_flatfielded = file_darksub.split ('/') [-1] [:-5] + 'f.fits'
    file_nflat = 'nflat_' + dict_target[file_darksub]['filter'] + '.fits'

    # if normalised flatfield does not exist, then stop the script
    path_nflat = pathlib.Path (file_nflat)
    if not (path_nflat.exists () ):
        print ("The flatfield file \"%s\" does not exist." % file_nflat)
        print ("Check the data!")
        sys.exit ()
    
    print ("# dividing %s by %s..." % (file_darksub, file_nflat) )
    print ("#   %s ==> %s" % (file_darksub, file_flatfielded) )
    
    # opening FITS file (raw data)
    hdu_list = astropy.io.fits.open (file_darksub)

    # header of primary HDU
    header = hdu_list[0].header

    # printing status
    print ("#     reading dark-subtracted data from \"%s\"..." % file_darksub)
    
    # image of primary HDU
    # reading the data as float64
    data_darksub = hdu_list[0].data.astype (numpy.float64)

    # closing FITS file
    hdu_list.close ()

    # opening FITS file (nflat)
    hdu_list = astropy.io.fits.open (file_nflat)

    # header of primary HDU
    header_nflat = hdu_list[0].header

    # printing status
    print ("#     reading normalised flatfield data from \"%s\"..." \
           % file_nflat)

    # image of primary HDU
    # reading the data as float64
    data_nflat = hdu_list[0].data.astype (numpy.float64)

    # closing FITS file
    hdu_list.close ()

    # printing status
    print ("#     dividing \"%s\" by \"%s\"..." % (file_darksub, file_nflat) )

    # flatfielding
    data_flatfielded = data_darksub / data_nflat

    # adding comments to new FITS file
    header['history'] = "FITS file created by the command \"%s\"" % (command)
    header['history'] = "Updated on %s" % (now)
    header['comment'] = "flatfielding was carried out"
    header['comment'] = "dark-subtracted data: %s" % (file_darksub)
    header['comment'] = "normalised flatfield data: %s" % (file_nflat)
    header['comment'] = "flatfielded data: %s" % (file_flatfielded)

    # printing status
    print ("#     writing new file \"%s\"..." % file_flatfielded)

    # writing a new FITS file
    astropy.io.fits.writeto (file_flatfielded, data_flatfielded, header=header)
