"""
Paginate input list of records using size limit for record and batch
"""

# presumed API limits imposed by the data service
API_MAX_RECORD_SIZE_BYTES = 1048576
API_MAX_BATCH_SIZE_BYTES = 5242880
API_MAX_BATCH_SIZE_RECORDS = 500


def _sanitize(
    inlist: list,
    max_record_size: int,
    max_batch_size: int,
    max_batch_records: int,
):
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

    if not 0 < max_batch_records <= API_MAX_BATCH_SIZE_RECORDS:
        raise ValueError(
            "'max_batch_records' argument has to be int and in range [0, %d]"
            % API_MAX_BATCH_SIZE_RECORDS,
        )


def optimum(
    inlist: list,
    max_record_size: int = API_MAX_RECORD_SIZE_BYTES,
    max_batch_size: int = API_MAX_BATCH_SIZE_BYTES,
    max_batch_records: int = API_MAX_BATCH_SIZE_RECORDS,
) -> list:
    """
    Paginate input list of records using size limit for record and batch
    """
    _sanitize(inlist, max_record_size, max_batch_size, max_batch_records)

    out_batches_size = 0
    cur_batch = []
    out_batches = []

    for in_record in inlist:
        # sanitize type in place since
        if not isinstance(in_record, str):
            raise TypeError("Unsupported batch record type")

        in_record_size = len(in_record.encode("utf-8"))  # ensure char-size

        if in_record_size > max_record_size:
            print("Discarding record that exceeds record size limit")
            continue

        # test if we're still under batch size limit
        if out_batches_size + in_record_size <= max_batch_size:
            out_batches_size += in_record_size
            cur_batch.append(in_record)

            # test if current batch reached records limit
            if len(cur_batch) == max_batch_records:
                out_batches.append(cur_batch)
                cur_batch = []
        else:
            raise ValueError(
                "Total batch size exceeds maximum batch size limit"
            )

    if cur_batch:
        out_batches.append(cur_batch)

    return out_batches
