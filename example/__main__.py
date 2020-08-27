"""
This is an example of how f_kinesis can be used to split list of data to
optimal length
"""
import sys

import f_kinesis


DATA = ["a", "b", "cc", "ddd", "eeeee", "ffffffff", "ggggggggggggg"]
RECORD_SIZE_LIMIT = 13
BATCH_SIZE_LIMIT = 64

optimised_data = None  # pylint: disable=invalid-name

try:
    optimised_data = f_kinesis.optimum(
        DATA, RECORD_SIZE_LIMIT, BATCH_SIZE_LIMIT
    )
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

print("source batch: " + str(DATA))
print(
    "RECORD_SIZE_LIMIT: %d, BATCH_SIZE_LIMIT: %d"
    % (RECORD_SIZE_LIMIT, BATCH_SIZE_LIMIT)
)
print("result batch: " + str(optimised_data))
