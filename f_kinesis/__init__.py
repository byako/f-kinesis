"""
Paginate input list of strings using size limit for record and batch
"""

# presumed API limits imposed by the data service
API_MAX_RECORD_SIZE_BYTES = 1048576
API_MAX_BATCH_SIZE_BYTES = 5242880
API_MAX_BATCH_SIZE_RECORDS = 500


def _sanitize(inlist: list, max_record_size: int, max_batch_size: int):
    """
    Validate input data
    """

    if not isinstance(inlist, list):
        raise TypeError("Input parameter is not of type 'list'")

    if (not isinstance(max_record_size, int)) or (
        not 0 < max_record_size <= API_MAX_RECORD_SIZE_BYTES
    ):
        raise ValueError(
            "'max_record_size' argument has to be int and in range [0, %d]"
            % API_MAX_RECORD_SIZE_BYTES,
        )

    if (not isinstance(max_batch_size, int)) or (
        not 0 < max_batch_size <= API_MAX_BATCH_SIZE_BYTES
    ):
        raise ValueError(
            "'max_batch_size' argument has to be int and in range [0, %d]"
            % API_MAX_BATCH_SIZE_BYTES,
        )

    if max_record_size > max_batch_size:
        raise ValueError("'max_record_size' cannot exceed 'max_batch_size'")


def optimum(
    inlist: list, max_record_size: int = 1048576, max_batch_size: int = 5242880
) -> list:
    """
    Paginate input list of strings using size limit for record and batch
    """
    _sanitize(inlist, max_record_size, max_batch_size)

    cur_batch_size = 0
    cur_record_size = 0
    cur_batch = []
    cur_record = []

    for instr in inlist:
        # sanitize type in place since
        if not isinstance(instr, str):
            raise TypeError("Unsupported type of batch element")

        instr_size = len(instr.encode("utf-8"))  # ensure char-size

        # fail if single string is more than a blank record can take
        if instr_size > max_record_size:
            raise ValueError("Batch element is too big for record size limit")

        # test if we're still under API batch size limit
        if cur_batch_size + instr_size <= max_batch_size:
            cur_batch_size += instr_size

            # test if current string fits into record size limit
            if cur_record_size + instr_size <= max_record_size:
                cur_record.append(instr)
                cur_record_size += instr_size
            else:  # record limit would be exceeded, get new record
                cur_batch.append(cur_record)
                cur_record = [instr]
                cur_record_size = instr_size
                # ensure API records number in batch will not be exceeded
                if len(cur_batch) >= API_MAX_BATCH_SIZE_RECORDS:
                    raise ValueError("Number of records in batch exceeded")
        else:
            raise ValueError(
                "Total batch size exceeds maximum batch size limit"
            )

    # last batch already counted with inclusive comparison condition
    cur_batch.append(cur_record)

    return cur_batch
