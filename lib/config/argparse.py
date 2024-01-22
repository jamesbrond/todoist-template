"""Command line parser util"""
import os
import logging
import argparse
import csv
from lib.i18n import _
import lib.__version__ as version
from lib.loader.loaderfactory import TEMPLATE_CSV, TEMPLATE_JSON, TEMPLATE_YAML


def val_variable(values):
    """Argparse variables type"""
    variables = []
    if os.path.isfile(values):
        with open(values, 'r', encoding='utf8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            variables = list(csv_reader)
    else:
        my_dict = {}
        for keyval in values.split(","):
            key, val = keyval.split("=")
            my_dict[key] = val
        variables = [my_dict]
    return variables


def parse_cmd_line(cli=None):
    """Command line parser function"""
    parser = argparse.ArgumentParser(
        prog="todoist_template.py",
        usage='%(prog)s [options]',
        description=_('Easily add tasks to Todoist with customizable YAML templates'),
        exit_on_error=False
    )

    # positional arguments:
    file_parser = parser.add_mutually_exclusive_group()
    file_parser.add_argument(
        "template.file",
        nargs="?",  # a single value, which can be optional
        type=argparse.FileType('r', encoding='utf8'))
    file_parser.add_argument(
        "--undo",
        dest="template.undo.file",
        metavar="UNDO_FILE",
        type=argparse.FileType("rb"),
        help=_("loads undo file and rollbacks all operations in it")
    )

    # options
    parser.add_argument(
        "-D",
        dest="template.variables",
        type=val_variable,  # can be a file or a comma separated list of key=value
        metavar="KEY0=VAL0,KEY1=VAL1...",
        default={},
        help=_("the variable values replaced in template")
    )

    parser.add_argument(
        "--id",
        dest="config.api_key_service",
        metavar="API_KEY_SERVICE",
        help=_("keyring service name where store Todoist API Token")
    )

    parser.add_argument(
        "-c",
        "--config",
        dest="configfile",
        help=_("configuration file")
    )

    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument(
        "-d",
        "--debug",
        dest="log.loggers.root.level",
        action="store_const",
        const="DEBUG",
        help=_("more verbose output"),
    )
    command_group.add_argument(
        "-q",
        "--quiet",
        dest="log.loggers.root.level",
        action="store_const",
        const="NOTSET",
        help=_("suppress output"),
    )

    parser.add_argument(
        "--dry-run",
        dest="template.dry_run",
        default=False,
        action="store_true",
        help=_("allows the %(prog)s command to run a trial without making \
any changes on Todoist.com, this process has the same output as the real \
execution except for new object IDs."),
    )

    parser.add_argument(
        "-u",
        "--update",
        dest="template.is_update",
        default=False,
        action="store_true",
        help=_("update task with the same name instead of adding a new one")
    )

    parser.add_argument(
        "--token",
        dest="config.api_token",
        metavar="API_TOKEN",
        help=_("the Todoist authorization token")
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + version.__version__,
        help=_("show program's version number and exit"))

    tpl_type_group = parser.add_mutually_exclusive_group()
    tpl_type_group.add_argument(
        "--yaml",
        dest="template.type",
        action="store_const",
        const=TEMPLATE_YAML,
        help=_("template input file has YAML format")
    )
    tpl_type_group.add_argument(
        "--json",
        dest="template.type",
        action="store_const",
        const=TEMPLATE_JSON,
        help=_("template input file has JSON format")
    )
    tpl_type_group.add_argument(
        "--csv",
        dest="template.type",
        action="store_const",
        const=TEMPLATE_CSV,
        help=_("template input file has CSV format")
    )

    args, unknown = parser.parse_known_args(cli)
    logging.debug('unknown options: %s', str(unknown))
    return vars(args)
