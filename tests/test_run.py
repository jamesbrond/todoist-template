"""Test run application"""
import unittest
import logging
from lib.argparse import parse_cmd_line
from lib.config import Config
from todoist_template import run_cli
from todoist_template import get_template_content


class TestRun(unittest.TestCase):
    """Test run application"""

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_template_content(self):
        """Test reading template"""
        with open('tests/test.yml', 'r', encoding='utf8') as file:
            template = get_template_content(file)
            self.assertTrue(template, 'Cannot get template content')

    def test_run_simple_dry_run(self):
        """Test simple template in dry-run"""
        cli = ["tests/test.yml", "-D", "test_name=me,test_date=today", "--dry-run"]
        cfg = Config(parse_cmd_line(cli), prompt_api_token=False)
        self.assertEqual(0, run_cli(cfg),
                         "This test will fail if you don't set a valid API Token in keyring or evironment")

    def test_run_complex_dry_run(self):
        """Test complex template in dry-run"""
        cli = ["tests/test2.yml", "-D", "test_name=me,test_date=today", "--dry-run", "-u"]
        cfg = Config(parse_cmd_line(cli), prompt_api_token=False)
        self.assertEqual(0, run_cli(cfg),
                         "This test will fail if you don't set a valid API Token in keyring or evironment")

    def test_run_simple(self):
        """Test simple template not in dry-run"""
        cli = ["tests/test.yml", "-D", "test_name=me,test_date=today", "-u"]
        cfg = Config(parse_cmd_line(cli), prompt_api_token=False)
        self.assertEqual(0, run_cli(cfg),
                         "This test will fail if you don't set a valid API Token in keyring or evironment")


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
