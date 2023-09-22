from cmdpkg import utils


def test_filter_none_values():
    assert list(utils.filter_none_values([1, 2, 3])) == [1, 2, 3]
    assert list(utils.filter_none_values([1, None, 3])) == [1, 3]
    assert list(utils.filter_none_values([None, None, None])) == []


def test_is_items_instance_of():
    assert utils.is_all_items_instance_of((), int)

    assert utils.is_all_items_instance_of((1, 2, 3), int)
    assert utils.is_all_items_instance_of((True, False), bool)

    assert not utils.is_all_items_instance_of((1, 2, 3), str)
    assert not utils.is_all_items_instance_of((1, False), str)
