#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/01 21:57:31 (CST) daisuke>
#

# importing sqlite3 module
import sqlite3

# database file
file_db = 'elements.db'

# connecting to database
conn = sqlite3.connect (file_db)

# creating a cursor
c = conn.cursor ()

# creating a table
sql_query = "select * from elements where Phase = 'liq';"
c.execute (sql_query)

# fetching results of the query
results = c.fetchall ()

# closing connection
conn.close ()

# printing results
print ("%-6s %-12s %-6s %-9s %-10s %-16s %-8s %-5s" \
       % ("Number", "Name", "Symbol", "Weight", "Phase", "Type", "Density", \
          "Year") )
print ("%6s %12s %6s %9s %10s %16s %8s %5s" \
       % ('-' * 6, '-' * 12, '-' * 6, '-' * 9, '-' * 10, \
          '-' * 16, '-' * 8, '-' * 5) )
for element in results:
    print ("%6d %-12s %-6s %9.5f %-10s %-16s %8.4f %5d" \
           % (element[0], element[1], element[2], element[3], \
              element[6], element[8], element[13], element[18]) )
