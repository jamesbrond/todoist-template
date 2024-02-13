"""Todoist-template configuration handler"""
import sys
import os
import logging
import logging.config
import argparse
import csv
import toml
from lib.i18n import _
import lib.__version__ as version
from lib.template.template_factory import TEMPLATE_CSV, TEMPLATE_JSON, TEMPLATE_YAML


DEFAULT_CONFIG_FILE = 'lib/config/config.toml'
PYTHON_MIN = (3, 9)
PYTHON_MAX = (4, 0)


class TTOptions(dict):
    """
    Use a dot "." to access members of dictionary
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _ = [self.__compose(arg) for arg in args]

        if kwargs:
            self.__compose(kwargs)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super().__delitem__(key)
        del self.__dict__[key]

    def has_key(self, key):
        """Retrunt true if config contains `key`"""
        return key in self.keys()

    def __compose(self, arg, update=False):
        for key, value in arg.items():
            if isinstance(value, dict):
                if self.has_key(key) and update:
                    self[key].update(value)
                else:
                    self[key] = TTOptions(value)
            elif value is not None:
                self[key] = value

    def set(self, path, value):
        """Set value"""
        self.set_array(path.split('.'), value)

    def set_array(self, keys, value):
        """Set array of keys"""
        key = keys.pop(0)
        if len(keys) == 0:
            self[key] = value
        else:
            if not self.has_key(key):
                self[key] = TTOptions()
            self[key].set_array(keys, value)

    def update(self, arg):
        """Update config opbject"""
        if arg:
            self.__compose(arg, True)


class TTConfig:
    """Todoist-template configuration handler class"""

    def __init__(self, cliargs=None):
        # Options in descending order of relevance
        # 1. hardcoded values
        self._options = TTOptions({"config": {}})

        # 2. configuration file
        args = parse_cmd_line(cliargs)
        if args.get("configfile"):
            self._options.update(self._load_config(args.get("configfile")))
        else:
            self._options.update(self._load_config(DEFAULT_CONFIG_FILE))

        # 3. command line
        self._options.update(self._map_args(args))

        logging.config.dictConfig(self.log)  # self.log -> uses __getattr___(log)

    def __getattr__(self, attr):
        """Returns configuration value"""
        return self._options.get(attr)

    def is_empty(self):
        """Returns true if configuration is empty"""
        return len(self._options) == 0

    def check_python_version(self, pymin, pymax):
        """Check python requirements for application"""
        try:
            logging.debug("check python requirement %s - %s", str(pymin), str(pymax))
            return sys.version_info >= pymin or sys.version_info < pymax
        except Exception as exc:
            logging.fatal(exc)
            return False

    def _load_config(self, filename):
        # load TOML configuration from `filename`
        try:
            data = toml.load(filename)
            self._options.config.file = filename
            return data
        except (FileNotFoundError, PermissionError) as ex:
            if filename != DEFAULT_CONFIG_FILE:
                # fallback
                return self._load_config(DEFAULT_CONFIG_FILE)
            raise ValueError("Bad configuration file") from ex
        except toml.decoder.TomlDecodeError as ex:
            raise ValueError("Bad configuration file") from ex

    def _map_args(self, args):
        data = TTOptions()
        _ = [data.set(key, value) for key, value in args.items() if value is not None]
        return data


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
        metavar="TEMPLATE FILE",
        type=argparse.FileType('r', encoding='utf8'),
        default=None,
        help=_("""the template fil, if no file is supplied it uses standard input.
 Requirement: file encoding must be UTF-8"""))
    file_parser.add_argument(
        "--undo",
        dest="template.undo.file",
        metavar="UNDO_FILE",
        type=argparse.FileType("rb"),
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
        dest="configfile",
        default=DEFAULT_CONFIG_FILE,
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

# ~@:-]
