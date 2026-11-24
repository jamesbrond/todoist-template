"""Test command line parsing"""
import sys
import logging
import argparse
from pathlib import Path
import collections.abc
import pytest
from todoist_template.config.config import parse_cmd_line


TEMPLATE_FILE = "template_file"
TEMPLATE_VARS = "variables"


@pytest.fixture(autouse=True)
def _silence_logging():
    """Disable logging noise during tests"""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


def test_command_line_arguments():
    """Test command line parsing"""
    cli = ["tests/assets/test.yml",
           "-D", "test_name=me,test_date=today",
           "--id", "TODOIST_TEMPLATE",
           "--token", "1234567890abcdef",
           "--debug",
           "--dry-run"
           ]
    args = parse_cmd_line(cli)
    assert isinstance(args.get(TEMPLATE_FILE), Path)
    assert args.get(TEMPLATE_FILE) == Path('tests/assets/test.yml')
    assert isinstance(args.get(TEMPLATE_VARS), collections.abc.Sequence), 'placeholder is not an array'
    assert {'test_name': 'me', 'test_date': 'today'} in args.get(TEMPLATE_VARS), 'wrong parameters in placeholder'
    assert args.get("config.api_key_service") == 'TODOIST_TEMPLATE'
    assert args.get("config.api_token") == '1234567890abcdef'
    assert args.get("log.loggers.root.level") == "DEBUG"
    assert args.get("dry_run")


def test_command_line_placeholders_csv():
    """Test command line parsing with CSV as placeholders"""
    cli = ["tests/assets/test.yml", "-D", "tests/assets/placeholders.csv"]
    args = parse_cmd_line(cli)
    assert isinstance(args.get(TEMPLATE_VARS), collections.abc.Sequence), 'placeholder is not an array'
    assert len(args.get(TEMPLATE_VARS)) == 3, 'wrong parameters in placeholder'


def test_command_line_stdio():
    """Test command line parsing with template passed as standard input"""
    cli = ["--debug"]
    args = parse_cmd_line(cli)
    assert args.get(TEMPLATE_FILE) is sys.stdin
    assert args.get("log.loggers.root.level") == "DEBUG"


def test_command_line_file_error():
    """Test command line parsing with not existing template file"""
    cli = ["test.tpl"]
    with pytest.raises(argparse.ArgumentError):
        parse_cmd_line(cli)


# ~@:-]
