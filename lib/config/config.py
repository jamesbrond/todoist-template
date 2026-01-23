"""Todoist-template configuration handler"""
from collections.abc import Iterable
from copy import copy
import sys
import os
import logging
import logging.config
import argparse
import csv
import toml
from lib.i18n import _
from lib.template.loader.csvloader import CSV_DELIMITER, CSV_FIELDNAMES
from lib.__version__ import __version__


DEFAULT_CONFIG_FILE = 'lib/config/config.toml'
PYTHON_MIN = (3, 14)
PYTHON_MAX = (4, 0)


class NoTraceExceptionFormatter(logging.StreamHandler):
    """Logging formatter without traceback for exceptions"""
    def format(self, record):
        if hasattr(record, "exc_info"):
            new_record = copy(record)
            new_record.exc_info = None
            return super().format(new_record)
        return super().format(record)


class TTOptions(dict):
    """
    Use a dot "." to access members of dictionary
    """
    def __init__(self: TTOptions, *args: Iterable, **kwargs: any) -> None:
        super().__init__(*args, **kwargs)
        _ = [self.__compose__(arg) for arg in args]

        if kwargs:
            self.__compose__(kwargs)

    def __getattr__(self, attr: str) -> any:
        return self.get(attr)

    def __setattr__(self, key: str, value: any) -> None:
        self.__setitem__(key, value)

    def __setitem__(self, key: str, value: any) -> None:
        super().__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item: str) -> None:
        self.__delitem__(item)

    def __delitem__(self, key: str) -> None:
        super().__delitem__(key)
        del self.__dict__[key]

    def has_key(self, key: str) -> bool:
        """Retrunt true if config contains `key`"""
        return key in self.keys()

    def __compose__(self, arg: dict[str, any], update: bool = False) -> None:
        for key, value in arg.items():
            if isinstance(value, dict):
                if self.has_key(key) and update:
                    self[key].update(value)
                else:
                    self[key] = TTOptions(value)
            elif value is not None:
                self[key] = value

    def set(self, path: str, value: any) -> None:
        """Set value"""
        self.set_array(path.split('.'), value)

    def set_array(self, keys: list[str], value: any) -> None:
        """Set array of keys"""
        key = keys.pop(0)
        if len(keys) == 0:
            self[key] = value
        else:
            if not self.has_key(key):
                self[key] = TTOptions()
            self[key].set_array(keys, value)

    def update(self, arg: dict[str, any]) -> None:
        """Update config opbject"""
        if arg:
            self.__compose__(arg, True)


class TTConfig:
    """Todoist-template configuration handler class"""

    def __init__(self, cliargs: list[str] | None = None) -> None:
        # Options in descending order of relevance
        # 1. hardcoded values
        # from default config file lib/config/config.toml
        self._options = TTOptions({})
        self._options.update(self._load_config(DEFAULT_CONFIG_FILE))

        # 2. configuration file if any
        # command line argument --config
        args = parse_cmd_line(cliargs)
        if args.get("configfile"):
            self._options.update(self._load_config(args.get("configfile")))

        # 3. command line arguments
        self._options.update(self._map_args(args))

        logging.config.dictConfig(self.log)  # self.log -> uses __getattr___(log)

    def __getattr__(self, attr: str) -> TTOptions | None:
        """Returns configuration value"""
        return self._options.get(attr)

    def is_empty(self) -> bool:
        """Returns true if configuration is empty"""
        return len(self._options) == 0

    def is_valid_python_version(self, pymin: tuple[int, int], pymax: tuple[int, int]) -> bool:
        """Check python requirements for application"""
        try:
            logging.debug("check python requirement %s - %s", str(pymin), str(pymax))
            return sys.version_info >= pymin or sys.version_info < pymax
        except Exception as exc:
            logging.fatal(exc)
            return False

    @property
    def version(self) -> str:
        """Returns application version"""
        return __version__

    def _load_config(self, filename: str) -> dict:
        # load TOML configuration from `filename`
        try:
            data = toml.load(filename)
            data.setdefault('config', {})['file'] = filename
            return data
        except (FileNotFoundError, PermissionError) as ex:
            raise ValueError("Cannot load configuration file") from ex
        except toml.decoder.TomlDecodeError as ex:
            raise ValueError("Bad configuration file") from ex

    def _map_args(self, args: dict) -> TTOptions:
        data = TTOptions()
        _ = [data.set(key, value) for key, value in args.items() if value is not None]
        return data


def val_variable(values: str) -> list[dict]:
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


def readable_file(filepath: str) -> str:
    """Checks if a file exists and is readable"""

    if filepath == '-':
        return "-"

    if not os.path.exists(filepath):
        # Raise ArgumentTypeError to make argparse show a clean error message
        raise argparse.ArgumentTypeError(f"File not found: {filepath}")

    if not os.access(filepath, os.R_OK):
        raise argparse.ArgumentTypeError(f"File not readable: {filepath}")

    # If all checks pass, return the original string (the filepath)
    return filepath


def parse_cmd_line(cli: list[str] | None = None) -> argparse.Namespace:
    """Command line parser function"""
    parser = argparse.ArgumentParser(
        description=_('Easily add tasks to Todoist with customizable YAML templates'),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        argument_default=argparse.SUPPRESS,
        exit_on_error=False
    )

    # positional arguments:
    file_parser = parser.add_mutually_exclusive_group()
    file_parser.add_argument(
        "template.file",
        nargs="?",  # a single value, which can be optional
        metavar="TEMPLATE_FILE",
        type=readable_file,
        default=sys.stdin,
        help=_("""the template file, if no file is supplied it uses standard input.
 Requirement: file encoding must be UTF-8"""))
    file_parser.add_argument(
        "--undo",
        dest="template.undo.file",
        metavar="UNDO_FILE",
        type=readable_file,
        help=_("loads undo file and rollbacks all operations in it")
    )

    parser.add_argument(
        "-t",
        dest="template.quick_add",
        default=False,
        action='store_true',
        help=_("""add a new item using the Todoist Quick Add implementation,
the template will be used as text for the new task""")
    )

    # options
    parser.add_argument(
        "-D",
        dest="template.variables",
        type=val_variable,  # can be a file or a comma separated list of key=value
        metavar="KEY0=VAL0,KEY1=VAL1... | PATH/TO/PARAMETERS.FILE",
        default={},
        help=_("can be a file or a comma separated list of key=value")
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
        type=readable_file,
        dest="configfile",
        help=_("TOML configuration file")
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
        version="%(prog)s " + __version__,
        help=_("show program's version number and exit"))

    tpl_type_group = parser.add_mutually_exclusive_group()
    tpl_type_group.add_argument(
        "--yaml",
        dest="template.type",
        action="store_const",
        const="YAML",
        help=_("template input file has YAML format")
    )
    tpl_type_group.add_argument(
        "--json",
        dest="template.type",
        action="store_const",
        const="JSON",
        help=_("template input file has JSON format")
    )
    tpl_type_group.add_argument(
        "--csv",
        dest="template.type",
        action="store_const",
        const="CSV",
        help=_(f"""template input file has CSV format.
Possible fields are: {', '.join(CSV_FIELDNAMES)}.
Default delimiter is '{CSV_DELIMITER}'.""")
    )
    tpl_type_group.add_argument(
        "--text",
        dest="template.type",
        action="store_const",
        const="PLAINTEXT",
        help=_("template input file has Plain/Text format.")
    )

    args, unknown = parser.parse_known_args(cli)
    logging.debug('unknown options: %s', str(unknown))
    return vars(args)

# ~@:-]
