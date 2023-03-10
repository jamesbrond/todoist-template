"""Command line parser util"""
import os
import sys
import logging
import argparse
import csv
from lib.i18n import _
import lib.__version__ as version


def val_placeholder(values):
    """Argparse placeholders type"""
    placeholders = []
    if os.path.isfile(values):
        with open(values, 'r', encoding='utf8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            placeholders = list(csv_reader)
    else:
        my_dict = {}
        for keyval in values.split(","):
            key, val = keyval.split("=")
            my_dict[key] = val
        placeholders = [my_dict]
    return placeholders


def parse_cmd_line(cli=None):
    """Command line parser function"""
    parser = argparse.ArgumentParser(
        prog="todoist_template.py",
        usage='%(prog)s [options]',
        description=_('Easily add tasks to Todoist with customizable YAML templates')
    )

    # positional arguments:
    parser.add_argument(
        "template",
        nargs="?",  # a single value, which can be optional
        type=str,
        default=sys.stdin)

    # options
    parser.add_argument(
        "-D",
        dest="placeholders",
        type=val_placeholder,  # can be a file or a comma separated list of key=value
        metavar="KEY0=VAL0,KEY1=VAL1...",
        default={},
        help=_("the placeholder values replaced in template")
    )

    parser.add_argument(
        "--id",
        dest="service_id",
        help=_("keyring service name where store Todoist API Token")
    )

    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument(
        "-d",
        "--debug",
        dest="loglevel",
        action="store_const",
        const=logging.DEBUG,
        help=_("more verbose output"),
    )
    command_group.add_argument(
        "-q",
        "--quiet",
        dest="loglevel",
        action="store_const",
        const=logging.NOTSET,
        help=_("suppress output"),
    )

    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        default=False,
        action="store_true",
        help=_("allows the %(prog)s command to run a trial without making \
any changes on Todoist.com, this process has the same output as the real \
execution except for new object IDs."),
    )

    parser.add_argument(
        "-u",
        "--update",
        dest="is_update",
        default=False,
        action="store_true",
        help=_("update task with the same name instead of adding a new one")
    )

    parser.add_argument(
        "--token",
        dest="token",
        help=_("the Todoist authorization token")
    )

    parser.add_argument(
        "--undo",
        dest="undo",
        type=argparse.FileType("rb"),
        help=_("loads undo file and rollbacks all operations in it")
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + version.__version__,
        help=_("show program's version number and exit"))

    parser.add_argument(
        "--gui",
        dest="gui",
        default=False,
        action="store_true",
        help=_("start todoist-template service with Web GUI"))

    args, unknown = parser.parse_known_args(cli)
    logging.debug('unknown options: %s', str(unknown))
    return vars(args)
