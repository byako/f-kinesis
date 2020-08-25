"""
Paginate input list of strings using size limit for page and batch
"""

API_MAX_PAGE_SIZE_BYTES = 1048576
API_MAX_BATCH_SIZE_BYTES = 5242880


def _sanitize(
    inlist: list, page_size: int, batch_size: int
):

    if not isinstance(inlist, list):
        raise Exception("Input parameter is not of type 'list'")

    if (
        not isinstance(batch_size, int)
        or 0 > batch_size > API_MAX_BATCH_SIZE_BYTES
    ):
        raise Exception(
            "'batch_size' argument has to be int and in range [0, %d]" %
            API_MAX_BATCH_SIZE_BYTES,
        )

    if (
        not isinstance(page_size, int)
        or 0 > page_size > API_MAX_PAGE_SIZE_BYTES
    ):
        raise ValueError(
            "'page_size' argument has to be int and in range [0, %d]" %
            API_MAX_PAGE_SIZE_BYTES,
        )

    if page_size > batch_size:
        raise ValueError("'page_size' cannot exceed 'batch_size'")


def optimum(
    inlist: list, page_size: int = 1048576, batch_size: int = 5242880
) -> list:
    """
    Paginate input list of strings using size limit for page and batch
    """
    print("Batch size: %s, page size: %s" % (batch_size, page_size))
    print("Batch: %s" % " ,".join(inlist))
    _sanitize(inlist, page_size, batch_size)

    cur_batch_size = 0
    cur_page_size = 0
    cur_batch = []
    cur_page = []
    for instr in inlist:
        if not isinstance(instr, str):
            raise ValueError("Unsupported type of list element")
        instr_size = len(instr.encode('utf-8'))
        if instr_size > page_size:
            raise ValueError("Batch element is too big for page size limit")
        if cur_batch_size + instr_size < batch_size:
            cur_batch_size += instr_size
            if cur_page_size + instr_size < page_size:
                cur_page.append(instr)
                cur_page_size += instr_size
            else:
                cur_batch.append(cur_page)
                cur_page = [instr]
                cur_page_size = instr_size
        else:
            raise ValueError(
                "Total batch size exceeds maximum batch size limit"
            )
    cur_batch.append(cur_page)

    return cur_batch
