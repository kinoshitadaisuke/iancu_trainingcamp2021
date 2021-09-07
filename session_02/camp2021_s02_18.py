#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 13:44:54 (CST) daisuke>
#

# input file name
file_input  = 'pi.data'

# output file name
file_output = 'pi2.data'

# opening file for reading
with open (file_input, 'r') as fh_in:
    # reading whole file
    data_pi = fh_in.read ()

# opening file for writing
with open (file_output, 'w') as fh_out:
    # writing data into file
    fh_out.write (data_pi)
