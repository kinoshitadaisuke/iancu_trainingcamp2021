#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 13:44:32 (CST) daisuke>
#

# making a list
list_number = list (range (10))

# printing list
print (list_number)

# a loop using "for" statement
for i in list_number:
    print (i)

# adding numbers from 1 to 100
total = 0
for i in range (1, 101):
    total += i
print ("1 + 2 + 3 + ... + 98 + 99 + 100 =", total)
