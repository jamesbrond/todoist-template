"""Test Config class"""
from pathlib import Path
import sys
import pytest
from todoist_template.template.template_model import TTemplate, guess_template_type
from todoist_template.template.loader.abstractloader import template_mimetypes, template_extensions


def test_tesmplate_stdio():
    """Template from standard input"""
    tpl = TTemplate(file=sys.stdin)
    assert tpl.stdin
    assert tpl.type is None


def test_read_file():
    """Template from file"""
    tpl = TTemplate(file=Path('tests/assets/test.yml'))
    assert not tpl.stdin
    assert tpl.file.stem == 'test'
    assert tpl.type == 'YAML'
    assert len(tpl.read()) > 0


def test_undo_file():
    """Test undo file generation"""
    tpl = TTemplate(file=Path('tests/assets/test.json'))
    undo_file = tpl.undo_file_from_template
    assert undo_file.stem.startswith('test_')
    assert undo_file.suffix == '.undo'
    assert tpl.type == 'JSON'


def test_undo_file_stdio():
    """Test undo file generation for stdin template"""
    tpl = TTemplate(file=sys.stdin)
    undo_file = tpl.undo_file_from_template
    assert undo_file.stem.startswith('todoist_template')
    assert undo_file.suffix == '.undo'


def test_template_file_not_found():
    """Test template file not found"""
    tpl = TTemplate(file=Path('tests/assets/non_existing.yml'))
    with pytest.raises(ValueError):
        tpl.read()


def test_template_no_file():
    """Test template with no file"""
    tpl = TTemplate()
    with pytest.raises(ValueError):
        tpl.read()


def test_template_no_file_stdin():
    """Test template with no file but stdin True"""
    tpl = TTemplate(stdin=True)
    with pytest.raises(ValueError):
        tpl.read()


def test_template_no_file_stdin_false():
    """Test template with no file and stdin False"""
    tpl = TTemplate(stdin=False)
    with pytest.raises(ValueError):
        tpl.read()


def test_template_undo_folder_default():
    """Test default undo folder"""
    tpl = TTemplate(file=Path('tests/assets/test.yml'))
    assert tpl.undo_folder is not None, "Undo folder should not be None"


def test_template_undo_folder_custom():
    """Test custom undo folder"""
    custom_folder = Path('custom_undo_folder')
    tpl = TTemplate(file=Path('tests/assets/test.yml'), undo_folder=custom_folder)
    assert tpl.undo_folder == custom_folder
    assert tpl.undo_file is None, "Undo file should be None when not set"


def test_template_on_undo_actiton():
    """Test when undo action file is set"""
    tpl = TTemplate(undo_file=Path('tests/assets/test.undo'))
    assert tpl.undo_folder == tpl.undo_file.parent.resolve()


def test_template_type_guessing():
    """Test template type guessing"""

    assert len(template_mimetypes) > 0
    assert len(template_extensions) > 0

    yaml_type = guess_template_type(Path('tests/assets/test.yml'))
    assert yaml_type == 'YAML'

    json_type = guess_template_type(Path('tests/assets/test.json'))
    assert json_type == 'JSON'

    csv_type = guess_template_type(Path('tests/assets/test.csv'))
    assert csv_type == 'CSV'

    txt_type = guess_template_type(Path('tests/assets/test.txt'))
    assert txt_type == 'PLAINTEXT'

    unknown_type = guess_template_type(Path('tests/assets/test.unknown'))
    assert unknown_type is None


# ~@:-]
