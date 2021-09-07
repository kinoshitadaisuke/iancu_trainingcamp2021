#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/01 17:40:26 (CST) daisuke>
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
sql_query = 'select sql from sqlite_master where name = "planet";'
c.execute (sql_query)

# fetching results of the query
results = c.fetchall ()

# closing connection
conn.close ()

# printing result
print ("schema of table \"planet\" =", results)
