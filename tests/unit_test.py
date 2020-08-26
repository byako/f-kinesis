"""
Unite tests for f_kinesis
"""
import re
import pytest
import f_kinesis


@pytest.mark.parametrize("batch", [None, 1, {}, set(), object()])
def test_fail_not_list(batch):
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
    "record_size", [-10, 0, f_kinesis.API_MAX_RECORD_SIZE_BYTES + 1]
)
def test_fail_exceed_record_size(record_size):
    """
    ValueError is raised for unsupported record size
    """
    batch = ["foo"]
    with pytest.raises(
        ValueError,
        match=re.escape(
            "'record_size' argument has to be int and in range [0, %s]"
            % f_kinesis.API_MAX_RECORD_SIZE_BYTES
        ),
    ):
        f_kinesis.optimum(
            batch,
            record_size,
            f_kinesis.API_MAX_BATCH_SIZE_BYTES,
        )


@pytest.mark.parametrize(
    "batch_size", [-10, 0, f_kinesis.API_MAX_BATCH_SIZE_BYTES + 1]
)
def test_fail_exceed_batch_size(batch_size):
    """
    ValueError is raised for unsupported batch size
    """
    batch = ["foo"]
    with pytest.raises(
        ValueError,
        match=re.escape(
            "'batch_size' argument has to be int and in range [0, %s]"
            % f_kinesis.API_MAX_BATCH_SIZE_BYTES
        ),
    ):
        f_kinesis.optimum(
            batch,
            f_kinesis.API_MAX_RECORD_SIZE_BYTES,
            batch_size,
        )


def test_fail_record_size_exceeds_batch_size():
    """
    ValueError is raised if record_size is bigger than batch_size
    """
    with pytest.raises(
        ValueError,
        match=re.escape("'record_size' cannot exceed 'batch_size'"),
    ):
        f_kinesis.optimum(
            ["one"],
            f_kinesis.API_MAX_RECORD_SIZE_BYTES,
            f_kinesis.API_MAX_RECORD_SIZE_BYTES - 5,
        )


def test_fail_if_string_is_bigger_than_record_size():
    """
    ValueError is raised if record_size is bigger than batch_size
    """
    with pytest.raises(
        ValueError,
        match=re.escape("Batch element is too big for record size limit"),
    ):
        f_kinesis.optimum(["12345678901"], 10)


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
