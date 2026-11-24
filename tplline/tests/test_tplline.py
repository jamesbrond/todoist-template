"""Tests for the TPLLine class."""
import io
from unittest.mock import patch
import pytest
from tplline.tplline import TPLLine


def test_no_input_raises_error():
    """Test that initializing TPLLine with no input raises a ValueError."""
    with pytest.raises(ValueError):
        TPLLine()


def test_from_string():
    """Test that a TPLLine instance can be created from a string."""
    tpl = TPLLine(text="Hello {name|World}!")
    assert tpl.render({"name": "jbrond"}) == "Hello jbrond!"


def test_from_file(tmp_path):
    """Test that a TPLLine instance can be created from a file."""
    template_file = tmp_path / "tpl.txt"
    template_file.write_text("Hello {name|World}!")
    tpl = TPLLine.from_file(str(template_file))
    assert tpl.render({"name": "jbrond"}) == "Hello jbrond!"


def test_from_file_with_include(tmp_path):
    """Test that a template file can include another file in the same directory."""
    footer = tmp_path / "footer.txt"
    footer.write_text("Goodbye {name|World}!")
    template_file = tmp_path / "tpl.txt"
    template_file.write_text("Hello {name|World}!\n#! include footer.txt")
    tpl = TPLLine.from_file(str(template_file))
    assert tpl.render({"name": "jbrond"}) == "Hello jbrond!\nGoodbye jbrond!"


def test_from_file_include_parent_directory(tmp_path):
    """Test that a template file in a subfolder can include a file from the parent directory."""
    footer = tmp_path / "footer.txt"
    footer.write_text("Goodbye {name|World}!")
    subfolder = tmp_path / "subfolder"
    subfolder.mkdir()
    template_file = subfolder / "tpl.txt"
    template_file.write_text("Hello {name|World}!\n#! include ../footer.txt")
    tpl = TPLLine.from_file(str(template_file))
    assert tpl.render({"name": "jbrond"}) == "Hello jbrond!\nGoodbye jbrond!"


def test_from_stdin():
    """Test that a TPLLine instance can be created from standard input."""
    with patch("sys.stdin", io.StringIO("Hello {name|World}!")):
        tpl = TPLLine.from_stdin()
    assert tpl.render({"name": "jbrond"}) == "Hello jbrond!"
