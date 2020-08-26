"""
Unite tests for f_kinesis
"""
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


def test_ok():
    """
    TypeError is raised if input batch is not list
    """
    batch = ["a", "b", "cc", "ddd", "eeeee", "ffffffff", "ggggggggggggg"]
    optimal_batch = f_kinesis.optimum(batch)
    assert len(optimal_batch) == 1
    assert len(optimal_batch[0]) == len(batch)
    for idx, value in enumerate(batch):
        assert value == optimal_batch[0][idx]
