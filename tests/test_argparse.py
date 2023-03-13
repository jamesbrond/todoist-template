import logging
import unittest
import collections.abc
from lib.argparse import parse_cmd_line


class TestCommandLine(unittest.TestCase):
    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)

    def test_command_line_arguments(self):
        cli = ["tests/test.yml",
               "-D", "test_name=me,test_date=today",
               "--id", "TODOIST_TEMPLATE",
               "--token", "1234567890abcdef",
               "--debug",
               "--dry-run"
               ]
        args = parse_cmd_line(cli)
        self.assertEqual(args.get("template"), "tests/test.yml")
        self.assertIsInstance(args.get("placeholders"), collections.abc.Sequence, 'placeholder is not an array')
        self.assertIn({'test_name': 'me', 'test_date': 'today'}, args.get("placeholders"),
                      'wrong parameters in placeholder')
        self.assertEqual(args.get("service_id"), 'TODOIST_TEMPLATE')
        self.assertEqual(args.get("token"), '1234567890abcdef')
        self.assertEqual(args.get("loglevel"), logging.DEBUG)
        self.assertTrue(args.get("dry_run"))

    def test_command_line_placeholders_csv(self):
        cli = ["tests/test.yml", "-D", "tests/placeholders.csv"]
        args = parse_cmd_line(cli)
        self.assertIsInstance(args.get("placeholders"), collections.abc.Sequence, 'placeholder is not an array')
        self.assertEqual(len(args.get("placeholders")), 3, 'wrong parameters in placeholder')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
