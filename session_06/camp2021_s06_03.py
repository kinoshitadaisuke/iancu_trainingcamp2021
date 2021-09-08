#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/08 21:28:29 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits
import astropy.units
import astropy.wcs

# importing photutils module
import photutils.aperture

# importing matplotlib module
import matplotlib.pyplot

# constructing parser object
desc = 'Setting apertures'
parser = argparse.ArgumentParser (description=desc)

# adding command-line arguments
parser.add_argument ('-r', '--radius', default=10.0, \
                     help='radius of aperture circle in arcsec')
parser.add_argument ('-s', '--std', default='', help='standard star file')
parser.add_argument ('-o', '--output', default='', \
                     help='output file name')
parser.add_argument ('file', nargs=1, default='', help='input file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
radius_arcsec = args.radius
file_std      = args.std
file_output   = args.output
file_fits     = args.file[0]

# checking input file name
if (file_fits == ''):
    print ("You need to specify input file name.")
    sys.exit ()
if not (file_fits[-5:] == '.fits'):
    print ("Input file must be a FITS file.")
    sys.exit ()

# checking stdard star file
if (file_std == ''):
    print ("You need to specify input file name.")
    sys.exit ()
    
# checking output file name
if not ( (file_output[-4:] == '.eps') or (file_output[-4:] == '.pdf') \
         or (file_output[-4:] == '.png') or (file_output[-3:] == '.ps') ):
    print ("Output file must be either EPS, PDF, PNG, or PS.")
    sys.exit ()
    
# opening FITS file
hdu_list = astropy.io.fits.open (file_fits)

# reading FITS header
header = hdu_list[0].header

# WCS
wcs = astropy.wcs.WCS (header)

# reading FITS image data
data = hdu_list[0].data

# closing FITS file
hdu_list.close ()

# making empty lists
list_ra  = []
list_dec = []

# opening standard star file
with open (file_std, 'r') as fh:
    # reading file line-by-line
    for line in fh:
        # skip if the line stars with '#'
        if (line[0] == '#'):
            continue
        # splitting data
        records = line.split ()
        # RA
        ra_deg = float (records[1])
        # Dec
        dec_deg = float (records[2])
        # appending RA and Dec to lists
        list_ra.append (ra_deg)
        list_dec.append (dec_deg)

# making skycoord object
positions = astropy.coordinates.SkyCoord (list_ra, list_dec, unit='deg')

# making aperture
u_arcsec = astropy.units.arcsec
aperture_std \
    = photutils.aperture.SkyCircularAperture (positions, \
                                              r=radius_arcsec * u_arcsec)
aperture_std_pix = aperture_std.to_pixel (wcs)
        
# making plot
matplotlib.pyplot.imshow (data, origin='lower', vmin=0, vmax=1)
aperture_std_pix.plot (color='red', lw=1.0)
matplotlib.pyplot.colorbar ()
matplotlib.pyplot.savefig (file_output, dpi=225)
