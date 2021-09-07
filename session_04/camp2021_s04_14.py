#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/01 19:22:23 (CST) daisuke>
#

# importing sqlite3 module
import sqlite3

# database file
file_db = 'bsc5.db'

# connecting to database
conn = sqlite3.connect (file_db)

# creating a cursor
c = conn.cursor ()

# creating a table
sql_query  = 'select * from bsc where mag_v < 2.0 and colour_bv > 1.0'
sql_query += ' order by colour_bv desc;'
c.execute (sql_query)

# fetching results of the query
results = c.fetchall ()

# closing connection
conn.close ()

# printing results
print ("%-4s  %-10s  %-5s  %-5s  %-20s" \
       % ("HR", "Name", "Vmag", "B-V", "SpType") )
print ("%4s  %10s  %5s  %5s  %20s" \
       % ('-' * 4, '-' * 10, '-' * 5, '-' * 5, '-' * 20) )
for star in results:
    print ("%4d  %-10s  %+5.2f  %+5.2f  %-20s" \
           % (star[0], star[1], star[2], star[3], star[4]) )
