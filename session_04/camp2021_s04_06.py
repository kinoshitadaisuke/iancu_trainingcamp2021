#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/01 17:55:14 (CST) daisuke>
#

# importing sqlite3 module
import sqlite3

# database file
file_db = 'solarsystem.db'

# connecting to database
conn = sqlite3.connect (file_db)

# creating a cursor
c = conn.cursor ()

# executing SQL query
sql_query  = 'select * from planet where (density > 3000 and mass > 1.0e+24)'
sql_query += ' order by density desc;'
c.execute (sql_query)

# fetching results of the query
results = c.fetchall ()

# closing connection
conn.close ()

# printing results
print ("%-12s  %10s  %10s  %10s" % ("Planet", "Mass", "Diameter", "Density") )
print ("%-12s  %10s  %10s  %10s" % ("", "(kg)", "(km)", "(kg/m^3)") )
for planet in results:
    print ("%-12s  %10g  %10.1f  %10.1f" \
           % (planet[0], planet[1], planet[2], planet[3]) )
