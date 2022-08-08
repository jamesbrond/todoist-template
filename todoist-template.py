"""Easily add tasks to Todoist with customizable YAML templates"""

import os
import sys
import datetime
import logging
import argparse
import lib.key_ring as keyring
from lib.template import TodoistTemplate


def _check_python_version():
    if sys.version_info < (3, 8) or sys.version_info >= (4, 0):
        raise SystemError("This script requires Python >= 3.8 and < 4")
    return 1


class StoreDictKeyPair(argparse.Action):
    """Argparse Action"""
    def __call__(self, parser, namespace, values, option_string=None):
        my_dict = {}
        for keyval in values.split(","):
            key, val = keyval.split("=")
            my_dict[key] = val
        setattr(namespace, self.dest, my_dict)

def _parse_cmd_line():
    parser = argparse.ArgumentParser(
        prog="todoist-template.py",
        usage='%(prog)s [options]',
        description='Easily add tasks to Todoist with customizable YAML templates'
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
        action=StoreDictKeyPair,
        metavar="KEY0=VAL0,KEY1=VAL1...",
        default={},
        help="the placeholder values replaced in template"
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    parser.add_argument(
        "--id",
        dest="service_id",
        default="TODOIST-TEMPLATE",
        help="keyring service name where store Todoist API Token"
    )

    command_group = parser.add_mutually_exclusive_group()
    command_group.add_argument(
        "-d",
        "--debug",
        dest="loglevel",
        default=logging.INFO,
        action="store_const",
        const=logging.DEBUG,
        help="more verbose output",
    )
    command_group.add_argument(
        "-q",
        "--quiet",
        dest="loglevel",
        default=logging.INFO,
        action="store_const",
        const=logging.NOTSET,
        help="suppress output",
    )

    parser.add_argument(
        "--dry-run",
        dest="is_test",
        default=False,
        action="store_true",
        help="allows the %(prog)s command to run a trial without making any changes on Todoist.com, this process has the same output as the real execution except for new object ids.",
    )

    parser.add_argument(
        "--undo",
        dest="undo",
        type=argparse.FileType("rb"),
        help="loads undo file and rollbacks all operations in it"
    )

    parser.add_argument(
        "--token",
        dest="token",
        help="the Todoist authorization token"
    )

    return parser.parse_args()


def main():
    """Main function"""
    args = _parse_cmd_line()
    logging.basicConfig(level=args.loglevel, format="%(message)s")

    try:
        _check_python_version()

        api_token = args.token if args.token else keyring.get_api_token(args.service_id)

        while not api_token:
            logging.warning("Todoist API token not found for %s application.", args.service_id)
            keyring.setup(args.service_id)
            api_token = keyring.get_api_token(args.service_id)

        tmpl = TodoistTemplate(api_token, args.is_test)
        if args.undo:
            if tmpl.rollback(args.undo):
                args.undo.close()
                logging.debug("remove file %s", args.undo.name)
                os.remove(args.undo.name)
        else:
            script_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
            with args.template as file:
                logging.debug("open file %s", file)
                undofile = os.path.join(
                    script_folder,
                    f"{os.path.basename(file.name)}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.undo"
                ) if args.is_test is False else None
                tmpl.parse(file, args.placeholders, undofile)

        return 0
    except Exception as exc:
        logging.error(exc, exc_info=logging.getLogger().isEnabledFor(logging.DEBUG))
        return 1


if __name__ == "__main__":
    sys.exit(main())

# ~@:-]
