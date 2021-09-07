#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 15:29:25 (CST) daisuke>
#

# importing matplotlib module
import matplotlib
import matplotlib.figure
import matplotlib.backends.backend_agg

# output file name
file_output = 'camp2021_s03_05.png'

# making objects "fig" and "ax"
fig = matplotlib.figure.Figure ()
matplotlib.backends.backend_agg.FigureCanvasAgg (fig)
ax = fig.add_subplot (111)

# labels
label_x = 'Semimajor Axis [au]'
label_y = 'Orbital Period [day]'
ax.set_xlabel (label_x)
ax.set_ylabel (label_y)

# plotting a figure
ax.set_xlim (0.1, 100.0)
ax.set_ylim (10.0, 100000.0)
ax.set_xscale ('log')
ax.set_yscale ('log')
ax.plot (0.3871,     88.0, 'bs', label='Mercury', markersize=10)
ax.plot (0.7233,    224.7, 'y^', label='Venus',   markersize=10)
ax.plot (1.0000,    365.2, 'go', label='Earth',   markersize=10)
ax.plot (1.5237,    687.0, 'rv', label='Mars',    markersize=10)
ax.plot (5.2034,   4331.0, 'ms', label='Jupiter', markersize=10)
ax.plot (9.5371,  10747.0, 'g^', label='Saturn',  markersize=10)
ax.plot (19.1913, 30589.0, 'co', label='Uranus',  markersize=10)
ax.plot (30.0690, 59800.0, 'bv', label='Neptune', markersize=10)
ax.grid ()
ax.legend (loc='upper left')

# saving the figure to a file
fig.savefig (file_output, dpi=225)
