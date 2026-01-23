#!/usr/bin/env python

"""Todoist-Template entry"""

import sys
import logging
from lib.config.config import TTConfig, PYTHON_MAX, PYTHON_MIN
from lib.todoist import TodoistTemplateAPI
from lib.todoist_template import AbstractTodoistAction, QuickAddAction, TemplateAction, UndoAction
from lib.config.apikey import APITokenStore


def main() -> int:
    """Main function"""
    try:
        cfg = TTConfig()

        logging.info("Starting todoist-template version %s", cfg.version)

        if not cfg.is_valid_python_version(PYTHON_MIN, PYTHON_MAX):
            raise SystemError(f"This script requires Python >= {PYTHON_MIN} and < {PYTHON_MAX}")

        if cfg.general.print_logo:
            print(cfg.general.logo)

        if not cfg.config.api_token:
            # get api_token from keyring or as user input
            api_token_store = APITokenStore(
                cfg.config.api_key_service,
                prompt=True)
            cfg.config.api_token = api_token_store.get()

        else:
            logging.debug('Use API token from cli')

        api = TodoistTemplateAPI(cfg)
        action: AbstractTodoistAction = None

        if cfg.template.undo.file is not None:
            action = UndoAction(cfg.template)
        elif cfg.template.quick_add:
            action = QuickAddAction(cfg.template)
        else:
            action = TemplateAction(cfg.template)

        return action.run(api)

    except Exception as exc:
        logging.error(exc, exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

# ~@:-]
