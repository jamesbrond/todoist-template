"""Command line arguments parser module"""
import sys
from pathlib import Path
import argparse
from typing import TextIO
import csv

from todoist_template.i18n import _t
from todoist_template.__version__ import __version__
from todoist_template.template.loader.csvloader import CSV_DELIMITER, CSV_FIELDNAMES


def argparse_existing_file(filename: str | TextIO) -> Path | TextIO:
    """Argparse Type: checks if a file exists and is a file"""
    if isinstance(filename, type(sys.stdin)):
        return filename

    file_path = Path(filename)
    if file_path.exists() and file_path.is_file():
        return file_path

    raise argparse.ArgumentTypeError(f"File not found: {filename}")


def argparse_val_variables(values: str) -> list[dict]:
    """Argparse Type: variables can be a CSV file or a comma separated list of key=value"""

    if not values:
        return []

    if Path(values).is_file():
        with open(values, 'r', encoding='utf8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            return list(csv_reader)

    results = {}
    pairs = values.split(',')
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            results[key.strip()] = value.strip()
    return [results]


def parse_cmd_line(cli: list[str] | None = None) -> argparse.Namespace:
    """Command line parser function"""
    parser = argparse.ArgumentParser(
        description=_t('Easily add tasks to Todoist with customizable YAML templates'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        argument_default=argparse.SUPPRESS,
        exit_on_error=False
    )

    # positional arguments:
    file_parser = parser.add_mutually_exclusive_group()
    file_parser.add_argument(
        "template_file",
        nargs="?",  # a single value, which can be optional
        metavar="TEMPLATE_FILE",
        type=argparse_existing_file,
        default=sys.stdin,
        help=_t("""the template file, if no file is supplied it uses standard input.
 Requirement: file encoding must be UTF-8"""))
    file_parser.add_argument(
        "--undo",
        dest="template_undo_file",
        metavar="UNDO_FILE",
        type=Path,
        help=_t("loads undo file and rollbacks all operations in it")
    )

    parser.add_argument(
        "-t",
        dest="quick_add",
        default=False,
        action='store_true',
        help=_t("""add a new item using the Todoist Quick Add implementation,
the template will be used as text for the new task""")
    )

    # options
    parser.add_argument(
        "-D",
        dest="variables",
        type=argparse_val_variables,  # can be a file or a comma separated list of key=value
        metavar="KEY0=VAL0,KEY1=VAL1... | PATH/TO/PARAMETERS.FILE",
        default={},
        help=_t("can be a file or a comma separated list of key=value")
    )

    parser.add_argument(
        "--id",
        dest="config.api_key_service",
        metavar="API_KEY_SERVICE",
        help=_t("keyring service name where store Todoist API Token")
    )

    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        dest="configfile",
        help=_t("TOML configuration file")
    )

    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument(
        "-d",
        "--debug",
        dest="log.loggers.root.level",
        action="store_const",
        const="DEBUG",
        help=_t("more verbose output"),
    )
    command_group.add_argument(
        "-q",
        "--quiet",
        dest="log.loggers.root.level",
        action="store_const",
        const="NOTSET",
        help=_t("suppress output"),
    )

    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        default=False,
        action="store_true",
        help=_t("allows the %(prog)s command to run a trial without making \
any changes on Todoist.com, this process has the same output as the real \
execution except for new object IDs."),
    )

    parser.add_argument(
        "-u",
        "--update",
        dest="is_update",
        default=False,
        action="store_true",
        help=_t("update task with the same name instead of adding a new one")
    )

    parser.add_argument(
        "--token",
        dest="config.api_token",
        metavar="API_TOKEN",
        help=_t("the Todoist authorization token")
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + __version__,
        help=_t("show program's version number and exit"))

    tpl_type_group = parser.add_mutually_exclusive_group()
    tpl_type_group.add_argument(
        "--yaml",
        dest="template_type",
        action="store_const",
        const="YAML",
        help=_t("template input file has YAML format")
    )
    tpl_type_group.add_argument(
        "--json",
        dest="template_type",
        action="store_const",
        const="JSON",
        help=_t("template input file has JSON format")
    )
    tpl_type_group.add_argument(
        "--csv",
        dest="template_type",
        action="store_const",
        const="CSV",
        help=_t(f"""template input file has CSV format.
Possible fields are: {', '.join(CSV_FIELDNAMES)}.
Default delimiter is '{CSV_DELIMITER}'.""")
    )
    tpl_type_group.add_argument(
        "--text",
        dest="template_type",
        action="store_const",
        const="PLAINTEXT",
        help=_t("template input file has Plain/Text format.")
    )

    args, unk = parser.parse_known_args(cli)  # pylint: disable=unused-variable
    return vars(args)

# ~@:-]
