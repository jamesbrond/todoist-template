"""Todoist-template configuration handler"""
from sys import version_info
from collections.abc import Iterable
import hashlib
from pathlib import Path
import logging
import logging.config
from typing import Any
import toml
from __version__ import __version__
from template.template_model import TTemplate
from .cliargs import parse_cmd_line


__location__ = Path(__file__).parent
DEFAULT_CONFIG_FILE = __location__ / 'config.toml'
PYTHON_MIN = "3.14"
PYTHON_MAX = "4.0"

# Module-level cache for config files
_config_file_cache: dict[str, dict] = {}

# Singleton instances
_ttconfig_instances = {}


def clear_config_cache() -> None:
    """Clear the configuration file cache. Useful for testing."""
    _config_file_cache.clear()
    logging.debug("Configuration cache cleared")


def singleton(cls):
    """Singleton decorator for classes"""
    def wrapper(*args, **kwargs):
        if cls not in _ttconfig_instances:
            _ttconfig_instances[cls] = cls(*args, **kwargs)
        return _ttconfig_instances[cls]
    return wrapper


def versiontuple(v):
    return tuple(map(int, (v.split("."))))


def check_python_version(pymin: str, pymax: str) -> bool:
    """Check python requirements for application"""
    current_version = version_info[:3]
    logging.debug("check current python %s against requirement %s - %s", str(current_version), pymin, pymax)
    return not (current_version < versiontuple(pymin) or current_version >= versiontuple(pymax))


class TTOptions(dict):
    """
    Use a dot "." to access members of dictionary
    """
    def __init__(self: TTOptions, *args: Iterable, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for arg in args:
            self.__compose__(arg)

        if kwargs:
            self.__compose__(kwargs)

    def __getattr__(self, attr: str) -> Any:
        return self.get(attr)

    def __setattr__(self, key: str, value: Any) -> None:
        self.__setitem__(key, value)

    def __setitem__(self, key: str, value: Any) -> None:
        super().__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item: str) -> None:
        self.__delitem__(item)

    def __delitem__(self, key: str) -> None:
        super().__delitem__(key)
        del self.__dict__[key]

    def __compose__(self, arg: dict[str, Any], update: bool = False) -> None:
        for key, value in arg.items():
            if isinstance(value, dict):
                if key in self and update:
                    self[key].update(value)
                else:
                    self[key] = TTOptions(value)
            elif value is not None:
                self[key] = value

    def set(self, path: str, value: Any) -> None:
        """Set value"""
        self.set_array(path.split('.'), value)

    def set_array(self, keys: list[str], value: Any) -> None:
        """Set array of keys"""
        key = keys.pop(0)
        if len(keys) == 0:
            self[key] = value
        else:
            if key not in self:
                self[key] = TTOptions()
            self[key].set_array(keys, value)

    def update(self, arg: dict[str, Any]) -> None:
        """Update config object"""
        if arg:
            self.__compose__(arg, True)


@singleton
class TTConfig:
    """Todoist-template configuration handler class"""

    def __init__(self, cliargs: list[str] | None = None) -> None:
        # Options in descending order of relevance
        # 1. hardcoded values
        # from default config file config/config.toml
        self._options = TTOptions({})
        self._options.update(self._load_config(DEFAULT_CONFIG_FILE))

        # 2. configuration file if any
        # command line argument --config
        args = parse_cmd_line(cliargs)
        if "configfile" in args:
            self._options.update(self._load_config(args.get("configfile")))

        # 3. command line arguments
        self._options.update(self._map_args(args))

        # computed configuration values
        # set is_undo flag
        self._options.is_undo = self._options.template_undo_file is not None
        self._options.template = TTemplate(
            file=self._options.template_file,
            undo_file=self._options.template_undo_file,
            undo_folder=self._options.config.undo_folder,
            type=self._options.template_type,
            encoding='utf-8'
        )

        # set up logging
        logging.config.dictConfig(self.log)  # self.log -> uses __getattr___(log)

    def __getattr__(self, attr: str) -> Any:
        """Returns configuration value"""
        return self._options.get(attr)

    def is_empty(self) -> bool:
        """Returns true if configuration is empty"""
        return len(self._options) == 0

    @property
    def version(self) -> str:
        """Returns application version"""
        return __version__

    @property
    def logo(self) -> str:
        """Returns application logo"""
        return self.general.logo.format(version=self.version)

    @property
    def is_valid_python_version(self) -> bool:
        """Check if current python version is valid for this application"""
        return check_python_version(PYTHON_MIN, PYTHON_MAX)

    def _generate_cache_key(self, filepath: Path) -> str:
        """Generate a unique cache key for the given file path"""
        m = hashlib.sha1()
        m.update(str(filepath.resolve()).encode('utf-8'))
        return m.hexdigest()

    def _load_config(self, filepath: Path) -> dict:
        """Load TOML configuration with caching"""
        cache_key = self._generate_cache_key(filepath)

        if cache_key in _config_file_cache:
            logging.debug("Using cached config from %s", cache_key)
            return _config_file_cache[cache_key].copy()

        try:
            data = toml.load(filepath)
            data.setdefault('config', {})['file'] = filepath
            _config_file_cache[cache_key] = data
            return data
        except (FileNotFoundError, PermissionError) as ex:
            raise ValueError("Cannot load configuration file") from ex
        except toml.decoder.TomlDecodeError as ex:
            raise ValueError("Bad configuration file") from ex

    def _map_args(self, args: dict) -> TTOptions:
        """Map command line arguments to TTOptions"""
        data = TTOptions()
        for key, value in args.items():
            if value is not None:
                data.set(key, value)
        return data

# ~@:-]
