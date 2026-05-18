"""Test Config class"""
from pathlib import Path
import sys
import unittest
from template.template_model import TTemplate, guess_template_type
from template.loader.abstractloader import template_mimetypes, template_extensions


class TestTemplateModel(unittest.TestCase):
    """Test Options class"""

    def test_tesmplate_stdio(self):
        """Template from standard input"""
        tpl = TTemplate(file=sys.stdin)
        self.assertTrue(tpl.stdin)
        self.assertIsNone(tpl.type)

    def test_read_file(self):
        """Template from file"""
        tpl = TTemplate(file=Path('tests/test.yml'))
        self.assertFalse(tpl.stdin)
        self.assertEqual(tpl.file.stem, 'test')
        self.assertEqual(tpl.type, 'YAML')
        self.assertGreater(len(tpl.read()), 0)

    def test_undo_file(self):
        """Test undo file generation"""
        tpl = TTemplate(file=Path('tests/test.json'))
        undo_file = tpl.undo_file_from_template
        self.assertTrue(undo_file.stem.startswith('test_'))
        self.assertTrue(undo_file.suffix == '.undo')
        self.assertEqual(tpl.type, 'JSON')

    def test_undo_file_stdio(self):
        """Test undo file generation for stdin template"""
        tpl = TTemplate(file=sys.stdin)
        undo_file = tpl.undo_file_from_template
        self.assertTrue(undo_file.stem.startswith('todoist_template'))
        self.assertTrue(undo_file.suffix == '.undo')

    def test_template_file_not_found(self):
        """Test template file not found"""
        tpl = TTemplate(file=Path('tests/non_existing.yml'))
        with self.assertRaises(ValueError):
            tpl.read()

    def test_template_no_file(self):
        """Test template with no file"""
        tpl = TTemplate()
        with self.assertRaises(ValueError):
            tpl.read()

    def test_template_no_file_stdin(self):
        """Test template with no file but stdin True"""
        tpl = TTemplate(stdin=True)
        with self.assertRaises(ValueError):
            tpl.read()

    def test_template_no_file_stdin_false(self):
        """Test template with no file and stdin False"""
        tpl = TTemplate(stdin=False)
        with self.assertRaises(ValueError):
            tpl.read()

    def test_template_undo_folder_default(self):
        """Test default undo folder"""
        tpl = TTemplate(file=Path('tests/test.yml'))
        self.assertIsNotNone(tpl.undo_folder, "Undo folder should not be None")

    def test_template_undo_folder_custom(self):
        """Test custom undo folder"""
        custom_folder = Path('custom_undo_folder')
        tpl = TTemplate(file=Path('tests/test.yml'), undo_folder=custom_folder)
        self.assertEqual(tpl.undo_folder, custom_folder)
        self.assertIsNone(tpl.undo_file, "Undo file should be None when not set")

    def test_template_on_undo_actiton(self):
        """Test when undo action file is set"""
        tpl = TTemplate(undo_file=Path('tests/test.undo'))
        self.assertEqual(tpl.undo_folder, tpl.undo_file.parent.resolve())

    def test_template_type_guessing(self):
        """Test template type guessing"""

        self.assertGreater(len(template_mimetypes), 0)
        self.assertGreater(len(template_extensions), 0)

        yaml_type = guess_template_type(Path('tests/test.yml'))
        self.assertEqual(yaml_type, 'YAML')

        json_type = guess_template_type(Path('tests/test.json'))
        self.assertEqual(json_type, 'JSON')

        csv_type = guess_template_type(Path('tests/test.csv'))
        self.assertEqual(csv_type, 'CSV')

        txt_type = guess_template_type(Path('tests/test.txt'))
        self.assertEqual(txt_type, 'PLAINTEXT')

        unknown_type = guess_template_type(Path('tests/test.unknown'))
        self.assertIsNone(unknown_type)


if __name__ == '__main__':
    unittest.main(verbosity=3, warnings='ignore')

# ~@:-]
