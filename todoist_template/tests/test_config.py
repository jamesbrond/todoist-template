"""Test Config class"""
import sys
from pathlib import Path
import pytest
from todoist_template.config.config import TTConfig, DEFAULT_CONFIG_FILE, _ttconfig_instances


@pytest.fixture(autouse=True)
def _clear_singleton():
    """Clear singleton instances before each test"""
    _ttconfig_instances.clear()
    yield


def test_config_singleton():
    """Test singleton behavior of TTConfig"""
    cfg1 = TTConfig(["tests/assets/test.yml"])
    cfg2 = TTConfig(["tests/assets/another_test.yml"])
    assert cfg1 is cfg2, "TTConfig is not a singleton"


def test_config_load_valid_file():
    """Load a valid TOML file"""
    args = ["tests/assets/test.yml", "--config", str(DEFAULT_CONFIG_FILE)]
    cfg = TTConfig(args)
    assert not cfg.is_empty()
    assert str(DEFAULT_CONFIG_FILE) == str(cfg.config.file)


def test_config_load_not_existing_file():
    """Load not existing file fallbacks on default"""
    args = ["tests/assets/test.yml", "--config", "./asddr55rgas.toml"]
    _ttconfig_instances.clear()
    with pytest.raises(ValueError):
        TTConfig(args)


def test_config_load_no_file():
    """Load no file fallbacks on default"""
    cfg = TTConfig(["tests/assets/test.yml"])
    assert not cfg.is_empty()
    assert DEFAULT_CONFIG_FILE == cfg.config.file


def test_config_load_not_valid_file():
    """Load not valid TOML"""
    args = ["tests/assets/test.yml", "--config", "./requirements.txt"]
    with pytest.raises(ValueError):
        TTConfig(args)


def test_config_getattr():
    """Get attribute from config"""
    cfg = TTConfig(["tests/assets/test.yml"])
    assert cfg.log.handlers.console_handler


def test_config_setattr():
    """Get attribute from config"""
    cfg = TTConfig(["tests/assets/test.yml"])
    cfg.config.api_token = "123456789"
    assert cfg.config.api_token == "123456789"


def test_argparse():
    """Config parse command line"""
    args = ["tests/assets/test.yml", "-d", "--token", "123456789", "--dry-run"]
    cfg = TTConfig(args)
    assert cfg.template.file
    assert cfg.log.loggers.root.level == "DEBUG"
    assert cfg.config.api_token == "123456789"
    assert cfg.dry_run
    with open(cfg.template.file, 'r', encoding='utf-8') as file:
        pass
    assert file.closed


def test_external_config():
    """Load external config file"""
    config_file = "tests/assets/test_config.toml"
    args = ["tests/assets/test.yml", "--config", config_file]

    cfg = TTConfig(args)
    assert not cfg.is_empty()
    assert isinstance(cfg.config.file, Path), "config.file is not a Path"
    assert cfg.config.file == Path(config_file)
    assert cfg.config.api_key_service == "TODOIST_TEMPLATE"
    assert cfg.general.print_logo is True
    assert cfg.log.loggers.root.level == "DEBUG"


def test_config_template_stdio():
    """Test config line parsing with template passed as standard input"""
    args = ["--debug"]
    cfg = TTConfig(args)
    assert not cfg.is_empty()
    assert cfg.template.stdin, 'Template stdin flag is wrong'
    assert cfg.template.file is sys.stdin, "Template file is not stdin"


# ~@:-]
