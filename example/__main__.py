"""
This is an example of how f_kinesis can be used to split list of data to
optimal length
"""
import sys

import optimum


DATA = ["a", "b", "cc", "ddd", "eeeee", "ffffffff", "ggggggggggggg"]

optimised_data = None

try:
    optimised_data = optimum.optimum(DATA, 13, 32)
except ValueError as err:
    print("Oh no! " + str(err))

if not optimised_data:
    print("Not OKAY")
    sys.exit(1)
else:
    for sublist in optimised_data:
        if not isinstance(sublist, list):
            print("Not OKAY")
            sys.exit(1)

print("batch:" + str(optimised_data))
