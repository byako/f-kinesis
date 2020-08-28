"""
Unite tests for f_kinesis
"""
import re
import pytest
import f_kinesis


@pytest.mark.parametrize("batch", [None, 1, {}, set(), object()])
def test_fail_inlist_not_list(batch):
    """
    TypeError is raised if input batch is not list
    """
    with pytest.raises(
        TypeError, match="Input parameter is not of type 'list'"
    ):
        f_kinesis.optimum(batch)


@pytest.mark.parametrize("batch_inner", [None, 1, {}, set(), object()])
def test_fail_str_not_str(batch_inner):
    """
    TypeError is raised if any batch element is not str
    """
    batch = [batch_inner]
    with pytest.raises(TypeError, match="Unsupported type of batch element"):
        f_kinesis.optimum(batch)


@pytest.mark.parametrize(
    "max_record_size", [-10, 0, f_kinesis.API_MAX_RECORD_SIZE_BYTES + 1]
)
def test_fail_wrong_record_size_param(max_record_size):
    """
    ValueError is raised for unsupported record size parameter value
    """
    batch = ["foo"]
    with pytest.raises(
        ValueError,
        match=re.escape(
            "'max_record_size' argument has to be int and in range [0, %s]"
            % f_kinesis.API_MAX_RECORD_SIZE_BYTES
        ),
    ):
        f_kinesis.optimum(
            batch,
            max_record_size,
            f_kinesis.API_MAX_BATCH_SIZE_BYTES,
        )


@pytest.mark.parametrize(
    "max_batch_size", [-10, 0, f_kinesis.API_MAX_BATCH_SIZE_BYTES + 1]
)
def test_fail_wrong_batch_size_param(max_batch_size):
    """
    ValueError is raised for unsupported batch size parameter value
    """
    batch = ["foo"]
    with pytest.raises(
        ValueError,
        match=re.escape(
            "'max_batch_size' argument has to be int and in range [0, %s]"
            % f_kinesis.API_MAX_BATCH_SIZE_BYTES
        ),
    ):
        f_kinesis.optimum(
            batch,
            f_kinesis.API_MAX_RECORD_SIZE_BYTES,
            max_batch_size,
        )


def test_fail_record_size_param_value_exceeds_batch_size_param_value():
    """
    ValueError is raised if max_record_size param value is bigger than
    max_batch_size param value
    """
    with pytest.raises(
        ValueError,
        match=re.escape("'max_record_size' cannot exceed 'max_batch_size'"),
    ):
        f_kinesis.optimum(
            ["one"],
            f_kinesis.API_MAX_RECORD_SIZE_BYTES,
            f_kinesis.API_MAX_RECORD_SIZE_BYTES - 5,
        )


def test_fail_if_any_string_is_bigger_than_record_size():
    """
    ValueError is raised if any string in batch is bigger than max_record_size
    """
    with pytest.raises(
        ValueError,
        match=re.escape("Batch element is too big for record size limit"),
    ):
        f_kinesis.optimum(["12345678901"], 10)


def test_record_size_limit_reached_ok():
    """
    ValueError is not raised if any string is same size as record size limit
    """
    batch = ["a" * f_kinesis.API_MAX_RECORD_SIZE_BYTES]

    result = f_kinesis.optimum(batch)
    print(result)
    assert len(result) == 1
    assert len(result[0]) == 1
    assert len(result[0][0]) == len(batch[0])


def test_api_batch_records_number_limit_exceeded_fail():
    """
    ValueError is raised if resulting batch ends up having too many records
    """
    batch = ["a"] * (f_kinesis.API_MAX_BATCH_SIZE_RECORDS + 1)

    with pytest.raises(
        ValueError,
        match=re.escape("Number of records in batch exceeded"),
    ):
        f_kinesis.optimum(batch, 1)


def test_api_batch_records_number_limit_reached_ok():
    """
    ValueError is not raised if batch records number limit reached
    """
    batch = ["a"] * f_kinesis.API_MAX_BATCH_SIZE_RECORDS

    result = f_kinesis.optimum(batch, 1)
    assert len(result) == f_kinesis.API_MAX_BATCH_SIZE_RECORDS


def test_batch_size_limit_exceed_fail():
    """
    ValueError is raised if resulting batch exceeds batch size limit
    """
    batch = ["one", "two", "three", "four"]

    with pytest.raises(
        ValueError,
        match=re.escape("Total batch size exceeds maximum batch size limit"),
    ):
        f_kinesis.optimum(batch, 5, 10)


def test_batch_size_limit_reached_ok():
    """
    ValueError is not raised if batch size limit reached
    """
    batch = ["a"] * 10

    result = f_kinesis.optimum(batch, 5, 10)
    assert len(result) == 2
    assert len(result[0]) == len(result[1]) == 5


def test_unicode_record_size_limit_exceeded_fail():
    """
    ValueError is raised if record size limit exceeded with unicode
    """
    batch = ["\u0391\u0392\u0394\u0395\u0396"]  # 10 bytes

    with pytest.raises(
        ValueError,
        match=re.escape("Batch element is too big for record size limit"),
    ):
        f_kinesis.optimum(batch, 8, 16)


def test_ok_same_order():
    """
    TypeError is raised if input batch is not list
    """
    batch = ["a", "b", "cc", "ddd", "eeeee", "ffffffff", "ggggggggggggg"]
    optimal_batch = f_kinesis.optimum(batch)
    assert len(optimal_batch) == 1
    assert len(optimal_batch[0]) == len(batch)
    for idx, value in enumerate(batch):
        assert value == optimal_batch[0][idx]
