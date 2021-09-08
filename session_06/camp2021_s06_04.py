#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/08 21:57:39 (CST) daisuke>
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

# importing photutils module
import photutils.centroids

# importing matplotlib module
import matplotlib.figure
import matplotlib.backends.backend_agg

# constructing parser object
desc = 'PSF fitting'
parser = argparse.ArgumentParser (description=desc)

# adding command-line arguments
list_psf = ['2dg', '2dm']
parser.add_argument ('-p', '--psf', choices=list_psf, default='2dg', \
                     help='PSF model [2dg=Gaussian, 2dm=Moffat] (default: 2dg)')
parser.add_argument ('-w', '--width', type=int, default=5, \
                     help='half-width of centroid calculation box (default: 5)')
parser.add_argument ('-x', '--xinit', type=int, default=-1, \
                     help='a rough x coordinate of target')
parser.add_argument ('-y', '--yinit', type=int, default=-1, \
                     help='a rough y coordinate of target')
parser.add_argument ('-o', '--output', default='psffitting.png', \
                     help='output file name')
parser.add_argument ('file', nargs=1, default='', help='input file name')

# command-line argument analysis
args = parser.parse_args ()

# input parameters
psf_model   = args.psf
half_width  = args.width
x_init      = args.xinit
y_init      = args.yinit
file_fits   = args.file[0]
file_output = args.output

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
    print ("Output file must be EPS or PDF or PNG or PS.")
    sys.exit ()

# opening FITS file
hdu_list = astropy.io.fits.open (file_fits)

# reading FITS header
header = hdu_list[0].header

# image size
image_size_x = header['NAXIS1']
image_size_y = header['NAXIS2']
    
# checking x_init and y_init
if not ( (x_init >=0) and (x_init < image_size_x) ):
    print ("Input x_init value exceed image size.")
    sys.exit ()
if not ( (y_init >=0) and (y_init < image_size_y) ):
    print ("Input y_init value exceed image size.")
    sys.exit ()
    
# reading FITS image data
data = hdu_list[0].data

# closing FITS file
hdu_list.close ()

# region of calculation
x_min = x_init - half_width
x_max = x_init + half_width + 1
y_min = y_init - half_width
y_max = y_init + half_width + 1

# extraction of subframe for calculation
subframe = data[y_min:y_max, x_min:x_max]

# rough background subtraction
subframe -= numpy.median (subframe)

# centroid measurement
(xc_com, yc_com) = photutils.centroids.centroid_com (subframe)

# PSF fitting
subframe_y, subframe_x = numpy.indices (subframe.shape)
if (psf_model == '2dg'):
    psf_init = astropy.modeling.models.Gaussian2D (x_mean=xc_com, y_mean=yc_com)
elif (psf_model == '2dm'):
    psf_init = astropy.modeling.models.Moffat2D (x_0=xc_com, y_0=yc_com)
fit = astropy.modeling.fitting.LevMarLSQFitter ()
psf_fitted = fit (psf_init, subframe_x, subframe_y, subframe, maxiter=1000)

# result of fitting
if (psf_model == '2dg'):
    x_centre     = psf_fitted.x_mean.value
    y_centre     = psf_fitted.y_mean.value
    theta        = psf_fitted.theta.value
    x_fwhm       = psf_fitted.x_fwhm
    y_fwhm       = psf_fitted.y_fwhm
    fwhm         = (x_fwhm + y_fwhm) / 2.0
elif (psf_model == '2dm'):
    x_centre     = psf_fitted.x_0.value
    y_centre     = psf_fitted.y_0.value
    alpha        = psf_fitted.alpha.value
    gamma        = psf_fitted.gamma.value
    fwhm         = psf_fitted.fwhm
amplitude    = psf_fitted.amplitude.value
x_centre_sub = x_centre
y_centre_sub = y_centre
x_centre    += x_min
y_centre    += y_min

# printing information
print ("#")
print ("# input file name = %s" % file_fits)
print ("# half-width of search box = %f" % half_width)
print ("# x_init = %f" % x_init)
print ("# y_init = %f" % y_init)
print ("#")
print ("# result")
print ("#  x_centre  = %f" % x_centre)
print ("#  y_centre  = %f" % y_centre)
print ("#  amplitude = %f" % amplitude)
if (psf_model == '2dg'):
    print ("#  theta     = %f" % theta)
    print ("#  x_fwhm    = %f" % x_fwhm)
    print ("#  y_fwhm    = %f" % y_fwhm)
elif (psf_model == '2dm'):
    print ("#  alpha     = %f" % alpha)
    print ("#  gamma     = %f" % gamma)
    print ("#  fwhm      = %f" % fwhm)
print ("#")

# printing result
print ("# X_CENTRE, Y_CENTRE, FWHM")
print ("%f %f %f" % (x_centre, y_centre, fwhm) )

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# axes
ax.set_xlabel ("X - %d [pixel]" % x_min)
ax.set_ylabel ("Y - %d [pixel]" % y_min)

# plotting image
im = ax.imshow (subframe, origin='lower')
fig.colorbar (im)
ax.plot (x_centre_sub, y_centre_sub, marker='+', color='red', markersize=10)

# saving file
fig.savefig (file_output, dpi=225)
