#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/01 18:56:05 (CST) daisuke>
#

# importing sqlite3 module
import sqlite3

# catalogue file
file_catalogue = 'bsc5.data'

# database file
file_db = 'bsc5.db'

# connecting to database
conn = sqlite3.connect (file_db)

# creating a cursor
c = conn.cursor ()

# creating a table
sql_table  = 'create table bsc (hr integer primary key, name text,'
sql_table += ' mag_v real, colour_bv real, sptype text);'
c.execute (sql_table)

# opening file
with open (file_catalogue, 'r') as fh:
    # reading the catalogue file line-by-line
    for line in fh:
        # Harvard Revised Number
        HR = int (line[0:4])
        # name
        name = line[4:14].strip ()
        if (name == ''):
            name = '___NONE___'
        # RA (J2000)
        RAh = line[75:77].strip ()
        if (RAh == ''):
            continue
        # visual magnitude
        Vmag = float (line[102:107])
        # (B-V) colour index
        BV = line[109:114].strip ()
        if (BV == ''):
            BV = -99.99
        else:
            BV = float (BV)
        # SpType
        SpType = line[127:147].strip ()
        if (SpType == ''):
            SpType = '___NONE___'

        # adding data
        sql_adddata = "insert into bsc values (%d, \"%s\", %f, %f, \"%s\")" \
            % (HR, name, Vmag, BV, SpType)
        c.execute (sql_adddata)

# saving the data
conn.commit ()

# closing connection
conn.close ()
