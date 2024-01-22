#!/usr/bin/env python

"""Todoist-Template entry"""
import os
import sys
import logging
import datetime
import lib.__version__ as version
from lib.config.config import TTConfig
from lib.todoist_template import TodoistTemplate
from lib.config.apikey import APITokenStore
from lib.i18n import _


def run_cli(api_token, cfg):
    """Run todoist-template as command line application"""
    is_undo = cfg.template.undo.file is not None
    is_quick_add = cfg.template.quick_add is not None

    todoist = TodoistTemplate(api_token, cfg.template.dry_run, is_undo)

    if is_undo:
        undo_filename = cfg.template.undo.file.name
        if todoist.rollback(cfg.template.undo.file):
            logging.debug(_("remove file %s"), undo_filename)
            os.remove(undo_filename)
    elif is_quick_add:
        text = cfg.template.quick_add
        if (len(text) >= 2 and text[0] == text[-1]) and text.startswith(("'", '"')):
            text =  text[1:-1]
        task = todoist.quick_add(text)
        logging.info("Task %s correctly added", task.id)
        logging.debug(task)
    else:
        template_filename = cfg.template.file.name

        todoist.upload(
            todoist.template(cfg.template),
            update_task=cfg.template.is_update)

        if not cfg.template.dry_run:
            now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            undofolder = os.path.join(
                os.path.dirname(os.path.realpath(sys.argv[0])),
                cfg.template.undo.folder)

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
        cfg.check_python_version(cfg.PYTHON_MIN, cfg.PYTHON_MAX)

        if cfg.general.print_logo:
            print(version.LOGO)

        api_token = cfg.config.api_token
        if not api_token:
            # get api_token from keyring or as user input
            api_token_store = APITokenStore(
                cfg.config.api_key_service,
                prompt=not cfg.general.gui)
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
