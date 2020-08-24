"""
Paginate input list of strings using size limit for page and batch
"""


def optimum(
    inlist: list, batch_size: int = 5242880, page_size: int = 1048576
) -> list:
    """
    Paginate input list of strings using size limit for page and batch
    """

    print("Batch size: %s, page size: %s" % (batch_size, page_size))
    print("Batch: %s" % " ,".join(inlist))
    return inlist
