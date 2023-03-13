"""Configuration"""

import os
import sys
import logging
import logging.handlers
import toml
from lib.i18n import _
from lib.key_ring import APITokenStore


class Config():
    """Load and handle toml configuration file, parse command line arguments"""

    def __init__(self, args=None, prompt_api_token=False):
        """Load TOML configuration file"""
        self._options = self._configuration(args, "./config.toml", prompt_api_token)
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

        if args.get("service_id") is not None:
            data["keyring"]["keyring_token_name"] = args.get("service_id")

        if args.get("loglevel") is not None:
            data["log"]["cli_level"] = args.get("loglevel")

        data["service"]["run_service"] = args.get("gui")

        token_store = APITokenStore(data['keyring']['keyring_token_name'], prompt_api_token)

        data["todoist"].update({
            "template": args.get("template"),
            "placeholders": args.get("placeholders") if args.get("placeholders") else [{}],
            "dry_run": args.get("dry_run"),
            "is_update": args.get("is_update"),
            "token": args.get("token") if args.get("token") is not None else token_store.get(),
            "undo": args.get("undo")
        })

        return data

# ~@:-]
