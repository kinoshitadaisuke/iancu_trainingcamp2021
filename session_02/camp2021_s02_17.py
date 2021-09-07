#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 13:44:47 (CST) daisuke>
#

# file name
file_pi = 'pi.data'

# opening file
with open (file_pi, 'r') as fh:
    # counter
    i = 0
    # reading file line-by-line
    for line in fh:
        # removing last character which should be line feed
        line = line.strip ()
        # printing line
        print (line)
        # incrementing the counter
        i += 1
        # stop reading the file, after reading 10 lines
        if (i >= 10):
            break
