#!/usr/bin/env python

"""Todoist-Template entry"""

import sys
import logging
from todoist_template.config.config import TTConfig, PYTHON_MAX, PYTHON_MIN  # pylint: disable=no-name-in-module
from todoist_template.config.apikey import APITokenStore  # pylint: disable=no-name-in-module
from todoist_template.todoist_api_wrapper import TodoistAPIWrapper
from todoist_template.todoist_actions import TemplateContext, quick_add_action, undo_action, template_action
from todoist_template.i18n import _t


def get_context(cfg: TTConfig, api: TodoistAPIWrapper) -> TemplateContext:
    """Get TemplateContext from TTConfig"""
    return TemplateContext(
        api=api,
        template=cfg.template,
        variables=cfg.variables,
        is_dry_run=cfg.dry_run,
        is_update_tasks=cfg.is_update
    )


def exception_handler(exception_type, exception, traceback):
    """Custom exception handler to print only the exception type and message"""
    logging.error(_t("Uncaught exception"), exc_info=(exception_type, exception, traceback))


def main() -> int:
    """Main function"""
    sys.excepthook = exception_handler
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
            logging.debug(_t('Use API token from cli'))

        with TodoistAPIWrapper(cfg) as api:
            result: int = 0
            context = get_context(cfg, api)

            if cfg.is_undo:
                result = undo_action(context)
            elif cfg.quick_add:
                result = quick_add_action(context)
            else:
                result = template_action(context)
            return 0 if result > 0 else 1

    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(main())

# ~@:-]
