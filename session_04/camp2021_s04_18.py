#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/01 22:47:05 (CST) daisuke>
#

# importing modules
import sqlite3

# database file
file_db = 'mpcorb.db'

# connection to the database
conn = sqlite3.connect (file_db)
c = conn.cursor ()

# SQL command
sql_command = 'select name,a,e,a*(1.0+e),i from mpcorb ' \
    + 'where (a * (1.0 + e) > 500.0) order by (a * (1.0 + e)) desc'

# SQL query
c.execute (sql_command)

# printing results
print ("%-28s %12s %9s %12s %12s" \
       % ('Name', 'a [au]', 'e', 'Q [au]', 'i [deg]'))
print ("%s" % "-" * 77)
for obj in c.fetchall ():
    print ("%-28s %12.7f %9.7f %12.7f %12.7f" \
           % (obj[0], obj[1], obj[2], obj[3], obj[4]) )

# closing connection
conn.commit ()
conn.close ()
