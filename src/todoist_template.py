#!/usr/bin/env python

"""Todoist-Template entry"""

import sys
import logging
from config.config import TTConfig, PYTHON_MAX, PYTHON_MIN  # pylint: disable=no-name-in-module
from config.apikey import APITokenStore  # pylint: disable=no-name-in-module
from todoist import TodoistTemplateAPI
from todoist_actions import TemplateContext, quick_add_action, undo_action, template_action


def main() -> int:
    """Main function"""
    try:
        cfg = TTConfig()

        if not cfg.is_valid_python_version:
            raise SystemError(f"This script requires Python >= {PYTHON_MIN} and < {PYTHON_MAX}")

        if cfg.general.print_logo:
            print(cfg.logo)

        if not cfg.config.api_token:
            # get api_token from keyring or as user input
            api_token_store = APITokenStore(
                cfg.config.api_key_service,
                prompt=True)
            cfg.config.api_token = api_token_store.get()

        else:
            logging.debug('Use API token from cli')

        context: TemplateContext = TemplateContext(
            api=TodoistTemplateAPI(cfg),
            template=cfg.template,
            variables=cfg.variables,
            is_dry_run=cfg.dry_run,
            is_update_tasks=cfg.is_update
        )

        result: int = 0
        if cfg.is_undo:
            result = undo_action(context)
        elif cfg.quick_add:
            result = quick_add_action(context)
        else:
            result = template_action(context)

        return 0 if result > 0 else 1

    except Exception as exc:
        logging.error(exc, exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

# ~@:-]
