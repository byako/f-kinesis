"""
Paginate input list of strings using size limit for record and batch
"""

API_MAX_RECORD_SIZE_BYTES = 1048576
API_MAX_BATCH_SIZE_BYTES = 5242880
API_MAX_BATCH_SIZE_RECORDS = 500


def _sanitize(inlist: list, record_size: int, batch_size: int):

    if not isinstance(inlist, list):
        raise TypeError("Input parameter is not of type 'list'")

    if (
        not isinstance(batch_size, int)
        or 0 > batch_size > API_MAX_BATCH_SIZE_BYTES
    ):
        raise TypeError(
            "'batch_size' argument has to be int and in range [0, %d]"
            % API_MAX_BATCH_SIZE_BYTES,
        )

    if (
        not isinstance(record_size, int)
        or 0 > record_size > API_MAX_RECORD_SIZE_BYTES
    ):
        raise ValueError(
            "'record_size' argument has to be int and in range [0, %d]"
            % API_MAX_RECORD_SIZE_BYTES,
        )

    if record_size > batch_size:
        raise ValueError("'record_size' cannot exceed 'batch_size'")


def optimum(
    inlist: list, record_size: int = 1048576, batch_size: int = 5242880
) -> list:
    """
    Paginate input list of strings using size limit for record and batch
    """
    print("Batch size: %s, record size: %s" % (batch_size, record_size))
    print("Batch: %s" % " ,".join(inlist))
    _sanitize(inlist, record_size, batch_size)

    cur_batch_size = 0
    cur_record_size = 0
    cur_batch = []
    cur_record = []
    for instr in inlist:
        if not isinstance(instr, str):
            raise TypeError("Unsupported type of batch element")
        instr_size = len(instr.encode("utf-8"))
        if instr_size > record_size:
            raise ValueError("Batch element is too big for record size limit")
        if cur_batch_size + instr_size < batch_size:
            cur_batch_size += instr_size
            if cur_record_size + instr_size < record_size:
                cur_record.append(instr)
                cur_record_size += instr_size
            else:
                cur_batch.append(cur_record)
                cur_record = [instr]
                cur_record_size = instr_size
                if len(cur_batch) > API_MAX_BATCH_SIZE_RECORDS:
                    raise ValueError("Number of records in batch exceeded")
        else:
            raise ValueError(
                "Total batch size exceeds maximum batch size limit"
            )
    cur_batch.append(cur_record)

    return cur_batch
