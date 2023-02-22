"""Configuration"""

import os
import sys
import logging
import logging.handlers
import argparse
import csv
import toml
import lib.__version__ as version
from lib.i18n import _
import lib.key_ring as keyring


class Config():
    """Load and handle toml configuration file, parse command line arguments"""

    def __init__(self, prompt_api_token=False):
        """Load TOML configuration file"""
        self._options = self._configuration(self._parse_cmd_line(), "./config.toml", prompt_api_token)
        self._set_logging()

    def __getattr__(self, key):
        """Returns configuration value"""
        return self._options.get(key)

    def check_python_version(self):
        """Check the current python version"""
        if sys.version_info < self._py_ver('min') or sys.version_info >= self._py_ver('max'):
            raise SystemError(_("This script requires Python >= 3.8 and < 4"))
        return 1

    def _py_ver(self, key):
        return tuple(e for e in self._options['python'][key])

    def _set_logging(self):
        logfolder = self._options["log"]["file_folder"]
        if not os.path.exists(logfolder):
            os.makedirs(logfolder)

        logger = logging.getLogger()
        logger.addHandler(self._logging_to_file_handler(f"{logfolder}/todoist_template.log"))
        logger.addHandler(self._logging_to_console_handler())
        # set the logger's level to the lowest
        logger.setLevel(min(self._options['log']['file_level'], self._options['log']['cli_level']))

    def _logging_to_file_handler(self, logfile):
        handler = logging.handlers.RotatingFileHandler(
            logfile,
            mode='a',
            maxBytes=self._options['log']['file_rolling_max_byte'],
            backupCount=self._options['log']['file_rolling_count'],
            encoding="utf8",
            delay=False,
            errors=None)
        handler.setFormatter(logging.Formatter(self._options['log']['file_format']))
        handler.setLevel(self._options['log']['file_level'])
        return handler

    def _logging_to_console_handler(self):
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(self._options['log']['cli_format']))
        handler.setLevel(self._options['log']['cli_level'])
        return handler

    def _configuration(self, args, config_file, prompt_api_token=False):
        data = toml.load(config_file)

        if args.service_id is not None:
            data["keyring"]["keyring_token_name"] = args.service_id

        if args.loglevel is not None:
            data["log"]["cli_level"] = args.loglevel

        data["service"]["run_service"] = args.gui

        data["todoist"].update({
            "template": args.template,
            "placeholders": args.placeholders if args.placeholders else [{}],
            "dry_run": args.dry_run,
            "is_update": args.is_update,
            "token": args.token if args.token is not None
            else keyring.get_keyring_api_token(data['keyring']['keyring_token_name'], prompt_api_token),
            "undo": args.undo
        })

        return data

    def _val_placeholder(self, values):
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

    def _parse_cmd_line(self):
        parser = argparse.ArgumentParser(
            prog="todoist_template.py",
            usage='%(prog)s [options]',
            description=_('Easily add tasks to Todoist with customizable YAML templates')
        )

        # positional arguments:
        parser.add_argument(
            "template",
            nargs="?",  # a single value, which can be optional
            type=argparse.FileType("r", encoding="utf8"),
            default=sys.stdin)

        # options
        parser.add_argument(
            "-D",
            dest="placeholders",
            type=self._val_placeholder,  # can be a file or a comma separated list of key=value
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

        return parser.parse_args()

# ~@:-]
