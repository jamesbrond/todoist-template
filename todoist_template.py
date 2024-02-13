#!/usr/bin/env python

"""Todoist-Template entry"""
import os
import sys
import logging
import datetime
import lib.__version__ as version
from lib.config.config import TTConfig, PYTHON_MAX, PYTHON_MIN
from lib.todoist_template import TodoistTemplate
from lib.config.apikey import APITokenStore
from lib.i18n import _


def run_cli(api_token, cfg):
    """Run todoist-template as command line application"""
    is_undo = cfg.template.undo.file is not None
    is_quick_add = cfg.template.quick_add

    todoist = TodoistTemplate(api_token, cfg.template.dry_run, is_undo, is_quick_add)

    if is_undo:
        _undo(todoist, cfg.template.undo)
    elif is_quick_add:
        _quick_add(todoist, cfg.template)
    else:
        _template(todoist, cfg.template)


def _undo(todoist, undo):
    logging.info("undo action")
    undo_filename = undo.file.name
    if todoist.rollback(undo.file):
        logging.debug(_("remove file %s"), undo_filename)
        os.remove(undo_filename)


def _quick_add(todoist, config):
    # Example: echo "test {when} @bb" | python todoist_template.py -t -D when=today -
    logging.info("quick add action")
    todoist.quick_add(config)


def _template(todoist, config):
    logging.debug("template action")

    template_filename = "".join([x if x.isalnum() else "" for x in config.file.name])
    todoist.template(config, update_task=config.is_update)

    if not config.dry_run:
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        undofolder = os.path.join(
            os.path.dirname(os.path.realpath(sys.argv[0])),
            config.undo.folder)

        if not os.path.exists(undofolder):
            os.makedirs(undofolder)

        undofile = os.path.join(
            undofolder,
            f"{os.path.basename(template_filename)}-{now}.undo")

        todoist.store_rollback(undofile)


def main():
    """Main function"""
    try:
        cfg = TTConfig()
        if not cfg.check_python_version(PYTHON_MIN, PYTHON_MAX):
            raise SystemError(f"This script requires Python >= {PYTHON_MIN} and < {PYTHON_MAX}")

        if cfg.general.print_logo:
            print(version.LOGO)

        api_token = cfg.config.api_token
        if not api_token:
            # get api_token from keyring or as user input
            api_token_store = APITokenStore(
                cfg.config.api_key_service,
                prompt=True)
            api_token = api_token_store.get()
        else:
            logging.debug('Use API token from cli')

        run_cli(api_token, cfg)

        return 0

    except Exception as exc:
        logging.error(exc, exc_info=logging.getLogger().isEnabledFor(logging.DEBUG))
        return 1


if __name__ == "__main__":
    sys.exit(main())

# ~@:-]
