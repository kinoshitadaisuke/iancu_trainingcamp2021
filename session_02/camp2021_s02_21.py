#!/usr/pkg/bin/python3.9

#
# Time-stamp: <2021/08/31 13:45:08 (CST) daisuke>
#

# definition of a function
def is_primenumber (n):
    # checking whether the number is an integer
    is_int = isinstance (n, int)
    # if the number is not an integer, then return error code
    if not (is_int):
        result = "The number given is not an integer."
        status = 0
        return (status, result)
    # checking whether the number is a prime number
    if (n < 2):
        result = "The number %d is not a prime number." % n
        status = 1
    else:
        for i in range (2, n):
            if (n % i == 0):
                result  = "%d is divisible by %d." % (n, i)
                result += " %d is not a prime number." % n
                break
            result = "The number %d is a prime number." % n
        status = 1
    # returning result
    return (status, result)

# calling a function
(status, result) = is_primenumber (100)
print ("result: %s (status code = %d)" % (result, status) )

# calling a function
(status, result) = is_primenumber (101)
print ("result: %s (status code = %d)" % (result, status) )

# calling a function
(status, result) = is_primenumber (102.3)
print ("result: %s (status code = %d)" % (result, status) )
