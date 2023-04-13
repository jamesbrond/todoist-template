"""Todoist-template configuration handler"""
import sys
import logging
import logging.config
import toml
from lib.config.argparse import parse_cmd_line


class TTOptions(dict):
    """
    Use a dot "." to access members of dictionary
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for arg in args:
            self.__compose(arg)

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
        self._set_array(path.split('.'), value)

    def _set_array(self, keys, value):
        key = keys.pop(0)
        if len(keys) == 0:
            self[key] = value
        else:
            if not self.has_key(key):
                self[key] = TTOptions()
            self[key]._set_array(keys, value)  # pylint: disable=protected-access

    def update(self, arg):
        """Update config opbject"""
        if arg:
            self.__compose(arg, True)


class TTConfig:
    """Todoist-template configuration handler class"""

    DEFAULT_CONFIG_FILE = 'lib/config/config.toml'
    PYTHON_MIN = (3, 9)
    PYTHON_MAX = (4, 0)

    def __init__(self, cliargs=None):
        # Options in descending order of relevance
        # 1. hardcoded values
        self._options = TTOptions({
            "config": {
                "file": self.DEFAULT_CONFIG_FILE
            }
        })

        # 2. configuration file
        args = parse_cmd_line(cliargs)
        if args.get("configfile"):
            self._options.update(self._load_config(args.get("configfile")))
        else:
            self._options.update(self._load_config(self.DEFAULT_CONFIG_FILE))

        # 3. command line
        self._options.update(self._map_args(args))

        self._init_logging(self.log)

    def __getattr__(self, attr):
        """Returns configuration value"""
        return self._options.get(attr)

    def is_empty(self):
        """Returns true if configuration is empty"""
        return len(self._options) == 0

    def check_python_version(self, pymin, pymax):
        """Check python requirements for application"""
        logging.debug("check python requirement %s - %s", str(pymin), str(pymax))

        try:
            if sys.version_info < pymin or sys.version_info >= pymax:
                raise SystemError(f"This script requires Python >= {pymin} and < {pymax}")
        except TypeError as ex:
            raise SystemError from ex

    def _load_config(self, filename):
        # load TOML configuration from `filename`
        try:
            data = toml.load(filename)
            self._options.config.file = filename
            return data
        except (FileNotFoundError, PermissionError) as ex:
            if filename != self.DEFAULT_CONFIG_FILE:
                # fallback
                return self._load_config(self.DEFAULT_CONFIG_FILE)
            raise ValueError("Bad configuration file") from ex
        except toml.decoder.TomlDecodeError as ex:
            raise ValueError("Bad configuration file") from ex

    def _map_args(self, args):
        data = TTOptions()
        for key, value in args.items():
            if value is not None:
                data.set(key, value)
        return data

    def _init_logging(self, log_options):
        logging.config.dictConfig(log_options)

# ~@:-]
