#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/08 22:12:10 (CST) daisuke>
#

# importing math module
import math

# r'-band magnitude of star ID 7
mag_star1 = 13.718

# net flux of star ID 7
flux_star1 = 112194.0

# flux error of star ID 7
err_star1 = 341.0

# net flux of star ID 13
flux_star2 = 52277.0

# flux error of star ID 13
err_star2 = 236.0

# r'-band magnitude of star ID 13
mag_star2 = mag_star1 - 2.5 * math.log10 (flux_star2 / flux_star1)

# error on magnitude
magerr_star1 = 2.5 * math.log10 (1 + err_star1 / flux_star1)
magerr_star2 = 2.5 * math.log10 (1 + err_star2 / flux_star2)
magerr_total = math.sqrt (magerr_star1**2 + magerr_star2**2)

# printing result
print ("#")
print ("# input parameters")
print ("#")
print ("#  mag_star1  = %f" % mag_star1)
print ("#  flux_star1 = %f ADU" % flux_star1)
print ("#  err_star1  = %f ADU" % err_star1)
print ("#  flux_star2 = %f ADU" % flux_star2)
print ("#  err_star2  = %f ADU" % err_star2)
print ("#")
print ("mag_star2 = %f +/- %f" % (mag_star2, magerr_total) )
