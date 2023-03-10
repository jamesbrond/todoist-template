import unittest
import logging
from lib.argparse import parse_cmd_line
from lib.config import Config
from todoist_template import run_cli

class TestRun(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_run_simple(self):
        cli = ["tests/test.yml", "-D", "test_name=me,test_date=today", "--dry-run" ]
        self.cfg = Config(parse_cmd_line(cli),prompt_api_token=False)
        self.assertEqual(0, run_cli(self.cfg), "This test will fail if you don't set a valid API Token in keyring or evironment")

    def test_run_complex(self):
        cli = ["tests/test2.yml", "-D", "test_name=me,test_date=today", "--dry-run", "-u" ]
        self.cfg = Config(parse_cmd_line(cli),prompt_api_token=False)
        self.assertEqual(0, run_cli(self.cfg), "This test will fail if you don't set a valid API Token in keyring or evironment")


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
