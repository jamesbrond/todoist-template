#!/usr/bin/env python

"""UI for Todoist Template"""

import os
import sys
import datetime
import logging
import eel
import lib.__version__ as version
from lib.argparse import parse_cmd_line
from lib.config import Config
from lib.i18n import _
from lib.template import TodoistTemplate
from lib.loader.loaderfactory import TemplateLoaderFactory


def get_template_content(file):
    """Read template file with the right template loader factory"""
    template_loader = TemplateLoaderFactory().get_loader(file.name)
    logging.debug(_("use %s to load '%s' file"), template_loader.__class__.__name__, file.name)
    return template_loader.load(file)


def undo(undo_file, api_token):
    """Rollback Todoist Actions"""
    tmpl = TodoistTemplate(None, api_token, False, False)  # pylint: disable=too-many-function-args
    tmpl.rollback(undo_file)
    undo_file.close()
    logging.debug(_("remove file %s"), undo_file.name)
    os.remove(undo_file.name)


def run_batch_template(template, placeholders_list, api_token, dry_run, is_update, undofile=None):
    """Run template against a list of placeholders"""
    tmpl = TodoistTemplate(template, api_token, dry_run, is_update)  # pylint: disable=too-many-function-args
    for placeholders in placeholders_list:
        tmpl.parse(template, placeholders, undofile)


@eel.expose
def get_api_token():
    """Method called by JavaScript to get API Token"""
    return ""


# Expose this function to Javascript
@eel.expose
def run_script(template, placeholders, api_token, dry_run=False, is_update=False):
    """Method called by JavaScript"""
    run_batch_template(template, [placeholders], api_token, dry_run, is_update, undofile=None)
    return "thanks for running this script"


def run_gui(cfg):
    """Run todoist-template with GUI"""
    eel.init('build/ng', allowed_extensions=['.js', '.html'])

    logging.info(_("Service running on http://localhost:%d"), cfg.service['port'])
    eel.start(
        'index.html',
        host=cfg.service["host"],
        port=cfg.service["port"],
        mode=cfg.service["mode"],
        cmdline_args=[]
    )
    return 0


def run_cli(cfg):
    """Run todoist-template command line"""
    api_token = cfg.todoist['token']

    if cfg.todoist['undo']:
        undo(cfg.todoist['undo'], api_token)
        return 0

    with cfg.todoist['template'] as file:
        script_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
        if not cfg.todoist['dry_run']:
            now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            undofolder = os.path.join(script_folder, cfg.todoist['undo_folder'])
            if not os.path.exists(undofolder):
                os.makedirs(undofolder)
            undofile = os.path.join(
                undofolder,
                f"{os.path.basename(file.name)}-{now}.undo"
            )
        else:
            logging.info("### DRY RUN ###")
            undofile = None

        logging.debug(_("open file %s"), file.name)
        run_batch_template(
            get_template_content(file),
            cfg.todoist['placeholders'],
            api_token,
            cfg.todoist['dry_run'],
            cfg.todoist['is_update'],
            undofile
        )

    return 0


def main():
    """Main function"""
    args = parse_cmd_line()
    cfg = Config(args, prompt_api_token=True)
    try:
        cfg.check_python_version()
        if cfg.python['print_logo']:
            print(version.LOGO)
        return run_gui(cfg) if cfg.service["run_service"] else run_cli(cfg)
    except Exception as exc:  # pylint: disable=broad-except
        logging.error(exc, exc_info=logging.getLogger().isEnabledFor(logging.DEBUG))
    return 1


if __name__ == "__main__":
    sys.exit(main())

# ~@:-]
