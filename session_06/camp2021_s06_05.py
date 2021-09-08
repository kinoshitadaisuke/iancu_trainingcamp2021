#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/08 22:05:41 (CST) daisuke>
#

# importing argparse module
import argparse

# importing sys module
import sys

# importing numpy module
import numpy

# importing astropy module
import astropy.io.fits
import astropy.modeling
import astropy.stats

# importing photutils module
import photutils.centroids
import photutils.aperture

# importing matplotlib module
import matplotlib.pyplot

# constructing parser object
desc = 'aperture photometry of point sources'
parser = argparse.ArgumentParser (description=desc)

# adding command-line arguments
parser.add_argument ('-f', '--fwhm', type=float, default=4.0, \
                     help='FWHM of stellar PSF in pixel (default: 4.0)')
parser.add_argument ('-a', '--aperture', type=float, default=1.5, \
                     help='aperture radius in FWHM (default: 1.5)')
parser.add_argument ('-s1', '--skyannulus1', type=float, default=3.0, \
                     help='inner sky annulus radius in FWHM (default: 3.0)')
parser.add_argument ('-s2', '--skyannulus2', type=float, default=5.0, \
                     help='outer sky annulus radius in FWHM (default: 5.0)')
parser.add_argument ('-w', '--width', type=int, default=15, \
                     help='half-width of subframe to be plotted (default: 15)')
parser.add_argument ('-x', '--xcentre', type=float, default=-1, \
                     help='x coordinate of target')
parser.add_argument ('-y', '--ycentre', type=float, default=-1, \
                     help='y coordinate of target')
parser.add_argument ('-o', '--output', default='', \
                     help='output file name')
parser.add_argument ('file', nargs=1, default='', help='input file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
fwhm_pixel            = args.fwhm
aperture_radius_fwhm  = args.aperture
skyannulus_inner_fwhm = args.skyannulus1
skyannulus_outer_fwhm = args.skyannulus2
half_width            = args.width
x_centre              = args.xcentre
y_centre              = args.ycentre
file_output           = args.output
file_fits             = args.file[0]

# aperture radii in pixel
aperture_radius_pixel  = aperture_radius_fwhm * fwhm_pixel
skyannulus_inner_pixel = skyannulus_inner_fwhm * fwhm_pixel
skyannulus_outer_pixel = skyannulus_outer_fwhm * fwhm_pixel

# checking input file name
if (file_fits == ''):
    print ("You need to specify input file name.")
    sys.exit ()
if not (file_fits[-5:] == '.fits'):
    print ("Input file must be a FITS file.")
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

# image size
image_size_x = header['NAXIS1']
image_size_y = header['NAXIS2']
    
# checking x_centre and y_centre
if not ( (x_centre >=0) and (x_centre < image_size_x) ):
    print ("Input x_centre value exceed image size.")
    sys.exit ()
if not ( (y_centre >=0) and (y_centre < image_size_y) ):
    print ("Input y_centre value exceed image size.")
    sys.exit ()
    
# reading FITS image data
data = hdu_list[0].data

# closing FITS file
hdu_list.close ()

# making subframe
x_min = int (x_centre) - half_width
x_max = int (x_centre) + half_width + 1
y_min = int (y_centre) - half_width
y_max = int (y_centre) + half_width + 1

# position of the centre
position = (x_centre, y_centre)

# making apertures (circular aperture for star and circular annulus for sky)
apphot_aperture \
    = photutils.aperture.CircularAperture (position, r=aperture_radius_pixel)
apphot_annulus \
    = photutils.aperture.CircularAnnulus (position, \
                                          r_in=skyannulus_inner_pixel, \
                                          r_out=skyannulus_outer_pixel)

# making masked data for sky annulus
skyannulus_data       = apphot_annulus.to_mask (method='center').multiply (data)
skyannulus_mask       = skyannulus_data <= 0.0
skyannulus_maskeddata = numpy.ma.array (skyannulus_data, mask=skyannulus_mask)

# sky background estimate using sigma-clipping algorithm
skybg_mean, skybg_median, skybg_stddev \
    = astropy.stats.sigma_clipped_stats (skyannulus_maskeddata, \
                                         sigma=3.0, maxiters=10, \
                                         cenfunc='median')

# sky background
skybg_per_pixel = skybg_median

# aperture photometry
noise = numpy.sqrt (data)
phot_star = photutils.aperture.aperture_photometry (data, apphot_aperture, \
                                                    error=noise)

# net flux
net_flux = phot_star['aperture_sum'] - skybg_per_pixel * apphot_aperture.area

# error of net flux
net_flux_error = phot_star['aperture_sum_err']

# printing result of aperture photometry
print ("net flux = %f +/- %f" % (net_flux, net_flux_error) )

# making masked data for sky annulus
skyannulus_data       = apphot_annulus.to_mask (method='center').multiply (data)
skyannulus_mask       = skyannulus_data <= 0.0
skyannulus_maskeddata = numpy.ma.array (skyannulus_data, mask=skyannulus_mask)

# making plot
matplotlib.pyplot.xlabel ("X [pixel]")
matplotlib.pyplot.ylabel ("Y [pixel]")
matplotlib.pyplot.xlim (x_min, x_max)
matplotlib.pyplot.ylim (y_min, y_max)
matplotlib.pyplot.imshow (data, origin='lower', vmin=0, vmax=3000)
matplotlib.pyplot.plot (x_centre, y_centre, marker='+', \
                        color='red', markersize=10)
apphot_aperture.plot (color='yellow', lw=2.0)
apphot_annulus.plot (color='green', lw=2.0)
matplotlib.pyplot.colorbar ()
matplotlib.pyplot.savefig (file_output, dpi=225)
