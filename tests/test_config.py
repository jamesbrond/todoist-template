
"""Test Config class"""
from io import TextIOWrapper
from pathlib import Path
import unittest
from src.config.config import TTConfig, DEFAULT_CONFIG_FILE, _ttconfig_instances


class TestConfig(unittest.TestCase):
    """Test Config class"""

    def setUp(self) -> None:
        """Set up test case"""
        super().setUp()
        # Clear singleton instances for tests
        _ttconfig_instances.clear()

    def test_config_singleton(self):
        """Test singleton behavior of TTConfig"""
        cfg1 = TTConfig(["tests/test.yml"])
        cfg2 = TTConfig(["tests/another_test.yml"])
        self.assertIs(cfg1, cfg2, "TTConfig is not a singleton")

    def test_config_load_valid_file(self):
        """Load a valid TOML file"""
        args = ["tests/test.yml", "--config", str(DEFAULT_CONFIG_FILE)]
        cfg = TTConfig(args)
        self.assertFalse(cfg.is_empty())
        self.assertEqual(str(DEFAULT_CONFIG_FILE), str(cfg.config.file))

    def test_config_load_not_existing_file(self):
        """Load not existing file fallbacks on default"""
        args = ["tests/test.yml", "--config", "./asddr55rgas.toml"]
        _ttconfig_instances.clear()
        with self.assertRaises(ValueError, msg="Did not raise ValueError for non-existing config file"):
            TTConfig(args)

    def test_config_load_no_file(self):
        """Load no file fallbacks on default"""
        cfg = TTConfig(["tests/test.yml"])
        self.assertFalse(cfg.is_empty())
        self.assertEqual(DEFAULT_CONFIG_FILE, cfg.config.file)

    def test_config_load_not_valid_file(self):
        """Load not valid TOML"""
        args = ["tests/test.yml", "--config", "./requirements.txt"]
        with self.assertRaises(ValueError):
            TTConfig(args)

    def test_config_getattr(self):
        """Get attribute from config"""
        cfg = TTConfig(["tests/test.yml"])
        self.assertTrue(cfg.log.handlers.console_handler)

    def test_config_setattr(self):
        """Get attribute from config"""
        cfg = TTConfig(["tests/test.yml"])
        cfg.config.api_token = "123456789"
        self.assertEqual(cfg.config.api_token, "123456789")

    def test_argparse(self):
        """Config parse command line"""
        args = ["tests/test.yml", "-d", "--token", "123456789", "--dry-run"]
        cfg = TTConfig(args)
        self.assertTrue(cfg.template.file, Path("tests/tests.yml"))
        self.assertEqual(cfg.log.loggers.root.level, "DEBUG")
        self.assertEqual(cfg.config.api_token, "123456789")
        self.assertTrue(cfg.dry_run)
        with open(cfg.template.file, 'r', encoding='utf-8') as file:
            pass
        self.assertTrue(file.closed)

    def test_external_config(self):
        """Load external config file"""
        config_file = "tests/test_config.toml"
        args = ["tests/test.yml", "--config", config_file]

        cfg = TTConfig(args)
        self.assertFalse(cfg.is_empty())
        self.assertTrue(isinstance(cfg.config.file, Path), "config.file is not a Path")
        self.assertEqual(cfg.config.file, Path(config_file))
        self.assertEqual(cfg.config.api_key_service, "TODOIST_TEMPLATE")
        self.assertEqual(cfg.general.print_logo, True)
        self.assertEqual(cfg.log.loggers.root.level, "DEBUG")

    def test_config_template_stdio(self):
        """Test config line parsing with template passed as standard input"""
        args = ["--debug"]
        cfg = TTConfig(args)
        self.assertFalse(cfg.is_empty())
        self.assertTrue(cfg.template.stdin, 'Template stdin flag is wrong')
        self.assertTrue(isinstance(cfg.template.file, TextIOWrapper), "Template file is not TextIOWrapper")


if __name__ == '__main__':
    unittest.main(verbosity=3, warnings='ignore')

# ~@:-]
