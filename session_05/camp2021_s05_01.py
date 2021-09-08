#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/07 21:06:55 (CST) daisuke>
#

# importing argparse module
import argparse

# importing astropy module
import astropy.io.fits

# construction of parser object
desc = 'Generating a list of FITS files'
parser = argparse.ArgumentParser (description=desc)

# adding arguments
default_keyword = 'TIME-OBS,IMAGETYP,EXPTIME,FILTER,OBJECT'
parser.add_argument ('-k', '--keyword', default=default_keyword, \
                     help='a list of keyword to check')
parser.add_argument ('files', nargs='+', help='FITS files')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
keyword = args.keyword
files   = args.files

# a list of FITS keywords
list_keyword = keyword.split (',')

# processing FITS files
for fits in files:
    # if the extension of the file is not '.fits', the we skip
    if not (fits[-5:] == '.fits'):
        continue

    # file name
    # for example, file = '/some/where/in/the/disk/abc0123.fits'
    # then, path ==> ['some', 'where', 'in', 'the', 'disk', 'abc0123.fits']
    # filename ==> 'abc0123.fits'
    path_fits = fits.split ('/')
    filename = path_fits[-1]

    # opening FITS file
    hdu_list = astropy.io.fits.open (fits)

    # header of primary HDU
    header = hdu_list[0].header

    # closing FITS file
    hdu_list.close ()

    # gathering information from FITS header
    record = "%-24s" % filename
    for key in list_keyword:
        # obtaining a value for given keyword
        if key in header:
            value = str (header[key])
        else:
            value = "__NONE__"
        # appending the value to the string "record"
        if (key == 'DATE-OBS'):
            record += "  %-10s" % value
        elif (key == 'TIME-OBS'):
            record += "  %-8s" % value
        elif (key == 'IMAGETYP'):
            record += "  %-5s" % value
        elif (key == 'EXPTIME'):
            record += "  %6.1f" % float (value)
        elif (key == 'FILTER'):
            record += "  %-16s" % value
        else:
            record += "  %s" % value

    # printing information
    print (record)
