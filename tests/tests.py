import pytest
import optimum


@pytest.mark.parametrize("batch", [None, 1, {}, set(), object()])
def test_fail_not_list(mocker, batch):
    """
    TypeError is raised if input batch is not list
    """
    with pytest.raises(TypeError, match="Input parameter is not of type 'list'"):
        optimum.optimum(batch)


@pytest.mark.parametrize("batch_inner", [None, 1, {}, set(), object()])
def test_fail_str_not_str(mocker, batch_inner):
    """
    TypeError is raised if any batch element is not str
    """
    batch = [batch_inner]
    with pytest.raises(TypeError, match="Unsupported type of batch element"):
        optimum.optimum(batch)


def test_ok(mocker):
    """
    TypeError is raised if input batch is not list
    """
    batch = ["a", "b", "cc", "ddd", "eeeee", "ffffffff", "ggggggggggggg"]
    optimal_batch = optimum.optimum(batch)
    assert len(optimal_batch) == 1
    assert len(optimal_batch[0]) == len(batch)
    for idx in range(0, len(batch)):
        assert batch[idx] == optimal_batch[0][idx]

