"""Test Config class"""
import pytest
from todoist_template.config.config import TTOptions


@pytest.fixture
def plain():
    """A plain (flat) TTOptions instance"""
    return TTOptions({"key0": "value0", "key1": "value1"})


@pytest.fixture
def nested():
    """A nested TTOptions instance"""
    return TTOptions({
        "parent0": {
            "child0": "value0",
            "child1": "value1"
        },
        "parent1": {
            "child2": "value2",
            "child3": "value3"
        }})


def test_constructor_none():
    """TTOptions contructor no arguments"""
    assert len(TTOptions()) == 0
    assert len(TTOptions({})) == 0


def test_constructor_kwargs():
    """TTOptions contructor kwargs"""
    assert len(TTOptions(key0="value0")) == 1
    assert len(TTOptions(leaf="value0", parent={"child": "value"})) == 2


def test_constructor_scalar():
    """TTOptions contructor scalar argument"""
    with pytest.raises(ValueError):
        TTOptions("test")
    with pytest.raises(ValueError):
        TTOptions({"test"})


def test_constructor_array():
    """TTOptions contructor array argument"""
    with pytest.raises(ValueError):
        TTOptions(["test"])


def test_constructor_plain_dict(plain):
    """TTOptions contructor plain dict argument"""
    assert len(plain) == 2
    assert plain.key1 == "value1"


def test_constructor_nested_dict(nested):
    """TTOptions contructor nested dict argument"""
    assert len(nested) == 2
    assert isinstance(nested.parent0, TTOptions)
    assert nested.parent1.child2 == "value2"


def test_options_set(plain, nested):
    """TTOptions option set"""
    plain.key1 = "new_value1"
    assert len(plain) == 2
    assert plain.key1 == "new_value1"

    nested.parent1.child2 = "new_value2"
    assert len(nested) == 2
    assert isinstance(nested.parent1, TTOptions)
    assert nested.parent1.child2 == "new_value2"


def test_options_setattr(plain, nested):
    """TTOptions option setattr"""
    plain.set("key1", 6)
    assert len(plain) == 2
    assert plain.key1 == 6

    nested.set("parent1.child2", "new_value2")
    assert len(nested) == 2
    assert isinstance(nested.parent1, TTOptions)
    assert nested.parent1.child2 == "new_value2"

    nested.set("parent2.child4", "new_value4")
    assert len(nested) == 3
    assert isinstance(nested.parent2, TTOptions)
    assert nested.parent2.child4 == "new_value4"


def test_options_del_leaf(plain, nested):
    """TTOptions option del leaf"""
    del plain.key1
    assert len(plain) == 1
    assert not plain.key1

    del nested.parent1.child2
    assert len(nested) == 2
    assert isinstance(nested.parent1, TTOptions)
    assert len(nested.parent1) == 1
    assert not nested.parent1.child2


def test_options_del_parent(nested):
    """TTOptions option del parent"""
    del nested.parent1
    assert len(nested) == 1
    assert isinstance(nested.parent0, TTOptions)
    assert not nested.parent1


def test_update(nested):
    """TTOptions update with dict"""
    new_value = {
        "parent0": {
            "child0": "value0",
            "child1": "new_value1"
        },
        "parent1": {
            "child3": "new_value3",
            "child4": 4
        },
        "key0": [1, 2, 3, 4]}
    nested.update(new_value)
    assert len(nested) == 3
    assert isinstance(nested.parent0, TTOptions)
    assert isinstance(nested.parent1, TTOptions)
    assert nested.key0[0] == 1


def test_update_with_option(nested):
    """TTOptions update with TTOptions"""
    new_nested = TTOptions({
        "parent0": {
            "child0": "value0",
            "child1": "new_value1"
        },
        "parent1": {
            "child3": "new_value3",
            "child4": 4
        },
        "key0": [1, 2, 3, 4]})
    nested.update(new_nested)
    assert len(nested) == 3
    assert isinstance(nested.parent0, TTOptions)
    assert isinstance(nested.parent1, TTOptions)
    assert nested.key0[0] == 1


# ~@:-]
