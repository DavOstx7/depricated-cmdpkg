import pytest

from cmdpkg import utils


def test_filter_none_values():
    assert list(utils.filter_none_values([1, 2, 3])) == [1, 2, 3]
    assert list(utils.filter_none_values([1, None, 3])) == [1, 3]
    assert list(utils.filter_none_values([None, None, None])) == []


def test_validate_minimum_length():
    utils.validate_minimum_length((1, 2, 3), minimum_length=0)
    utils.validate_minimum_length((1, 2, 3), minimum_length=3)

    with pytest.raises(ValueError) as exception:
        utils.validate_minimum_length((1, 2, 3), minimum_length=4)
        assert not str(exception.value)

    with pytest.raises(ValueError) as exception:
        utils.validate_minimum_length((1, 2, 3), minimum_length=4, message="error")
        assert str(exception.value) == "error"


def test_validate_same_type():
    utils.validate_same_type((1, 2, 3))
    utils.validate_same_type((True, False))

    with pytest.raises(TypeError) as exception:
        utils.validate_same_type((0.5, 1))
        assert not str(exception.value)

    with pytest.raises(TypeError) as exception:
        utils.validate_same_type((0.5, 1), message="error")
        assert str(exception.value) == "error"
