"""Test command line parsing"""
from io import TextIOWrapper
import logging
import argparse
from pathlib import Path
import unittest
import collections.abc
from config.config import parse_cmd_line


TEMPLATE_FILE = "template_file"
TEMPLATE_VARS = "variables"


class TestCommandLine(unittest.TestCase):
    """Test command line parsing"""

    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)

    def test_command_line_arguments(self):
        """Test command line parsing"""
        cli = ["tests/test.yml",
               "-D", "test_name=me,test_date=today",
               "--id", "TODOIST_TEMPLATE",
               "--token", "1234567890abcdef",
               "--debug",
               "--dry-run"
               ]
        args = parse_cmd_line(cli)
        self.assertIsInstance(args.get(TEMPLATE_FILE), Path)
        self.assertEqual(args.get(TEMPLATE_FILE), Path('tests/test.yml'))
        self.assertIsInstance(args.get(TEMPLATE_VARS),
                              collections.abc.Sequence,
                              'placeholder is not an array')
        self.assertIn({'test_name': 'me', 'test_date': 'today'}, args.get(TEMPLATE_VARS),
                      'wrong parameters in placeholder')
        self.assertEqual(args.get("config.api_key_service"), 'TODOIST_TEMPLATE')
        self.assertEqual(args.get("config.api_token"), '1234567890abcdef')
        self.assertEqual(args.get("log.loggers.root.level"), "DEBUG")
        self.assertTrue(args.get("dry_run"))

    def test_command_line_placeholders_csv(self):
        """Test command line parsing with CSV as placeholders"""
        cli = ["tests/test.yml", "-D", "tests/placeholders.csv"]
        args = parse_cmd_line(cli)
        self.assertIsInstance(args.get(TEMPLATE_VARS),
                              collections.abc.Sequence,
                              'placeholder is not an array')
        self.assertEqual(len(args.get(TEMPLATE_VARS)), 3, 'wrong parameters in placeholder')

    def test_command_line_stdio(self):
        """Test command line parsing with template passed as standard input"""
        cli = ["--debug"]
        args = parse_cmd_line(cli)
        self.assertIsInstance(args.get(TEMPLATE_FILE), TextIOWrapper)
        self.assertEqual(args.get("log.loggers.root.level"), "DEBUG")

    def test_command_line_file_error(self):
        """Test command line parsing with not existing template file"""
        cli = ["test.tpl"]
        with self.assertRaises(argparse.ArgumentError):
            parse_cmd_line(cli)


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
