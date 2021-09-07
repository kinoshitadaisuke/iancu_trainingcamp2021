#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/01 17:40:49 (CST) daisuke>
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
sql_query = 'select name from sqlite_master where type = "table";'
c.execute (sql_query)

# fetching results of the query
results = c.fetchall ()

# closing connection
conn.close ()

# printing result
print ("list of existing tables =", results)
