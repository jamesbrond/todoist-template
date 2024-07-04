"""Test Config class"""
import unittest
from lib.config.config import TTConfig, DEFAULT_CONFIG_FILE


class TestConfig(unittest.TestCase):
    """Test Config class"""

    def test_config_load_valid_file(self):
        """Load a valid TOML file"""
        args = ["--config", DEFAULT_CONFIG_FILE]
        cfg = TTConfig(args)
        self.assertFalse(cfg.is_empty())
        self.assertEqual(DEFAULT_CONFIG_FILE, cfg.config.file)

    def test_config_load_not_existing_file(self):
        """Load not existing file fallbacks on default"""
        args = ["--config", "./asddr55rgas.toml"]
        cfg = TTConfig(args)
        self.assertFalse(cfg.is_empty())
        self.assertEqual(DEFAULT_CONFIG_FILE, cfg.config.file)

    def test_config_load_no_file(self):
        """Load no file fallbacks on default"""
        cfg = TTConfig()
        self.assertFalse(cfg.is_empty())
        self.assertEqual(DEFAULT_CONFIG_FILE, cfg.config.file)

    def test_config_load_not_valid_file(self):
        """Load not valid TOML"""
        args = ["--config", "./requirements.txt"]
        with self.assertRaises(ValueError):
            TTConfig(args)

    def test_check_python_version_fail(self):
        """Check wrong python version"""
        cfg = TTConfig()
        self.assertFalse(cfg.check_python_version([2, 7], [3, 5]))

    def test_check_python_version_fail_none(self):
        """Check wrong python version passing None"""
        cfg = TTConfig()
        self.assertFalse(cfg.check_python_version(None, None))

    def test_config_getattr(self):
        """Get attribute from config"""
        cfg = TTConfig()
        self.assertTrue(cfg.log.handlers.console_handler)

    def test_argparse(self):
        """Config parse command line"""
        args = ["tests/test.yml", "-d", "--token", "123456789", "--dry-run"]
        cfg = TTConfig(args)
        self.assertTrue(cfg.template.file.name, "tests/tests.yml")
        self.assertEqual(cfg.log.loggers.root.level, "DEBUG")
        self.assertEqual(cfg.config.api_token, "123456789")
        self.assertTrue(cfg.template.dry_run)
        cfg.template.file.close()
        self.assertTrue(cfg.template.file.closed)


if __name__ == '__main__':
    unittest.main(verbosity=3, warnings='ignore')

# ~@:-]
