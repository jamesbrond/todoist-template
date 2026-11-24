"""PlaceholderToken tests."""
from tplline.tokenizer.token import PlaceholderToken


def test_raw_returns_original_source():
    """Test that the raw() method returns the original source of the token."""
    token = PlaceholderToken("{username|Guest}")
    assert token.raw() == "{username|Guest}"


def test_raw_is_unaffected_by_render():
    """Test that the raw() method is unaffected by the render() method."""
    token = PlaceholderToken("{username|Guest}")
    token.render({"username": "jbrond"})
    assert token.raw() == "{username|Guest}"


def test_repr():
    """Test that the __repr__() method returns a string representation of the token."""
    token = PlaceholderToken("{username|Guest}")
    assert repr(token) == "Token[PLACEHOLDER]({username|Guest})"
