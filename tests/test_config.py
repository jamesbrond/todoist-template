import os
import logging
import unittest
from lib.argparse import parse_cmd_line
from lib.config import Config


class TestConfig(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

        # delete log folder
        logfolder = 'logs'
        if os.path.exists(logfolder):
            for filename in os.listdir(logfolder):
                os.remove(os.path.join(logfolder, filename))
            os.rmdir(logfolder)

        cli = ["tests/test.yml",
               "-D", "test_name=me,test_date=today",
               "--id", "TODOIST_TEMPLATE",
               "--debug",
               "--dry-run"
               ]
        self.cfg = Config(parse_cmd_line(cli), prompt_api_token=False)

    def test_is_dry_run(self):
        self.assertTrue(self.cfg.todoist['dry_run'], "This test doesn't run in dry-run")

    def test_python_version(self):
        self.cfg.check_python_version()


if __name__ == '__main__':
    unittest.main(warnings='ignore')

# ~@:-]
