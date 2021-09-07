#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/01 22:39:09 (CST) daisuke>
#

# importing modules
import sqlite3

# database file
file_db = 'mpcorb.db'

# connection to the database
conn = sqlite3.connect (file_db)
c = conn.cursor ()

# SQL command
sql_command = 'select name,a,e,i,absmag,nobs from mpcorb' \
    + ' where absmag < 3.5 order by absmag'

# SQL query
c.execute (sql_command)

# printing results
print ("%-28s %11s %9s %9s %6s %5s" \
       % ('Name', 'a [au]', 'e', 'i [deg]', 'absmag', 'nobs'))
print ("%s" % "-" * 73)
for obj in c.fetchall ():
    print ("%-28s %11.7f %9.7f %9.5f %6.1f %5d" \
           % (obj[0], obj[1], obj[2], obj[3], obj[4], obj[5]) )

# closing connection
conn.commit ()
conn.close ()
