#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/07 22:27:02 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'listing dark-subtracted flatfield frames'
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

    # if the data type is not "FLAT", the we skip the file
    if not (datatype == 'FLAT'):
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
print ("List of FITS files for constructing combined flatfield:")
for filter_name in sorted (dict_target.keys () ):
    print ("  %s band flatfield:"% filter_name)
    for file_fits in sorted (dict_target[filter_name].keys () ):
        print ("    %s (%d sec data taken at %s on %s)" \
               % (file_fits, dict_target[filter_name][file_fits]['exptime'], \
                  dict_target[filter_name][file_fits]['time-obs'], \
                  dict_target[filter_name][file_fits]['date-obs']) )
