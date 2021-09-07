#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 13:44:22 (CST) daisuke>
#

# making a list
list_a = [1, 3, 5, 7, 9]

# printing list
print ("list_a =", list_a)

# accessing an element using index
# list_a[0] is the value of first element of the list "list_a"
print ("list_a[0] =", list_a[0])

# list_a[2] is the value of third element of the list "list_a"
print ("list_a[2] =", list_a[2])

# list_a[-1] is the value of last element of the list "list_a"
print ("list_a[-1] =", list_a[-1])

# accessing elements using slicing
print ("list_a[1:3] =", list_a[1:3])

# number of elements in the list
n = len (list_a)
print ("number of elements =", n)

# adding one more element to the list
list_a.append (6)

# printing list
print ("list_a =", list_a)

# number of elements in the list
n = len (list_a)
print ("number of elements =", n)

# adding some more elements to the list
list_a.extend ([-1, 8, 4])

# printing list
print ("list_a =", list_a)

# number of elements in the list
n = len (list_a)
print ("number of elements =", n)

# printing list
print ("list_a =", list_a)

# sorting list
list_b = sorted (list_a)

# printing list
print ("list_b =", list_b)
