#!/usr/bin/env python

"""Easily add tasks to Todoist with customizable YAML templates"""

import os
import sys
import datetime
import logging
import argparse
import csv
import lib.key_ring as keyring
from lib.template import TodoistTemplate
import lib.__version__ as version
from lib.i18n import _


def _check_python_version():
    if sys.version_info < (3, 8) or sys.version_info >= (4, 0):
        raise SystemError(_("This script requires Python >= 3.8 and < 4"))
    return 1


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


def _parse_cmd_line():
    parser = argparse.ArgumentParser(
        prog="todoist_template.py",
        usage='%(prog)s [options]',
        description=_('Easily add tasks to Todoist with customizable YAML templates')
    )

    # positional arguments:
    parser.add_argument(
        "template",
        nargs="?",
        type=argparse.FileType("r", encoding="utf8"),
        default=sys.stdin)

    # options
    parser.add_argument(
        "-D",
        dest="placeholders",
        type=val_placeholder,
        metavar="KEY0=VAL0,KEY1=VAL1...",
        default={},
        help=_("the placeholder values replaced in template")
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + version.__version__,
        help=_("show program's version number and exit"))

    parser.add_argument(
        "--id",
        dest="service_id",
        default="TODOIST-TEMPLATE",
        help=_("keyring service name where store Todoist API Token")
    )

    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument(
        "-d",
        "--debug",
        dest="loglevel",
        default=logging.INFO,
        action="store_const",
        const=logging.DEBUG,
        help=_("more verbose output"),
    )
    command_group.add_argument(
        "-q",
        "--quiet",
        dest="loglevel",
        default=logging.INFO,
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
        "--undo",
        dest="undo",
        type=argparse.FileType("rb"),
        help=_("loads undo file and rollbacks all operations in it")
    )

    parser.add_argument(
        "--token",
        dest="token",
        help=_("the Todoist authorization token")
    )

    return parser.parse_args()


def main():
    """Main function"""
    args = _parse_cmd_line()

    logging.basicConfig(level=args.loglevel, format="%(message)s")
    logging.info(version.LOGO)

    try:
        _check_python_version()

        api_token = args.token if args.token else keyring.get_api_token(args.service_id)

        while not api_token:
            logging.warning(_("Todoist API token not found for %s application."), args.service_id)
            keyring.setup(args.service_id)
            api_token = keyring.get_api_token(args.service_id)

        tmpl = TodoistTemplate(api_token, args.dry_run)
        if args.undo:
            if tmpl.rollback(args.undo):
                args.undo.close()
                logging.debug(_("remove file %s"), args.undo.name)
                os.remove(args.undo.name)
        else:
            script_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
            with args.template as file:
                logging.debug(_("open file %s"), file)
                if not args.dry_run:
                    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                    undofile = os.path.join(
                        script_folder,
                        f"{os.path.basename(file.name)}-{now}.undo"
                    )
                else:
                    undofile = None
                for placeholders in args.placeholders:
                    tmpl.parse(file, placeholders, undofile)

        return 0

    except Exception as exc:  # pylint: disable=broad-except
        logging.error(exc, exc_info=logging.getLogger().isEnabledFor(logging.DEBUG))
        return 1


if __name__ == "__main__":
    sys.exit(main())

# ~@:-]
