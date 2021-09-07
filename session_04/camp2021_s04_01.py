#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/09/01 16:25:41 (CST) daisuke>
#

# importing sqlite3 module
import sqlite3

# database file
file_db = 'solarsystem.db'

# connecting to database
conn = sqlite3.connect (file_db)

# creating a cursor
c = conn.cursor ()

# creating a table
sql_table = 'create table planet (name text primary key, mass real, '
sql_table += 'diameter real, density real);'
c.execute (sql_table)

# adding data
c.execute ("insert into planet values ('Mercury', 3.30E23,   4879, 5427);")
c.execute ("insert into planet values ('Venus',   4.87E24,  12104, 5243);")
c.execute ("insert into planet values ('Earth',   5.97E24,  12756, 5514);")
c.execute ("insert into planet values ('Mars',    6.42E23,   6792, 3933);")
c.execute ("insert into planet values ('Jupiter', 1.90E27, 142984, 1326);")
c.execute ("insert into planet values ('Saturn',  5.68E26, 120536,  687);")
c.execute ("insert into planet values ('Uranus',  8.68E25,  51118, 1271);")
c.execute ("insert into planet values ('Neptune', 1.02E26,  49528, 1638);")

# saving the data
conn.commit ()

# closing connection
conn.close ()
