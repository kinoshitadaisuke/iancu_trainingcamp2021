#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/07 21:14:34 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'Checking filters used for the observation'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_filter_keyword = 'FILTER'
default_datatype_keyword = 'IMAGETYP'
parser.add_argument ('-f', '--filter', default=default_filter_keyword, \
                     help='FITS keyword for filter name')
parser.add_argument ('-t', '--type', default=default_datatype_keyword, \
                     help='FITS keyword for data type')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
filter_keyword   = args.filter
datatype_keyword = args.type
files            = args.files

# declaring a dictionary for filter names
dict_filters = {}

# processing FITS files
for fits in files:
    # if the extension of the file is not '.fits', the we skip
    if not (fits[-5:] == '.fits'):
        continue

    # opening FITS file
    hdu_list = astropy.io.fits.open (fits)

    # header of primary HDU
    header = hdu_list[0].header

    # closing FITS file
    hdu_list.close ()

    # data type
    datatype = header[datatype_keyword]

    # if the data type is not "LIGHT", the we skip the file
    if not (datatype == 'LIGHT'):
        continue

    # filter
    filter_name = header[filter_keyword]

    # if the filter name is not in the dictionary "dict_filters", then append
    # if the filter name is in the dictionary "dict_filters", then add 1
    if not (filter_name in dict_filters):
        # appending "filter_name" to the dictionary "dict_filters"
        dict_filters[filter_name] = 1
    else:
        # add 1
        dict_filters[filter_name] += 1

# printing filter list
print ("List of filters used for acquiring object frames:")
for filter_name in sorted (dict_filters.keys () ):
    print ("  %s (%d files)" % (filter_name, dict_filters[filter_name]) )
