#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/01 22:28:24 (CST) daisuke>
#

# importing modules
import sqlite3

# MPCORB file
file_mpcorb = 'mpcorb.dat'

# database file name
file_db = 'mpcorb.db'

# flag for the header
header = 'YES'

# a list for orbit data
orbit = []

# SQL commands
make_table = 'create table mpcorb ' \
    + '(name text primary key, a real, e real, i real, ' \
    + 'node real, peri real, M real, epoch text, ' \
    + 'nobs integer, nopp integer, residual real, lastobs text, ' \
    + 'absmag real, slope real)'
add_data = 'insert into mpcorb ' \
    + 'values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

# opening MPCORB file
with open (file_mpcorb, 'r') as fh:
    # reading file line-by-line
    for line in fh:
        # if we find a line starting with '-----', it is the end of the header.
        if (line[0:5] == '-----'):
            header = 'NO'
        # we skip the line starting with '-----'.
        if ( (header == 'YES') or (line[0:5] == '-----') ):
            continue
        # we stop analysing the data when reaching to an empty line.
        # after the empty line, we have data for un-numbered asteroids.
        # we focus on numbered asteroids only.
        if ( (header == 'NO') and (line == '\n') ):
            break

        # designation in packed form
        desig = line[0:7]
        # absolute magnitude
        absmag = float (line[8:13])
        # slope parameter
        slope = float (line[14:19])
        # epoch
        epoch = line[20:25]
        # mean anomaly
        M = float (line[26:35])
        # argument of perihelion
        peri = float (line[37:46])
        # longitude of ascending node
        node = float (line[48:57])
        # inclination
        i = float (line[59:68])
        # eccentricity
        e = float (line[70:79])
        # daily motion
        n = float (line[80:91])
        # semimajor axis
        a = float (line[92:103])
        # uncertainty parameter
        u = line[105:106]
        # reference
        ref = line[107:116]
        # number of observations
        nobs = int (line[117:122])
        # number of oppositions
        nopp = int (line[123:126])
        # rms residual
        residual = float (line[137:141])
        # coarse indicator of perturbers
        coase = line[142:145]
        # precise indicator of perturbers
        precise = line[146:149]
        # computer
        computer = line[150:160]
        # 4-hexdigit flags
        flag = line[161:165]
        # readable designation
        name = line[166:194]
        name = name.strip ()
        # date of last observation
        lastobs = line[194:202]

        # data to be added to table
        record = (name, a, e, i, node, peri, M, \
                  epoch, nobs, nopp, residual, lastobs, \
                  absmag, slope)
        orbit.append (record)
    
# connection to the database
conn = sqlite3.connect (file_db)
c = conn.cursor ()

# make a table
c.execute (make_table)

# add data
c.executemany (add_data, orbit)

# closing connection
conn.commit ()
conn.close ()
